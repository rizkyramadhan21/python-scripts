#!/usr/bin/python
#---------------------------------------
# cetakATMProJakarta3.py
# (c) Jansen A. Simanullang, 16:40
# 07.04.2015 10:10 AM
# 07.01.2016 10:45 PM
# 08.01.2016 19:05 PM proxychains telegram-cli -W -e
# 03.02.2016, 09.02.2016 add officer code as branchcode
# to be used with telegram-bot plugin
#---------------------------------------
# usage: cetakALECProJakarta3 atm/cdm/edc/loan
# script name followed by space and TelegramName
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
	
alamatURL = 'http://172.18.65.42/monitorcdm/'

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




def cetakCDMPro(strKanwil):

	from pyvirtualdisplay import Display
	from selenium import webdriver

	display = Display(visible=0, size=(800, 600))
	display.start()

	# now Firefox run in a virtual display. 
	# you will not see the browser.
	browser = webdriver.Firefox()

	alamatURL = 'http://172.18.65.42/monitorcdm/'

	browser.get(alamatURL)

	browser.title
	print "logging in... "
	browser.find_elements_by_css_selector("input[type='radio'][value='GUEST']")[0].click()
	browser.find_element_by_class_name('tbutton').click()
	browser.get(alamatURL)

	print "getting in... "
	browser.get('http://172.18.65.42/monitorcdm/?_module_='+strKanwil)
	strHTML = browser.page_source

	browser.quit()
	display.stop()
	#------------------------------------------------------------------------------------


        arrTable, strStyle = analyzeHTML(strHTML)
	numRows, numRowsHead, numCols, table = getTableDimension(arrTable)

	strNamaFile = "MONITORING CDM " + strRegionName + " -" + time.strftime("%Y%m%d") + ".html"
	strNamaFilePDF = "cdmpro-" + time.strftime("%Y%m%d-%H") + ".pdf"

	dTabel = '<h1>Monitoring CDM  ' + strRegionName + ' - ' + time.strftime("(%d.%m.%Y - %H:%M)")+ "</h1>" +str(table)
	
	strHTML = '<HTML><HEAD><TITLE>Monitoring CDM  ' + strRegionName + ' </TITLE><META HTTP-EQUIV="REFRESH" CONTENT="3600">'+ strStyle +'</HEAD><body>' + dTabel

	strNamaFile = prepareDirectory('OUTPUT', 'CDM') + strNamaFile
	strNamaFilePDF = prepareDirectory('OUTPUT', 'CDM') + strNamaFilePDF

	options = {'page-size': 'A2', 'orientation':'landscape'}

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



if len(sys.argv) > 0:

#-----------------------------------------------------------------------------------

	try:

		strGenre = sys.argv[1]

	except IndexError:

		strGenre = defaultGenre

	try:

		strBranchCode = sys.argv[2]

	except:
			
		strBranchCode = defaultBranchCode

	try:

		TelegramName = sys.argv[3]

	except IndexError: #list index out of range

		TelegramName = defaultTelegramName

#-----------------------------------------------------------------------------------


	if strGenre.upper() == 'ATM':

		if strBranchCode.upper() == '0853':

			alamatURL = 'http://172.18.65.42/statusatm/dashboard_cabang.pl?REGID=15&REGNAME=Jakarta%20III'

		else:

			alamatURL = "http://172.18.65.42/statusatm/viewbybranch6.pl?AREA_ID=" + strBranchCode

		strNamaFile = cetakURL('A4','portrait', 'ATM', alamatURL, strBranchCode)
		

	if strGenre.upper() == 'LOAN':

		if strBranchCode.upper() == '0853':
	
			alamatURL = 'http://172.18.65.42/statusloan/dashboard_cabang.pl?REGID=Q&REGNAME=Jakarta%203'

		elif checkPureDigit(strBranchCode) == True:

				alamatURL = 'http://172.18.65.42/statusloan/dashboard_ao_allsegment.pl?BRID='+strBranchCode

		else:

				alamatURL = 'http://172.18.65.42/statusloan/dashboard_ao_detail_debitur.pl?offCode='+strBranchCode.upper()
		

		strNamaFile = cetakURL('A4', 'landscape','LOAN', alamatURL, strBranchCode)



	if strGenre.upper() == 'EDC':

		if strBranchCode.upper() == '0853':
	
			strNamaFile = cetakURL('A2', 'landscape','EDC', 'http://172.18.44.66/edcpro/index.php/main/kanwil_implementor?kanwil=Q', strBranchCode)

		else:

			pass

	if strGenre.upper() == 'CDM':

		if strBranchCode.upper() == '0853':
	
			strNamaFile = cetakCDMPro(defaultStrKanwil)

		else:

			pass


	telegramCommand = 'echo "send_file '+TelegramName+' '+strNamaFile+'" | nc 127.0.0.1 8885'
	telegramCommand = 'proxychains telegram-cli -W -e "send_file '+TelegramName+' '+strNamaFile+'"'

	print telegramCommand
	os.system(telegramCommand)

