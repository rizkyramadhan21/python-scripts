#!/usr/bin/python
#---------------------------------------
# cetakSavingProJakarta3.py
# (c) Jansen A. Simanullang
# 12.02.2016 20:37
# to be used with telegram-bot plugin
#---------------------------------------
# usage:
# cetakSavingProJakarta3.py [1] [2] [3] [4]
# script name followed by 4 arguments
# requires wkhtmltopdf  0.12.2.1 (with patched qt) 
# or newer
#---------------------------------------

import pdfkit, time, os, sys
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
from splinter import Browser
import os, time, urlparse

defaultTelegramName = "0853_TSI_-_Jansen_Simanullang"
defaultGenre = 'ATM'
defaultStrKanwil = 'kanwil_jkt3'
defaultBranchCode = '0853'
strRegionName = 'JAKARTA III'

scriptDirectory = os.path.dirname(os.path.abspath(__file__)) + "/"



def prepareDirectory(strOutputDir, strOutputSubdir):

	# siapkan struktur direktori untuk penyimpanan data
	# struktur direktori adalah ['OUTPUT', 'ATM', '2015', '04-APR', 'DAY-28'] makes './OUTPUT/ATM/2015/04-APR/DAY-28'

	arrDirectoryStructure = [strOutputDir, strOutputSubdir, time.strftime("%Y"), time.strftime("%m-%b").upper() , "DAY-"+time.strftime("%d"), 'PDF']

	fullDirPath = scriptDirectory

	for i in range (0, len(arrDirectoryStructure)):
	
		fullDirPath = fullDirPath + arrDirectoryStructure[i] + "/"

		if not os.path.exists(fullDirPath):

			print "creating directories:", arrDirectoryStructure[i]
		    	os.mkdir(fullDirPath)
			os.chdir(fullDirPath)

	print fullDirPath

	return fullDirPath



def cetakURL(strPaperSize, strOrientation, strGenre, strURL, strBranchCode):

	options = {'page-size': strPaperSize, 'orientation':strOrientation}
	strNamaFile = strGenre.lower()+"pro-" + time.strftime("%Y%m%d-%H-") + strBranchCode+ ".pdf"
	strNamaFile = prepareDirectory('OUTPUT', strGenre) + strNamaFile
	pdfkit.from_url(strURL, strNamaFile, options)

	return strNamaFile

#-----------------------------------------------------------------------------------

def getTableDimension(arrTable):

	# fungsi ini untuk mendapatkan dimensi tabel dan isinya berdasarkan data sream string HTML
	# fungsi ini melanjutkan dari fungsi fetchHTML()
	# dimensi tabel dimaksud adalah jumlah baris dan jumlah kolom pada tabel
	# inisialisasi variabel 'largest_table' dan 'max_rows'

	# bagaimana cara menentukan tabel mana yang berisi data?
	# pilihlah tabel yang terbesar yang memiliki jumlah baris terbanyak

	largest_table = None

	max_rows = 0

	for table in arrTable:

		# cek satu per satu jumlah baris yang ada pada masing-masing tabel dalam array kumpulan tabel
		# simpan dalam variabel bernama numRows

		numRows = len(table.findAll(lambda tag: tag.name == 'tr' and tag.findParent('table') == table))
		
		# jika jumlah baris pada suatu tabel lebih besar daripada '0' maka jadikan sebagai max_rows sementara
		# proses ini diulangi terus menerus maka max_rows akan berisi jumlah baris terbanyak

		if numRows > max_rows:
			
		        largest_table = table
			max_rows = numRows

	# ini hanya mengembalikan penyebutan 'tabel terbesar' hanya sebagai 'tabel'
	# dan mengembalikan penyebutan 'jumlah baris terbanyak' hanya sebagai 'jumlah baris'

	table = largest_table

	numRows = max_rows

	# bagaimana cara menentukan berapa jumlah kolomnya?

	numCols = len(table.contents[1])
	

	# bagaimana cara menentukan berapa jumlah baris yang terpakai sebagai header?

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')

	# inisialisasi variabel numRowsHead sebagai jumlah baris yang mengandung header

	numRowsHead = 0	
	
	# periksa satu per satu setiap baris

	for i in range (0, numRows):
		
		# apabila dalam suatu baris tertentu terdapat tag <th>
		if rows[i].findAll('th'):
			
			# maka numRows bertambah 1
			numRowsHead = i + 1


	# hasil akhir fungsi getTableDimension ini menghasilkan jumlah baris, jumlah baris yang terpakai header, jumlah kolom dan isi tabel itu sendiri

	return numRows, numRowsHead, numCols, table

#-----------------------------------------------------------------------------------


def fileCreate(strNamaFile, strData):
	f = open(strNamaFile, "w")
	f.writelines(str(strData))
	f.close()
    
def fileAppend(strNamaFile, strData):
	f = open(strNamaFile, "a")
	f.writelines(str(strData))
	f.close()


#-----------------------------------------------------------------------------------


def getParentURL(alamatURL):

	parts = alamatURL.split('//', 2)
	parentURL = parts[0]+'//' + parts[1].split('/')[0] + '/' + parts[1].split('/')[1]
	return parentURL
	# contoh hasilnya
	# alamatURL='http://172.18.65.42/monitorcdm/?_module_=kanwil_jkt3'
	# parentURL = http://172.18.65.42/monitorcdm
	
alamatURL = 'http://172.18.41.101/DashboardSimpanan/'

def analyzeHTML(strHTML):

	print "analyzing html..."

	parentURL = getParentURL(alamatURL)

	strHTML = strHTML.replace('href="./','href="'+parentURL+'/')
	strHTML = strHTML.replace('href="?_','href="'+parentURL+'/?_')
	# fix broken HTML
	strHTML = strHTML.replace('</tr><td>',"</tr><tr><td>")
	strHTML = strHTML.replace('</td></tr><td>','</td></tr><tr><td>')

	mysoup = BeautifulSoup(strHTML)

	arrTable = mysoup.findAll('table')
	arrStyle = mysoup.findAll( 'link' , rel = "stylesheet" )
	strStyle = ""

	for i in range (0, len(arrStyle)):

		strStyle = strStyle + str(arrStyle[i])
	

	return arrTable, strStyle




def danaKanwil(strKanwil):

	from pyvirtualdisplay import Display
	from selenium import webdriver

	display = Display(visible=0, size=(800, 600))
	display.start()

	# now Firefox run in a virtual display. 
	# you will not see the browser.
	browser = webdriver.Firefox()

	alamatURL = 'http://172.18.41.101/DashboardSimpanan/'

	browser.get(alamatURL)

	print browser.title
	print "getting in... "
	alamatURL ="http://172.18.41.101/DashboardSimpanan/index.php/c_RptMonitoringDPK/getBranchSegmentByKanwil/"
	browser.get(alamatURL+strKanwil)
	strHTML = browser.page_source

	browser.quit()
	display.stop()
	#------------------------------------------------------------------------------------


	arrTable, strStyle = analyzeHTML(strHTML)
	numRows, numRowsHead, numCols, table = getTableDimension(arrTable)

	strNamaFile = "MONITORING SIMPANAN " + strRegionName + " -" + time.strftime("%Y%m%d") + ".html"
	strNamaFilePDF = "savingpro-" + time.strftime("%Y%m%d-%H") + ".pdf"

	dTabel = '<h1  style="color: #0000FF;">Monitoring SIMPANAN  ' + strRegionName + ' - ' + time.strftime("(%d.%m.%Y - %H:%M)")+ "</h1>" +str(table)
	
	strHTML = '<HTML><HEAD><TITLE>Monitoring SIMPANAN  ' + strRegionName + ' </TITLE><META HTTP-EQUIV="REFRESH" CONTENT="3600">'+ strStyle +'</HEAD><body>' + dTabel

	strNamaFile = prepareDirectory('OUTPUT', 'SAVING') + strNamaFile
	strNamaFilePDF = prepareDirectory('OUTPUT', 'SAVING') + strNamaFilePDF

	options = {'page-size': 'A2', 'orientation':'landscape'}

	fileCreate(strNamaFile, strHTML)
	pdfkit.from_file(strNamaFile, strNamaFilePDF, options)

	return strNamaFilePDF

#-----------------------------------------------------------------------------------


def danaKanca(strBranchCode):

	strBranchCode = str(int(strBranchCode))


	from pyvirtualdisplay import Display
	from selenium import webdriver

	display = Display(visible=0, size=(800, 600))
	display.start()

	# now Firefox run in a virtual display. 
	# you will not see the browser.
	browser = webdriver.Firefox()

	alamatURL = 'http://172.18.41.101/DashboardSimpanan/'

	browser.get(alamatURL)

	print browser.title

	print "getting in... "
	alamatURL ="http://172.18.41.101/DashboardSimpanan/index.php/c_RptMonitoringDPK/getUkerSegmentByBranch/"
	browser.get(alamatURL+strBranchCode)
	strHTML = browser.page_source

	browser.quit()
	display.stop()
	#------------------------------------------------------------------------------------


	arrTable, strStyle = analyzeHTML(strHTML)
	numRows, numRowsHead, numCols, table = getTableDimension(arrTable)

	strNamaFile = "MONITORING SIMPANAN " + strBranchCode + " -" + time.strftime("%Y%m%d") + ".html"

	strNamaFilePDF = "savingpro-" + time.strftime("%Y%m%d-") +strBranchCode+ ".pdf"

	dTabel = '<h1  style="color: #0000FF;">Monitoring SIMPANAN  ' + strBranchCode + ' - ' + time.strftime("(%d.%m.%Y - %H:%M)")+ "</h1>" +str(table)
	
	strHTML = '<HTML><HEAD><TITLE>Monitoring SIMPANAN  ' + strBranchCode + ' </TITLE><META HTTP-EQUIV="REFRESH" CONTENT="3600">'+ strStyle +'</HEAD><body>' + dTabel

	strNamaFile = prepareDirectory('OUTPUT', 'SAVING') + strNamaFile
	strNamaFilePDF = prepareDirectory('OUTPUT', 'SAVING') + strNamaFilePDF

	options = {'page-size': 'A2', 'orientation':'landscape'}

	fileCreate(strNamaFile, strHTML)
	pdfkit.from_file(strNamaFile, strNamaFilePDF, options)

	return strNamaFilePDF


def danaUker(strBranchCode):

	strBranchCode = str(int(strBranchCode))

	from pyvirtualdisplay import Display
	from selenium import webdriver

	display = Display(visible=0, size=(800, 600))
	display.start()

	# now Firefox run in a virtual display. 
	# you will not see the browser.
	browser = webdriver.Firefox()

	alamatURL ="http://172.18.41.101/DashboardSimpanan/index.php/c_RptMonitoringDPK/getOfficerSegmentByLevel/"
	browser.get(alamatURL+strBranchCode+"/Funding-Officer")

	print browser.title
	strHTML = browser.page_source

	browser.quit()
	display.stop()
	#------------------------------------------------------------------------------------


	arrTable, strStyle = analyzeHTML(strHTML)
	numRows, numRowsHead, numCols, table = getTableDimension(arrTable)

	strNamaFile = "MONITORING SIMPANAN " + strBranchCode + " -" + time.strftime("%Y%m%d") + ".html"
	strNamaFilePDF = "savingpro-" + time.strftime("%Y%m%d-") +strBranchCode+ ".pdf"

	dTabel = '<h1  style="color: #0000FF;">Monitoring SIMPANAN  ' + strBranchCode.zfill(4) + '</h1><h4>posisi tanggal ' + time.strftime("%d.%m.%Y jam %H:%M")+ "</h4>" +str(table)
	
	strHTML = '<HTML><HEAD><TITLE>Monitoring SIMPANAN  ' + strBranchCode + ' </TITLE><META HTTP-EQUIV="REFRESH" CONTENT="3600">'+ strStyle +'</HEAD><body>' + dTabel

	strNamaFile = prepareDirectory('OUTPUT', 'SAVING') + strNamaFile
	strNamaFilePDF = prepareDirectory('OUTPUT', 'SAVING') + strNamaFilePDF

	options = {'page-size': 'A2', 'orientation':'landscape'}

	fileCreate(strNamaFile, strHTML)
	pdfkit.from_file(strNamaFile, strNamaFilePDF, options)

	return strNamaFilePDF



def upDownByFO(strBranchCode, strOfficerCode):

	strBranchCode = str(int(strBranchCode))

	from pyvirtualdisplay import Display
	from selenium import webdriver

	display = Display(visible=0, size=(800, 600))
	display.start()

	# now Firefox run in a virtual display. 
	# you will not see the browser.
	browser = webdriver.Firefox()

	alamatURL ="http://172.18.41.101/DashboardSimpanan/index.php/c_RptMonitoringDPK/getAccountByOfficerCode/"
	browser.get(alamatURL+strBranchCode+"/"+strOfficerCode)

	print browser.title
	strHTML = browser.page_source

	browser.quit()
	display.stop()
	#------------------------------------------------------------------------------------


	arrTable, strStyle = analyzeHTML(strHTML)
	numRows, numRowsHead, numCols, table = getTableDimension(arrTable)

	strNamaFile = "MONITORING SIMPANAN " + strOfficerCode + " -" + time.strftime("%Y%m%d") + ".html"
	strNamaFilePDF = "savingpro-" + time.strftime("%Y%m%d-") +strOfficerCode+ ".pdf"

	dTabel = '<h1  style="color: #0000FF;">Monitoring SIMPANAN  ' + strOfficerCode + '</h1><h4>posisi tanggal ' + time.strftime("%d.%m.%Y jam %H:%M")+ "</h4>" +str(table)
	
	strHTML = '<HTML><HEAD><TITLE>Monitoring SIMPANAN  ' + strOfficerCode + ' </TITLE><META HTTP-EQUIV="REFRESH" CONTENT="3600">'+ strStyle +'</HEAD><body>' + dTabel

	strNamaFile = prepareDirectory('OUTPUT', 'SAVING') + strNamaFile
	strNamaFilePDF = prepareDirectory('OUTPUT', 'SAVING') + strNamaFilePDF

	options = {'page-size': 'A3', 'orientation':'landscape'}

	fileCreate(strNamaFile, strHTML)
	pdfkit.from_file(strNamaFile, strNamaFilePDF, options)

	return strNamaFilePDF


#-----------------------------------------------------------------------------------
def checkPureDigit(strBranchCode):
	# return true if it is a pure digit
	# return false if it contains alphs

	hasilcek = True

	for i in strBranchCode:

		hasilcek = hasilcek and i.isdigit()

	return hasilcek
			
			
		



#-----------------------------------------------------------------------------------





#danaKanwil("Q")
#danaKanca("Q","19")
#danaUker("19")
#upDownByFO("19", "AE0")

#-----------------------------------------------------------------------------------
defaultGenre = "dana" # dana, fo
defaultGenreUker = "kanwil" #kanwil, kanca, uker
defaultBranchCode = "0853"
defaultTelegramName = "0853_TSI_-_Jansen_Simanullang"

if len(sys.argv) > 0:

#-----------------------------------------------------------------------------------

	try:

		strGenre = sys.argv[1] #dana atau FO

	except IndexError:

		strGenre = defaultGenre
#---------------------------------------------

	try:

		strGenreUker = sys.argv[2] #kanwil, kanca, uker

	except IndexError:

		strGenreUker = defaultGenreUker
#---------------------------------------------
	try:

		strBranchCode = sys.argv[3]

	except:
			
		strBranchCode = defaultBranchCode
#---------------------------------------------
	try:

		TelegramName = sys.argv[4]

	except IndexError: #list index out of range

		TelegramName = defaultTelegramName

#-----------------------------------------------------------------------------------


	if strGenre.upper() == 'DANA':

		if strGenreUker.upper() == 'KANWIL':

			strNamaFile = danaKanwil("Q")

		elif strGenreUker.upper() == 'KANCA':

			strNamaFile = danaKanca(strBranchCode)

		elif strGenreUker.upper() == 'UKER':

			strNamaFile = danaUker(strBranchCode)

	if strGenre.upper() == 'FO':
		
		strNamaFile = upDownByFO(sys.argv[2], sys.argv[3])


	telegramCommand = 'echo "send_file '+TelegramName+' '+strNamaFile+'" | nc 127.0.0.1 8885'
	telegramCommand = 'proxychains telegram-cli -W -e "send_file '+TelegramName+' '+strNamaFile+'"'

	print telegramCommand
	os.system(telegramCommand)

