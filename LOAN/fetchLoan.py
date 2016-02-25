#!/usr/bin/python
#---------------------------------------
# fetchLoan.py
# (c) Jansen A. Simanullang
# 25.02.2016
# to be used with telegram-bot plugin
#---------------------------------------
# usage:
# fetchLoan.py [1] [2] [3] [4]
# script name followed by 4 arguments
# [1] genre
# [2] subgenre
# [3] branchcode
# [4] TelegramName
# requires wkhtmltopdf  0.12.2.1 (with patched qt) 
# or newer
#---------------------------------------

import pdfkit, time, os, sys
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
from splinter import Browser
import os, time, urlparse

defaultGenre = 'ritel'
defaultSubGenre = 'komersial'
defaultBranchGenre = 'kanca' # either 'kanwil', 'kanca', 'uker'
defaultBranchCode = '0853'
defaultTelegramName = "0853_TSI_-_Jansen_Simanullang"
strRegionName = 'JAKARTA III'
alamatURL = "http://172.18.65.42/monitorloan/"

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



def cetakURL(strPaperSize, strOrientation, strURL, strBranchCode, strGenre, strSubGenre, strBranchGenre):

	options = {'page-size': strPaperSize, 'orientation':strOrientation}
	strNamaFile = strGenre.lower()+"-"+strSubGenre + "-" + strBranchGenre +"-"+ strBranchCode +time.strftime("-%Y%m%d") + ".pdf"
	strNamaFile = prepareDirectory('OUTPUT', 'LOAN') + strNamaFile
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
#---------------------------------------
	try:

		strSubGenre = sys.argv[2]

	except:
			
		strSubGenre = defaultSubGenre
#---------------------------------------
	try:

		strBranchGenre = sys.argv[3]

	except:
			
		strBranchGenre = defaultBranchGenre
#---------------------------------------
	try:

		strBranchCode = str(int(sys.argv[4]))

	except:
			
		strBranchCode = defaultBranchCode
#---------------------------------------
	try:

		TelegramName = sys.argv[5]

	except IndexError: #list index out of range

		TelegramName = defaultTelegramName

#-----------------------------------------------------------------------------------


	if strGenre.upper() == 'MIKRO':

		if strSubGenre.upper() == 'KUPEDES':

			segmenID = "11100"
			strDESC = "KREDIT%20MIKRO%20-KUPEDES"

		if strSubGenre.upper() == 'KUPRAK':

			segmenID = "11300"
			strDESC = "KREDIT%20MIKRO%20-KUPEDES RAKYAT"

		if strSubGenre.upper() == 'KUR':

			segmenID = "11200"
			strDESC = "KREDIT%20MIKRO%20-KUR MIKRO"

		if strSubGenre.upper() == 'GBT':

			segmenID = "12000"
			strDESC = "KREDIT%20MIKRO%20-GBT"

#-----------------------------------------------


	if strGenre.upper() == 'RITEL':

		if strSubGenre.upper() == 'KRETAP':

			segmenID = "41210"
			strDESC = "RITEL KONSUMTIF - KRETAP"

		if strSubGenre.upper() == 'KRESUN':

			segmenID = "41220"
			strDESC = "RITEL KONSUMTIF - KRESUN"

		if strSubGenre.upper() == 'PITUNG':

			segmenID = "41230"
			strDESC = "RITEL KONSUMTIF - PITUNG"

		if strSubGenre.upper() == 'CASHCOLL':

			segmenID = "42100"
			strDESC = "RITEL KONSUMTIF - CASHCOLL"

		if strSubGenre.upper() == 'NONCASHCOLL':

			segmenID = "42200"
			strDESC = "RITEL KONSUMTIF - NONCASHCOLL"



#-----------------------------------------------

	if strGenre.upper() == 'KONSUMER':

		if strSubGenre.upper() == 'KPR':

			segmenID = "41250"
			strDESC = "KONSUMER - KPR"

		if strSubGenre.upper() == 'MOBIL':

			segmenID = "41270"
			strDESC = "KONSUMER - MOBIL"

		if strSubGenre.upper() == 'KMG':

			segmenID = "41290"
			strDESC = "KONSUMER - KMG"

#-----------------------------------------------

	if strGenre.upper() == 'PROGRAM':

		if strSubGenre.upper() == 'KUR':

			segmenID = "51000"
			strDESC = "PROGRAM - KUR"

		if strSubGenre.upper() == 'NONKUR':

			segmenID = "52000"
			strDESC = "PROGRAM - NON KUR"

#-----------------------------------------------

	dashboardKanwil = 'dashboard_segdetail2'
	dashboardKanca = 'dashboard_segdetail3'
	dashboardUker = 'dashboard_ao_segdet'

#-----------------------------------------------------------------------------------


	if strBranchGenre.upper() == 'KANWIL':

		print "KANWIL"

		if strBranchCode.upper() == '853':

			alamatURL = 'http://172.18.65.42/statusloan/'+dashboardKanwil+'.pl?DESC='+strDESC+'&SEGMEN='+segmenID+'&REGID=Q&REGNAME=KANWIL%20JAKARTA%203'

	elif strBranchGenre.upper() == 'KANCA':

		alamatURL = 'http://172.18.65.42/statusloan/'+dashboardKanca+'.pl?DESC='+strDESC+'&SEGMEN='+segmenID+'&MBRID='+strBranchCode

	elif strBranchGenre.upper() == 'UKER':

		alamatURL = 'http://172.18.65.42/statusloan/'+dashboardUker+'.pl?DESC='+strDESC+'&SEGMEN='+segmenID+'&BRID='+strBranchCode
			
#-----------------------------------------------------------------------------------



	strNamaFile = cetakURL('A4', 'landscape', alamatURL, strBranchCode, strGenre, strSubGenre, strBranchGenre)

	
#-----------------------------------------------------------------------------------

	telegramCommand = 'echo "send_file '+TelegramName+' '+strNamaFile+'" | nc 127.0.0.1 8885'
	telegramCommand = 'proxychains telegram-cli -W -e "send_file '+TelegramName+' '+strNamaFile+'"'

	print telegramCommand
	os.system(telegramCommand)
