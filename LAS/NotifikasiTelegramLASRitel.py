# -*- coding: utf-8 -*-
#!/usr/bin/python
#---------------------------------------
# NotifikasiTelegramLAS.py
# (c) Jansen A. Simanullang, 25.01.2016
# to be used with LASRecipients
#---------------------------------------
# usage: NotifikasiTelegramLAS
# example: NotifikasiTelegramLAS
#---------------------------------------

from urllib import urlopen
from BeautifulSoup import BeautifulSoup
import os, sys, time, urlparse, smtplib
import urllib, urllib2
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage


################################################################################################
firstURL='http://172.18.65.56/lasmobileritel/index.php/dashboard/load_content'
RegionName = "Jakarta 3"
################################################################################################

scriptDirectory = os.path.dirname(os.path.abspath(__file__)) + "/"

asciiArt="""
	   ▄▄▄▄▄▄▄▄▄
        ▄█████████████▄ 
█████  █████████████████  █████
▐████▌ ▀███▄       ▄███▀ ▐████▌
 █████▄  ▀███▄   ▄███▀  ▄█████
 ▐██▀███▄  ▀███▄███▀  ▄███▀██▌    
  ███▄▀███▄  ▀███▀  ▄███▀▄███ 
  ▐█▄▀█▄▀███ ▄─▀─▄ ███▀▄█▀▄█▌
   ███▄▀█▄██ ██▄██ ██▄█▀▄███
    ▀███▄▀██ █████ ██▀▄███▀
   █▄ ▀█████ █████ █████▀ ▄█
   ███        ███	 ███
   ███▄    ▄█ ███ █▄	▄███
   █████ ▄███ ███ ███▄ █████
   █████ ████ ███ ████ █████
   █████ ████ ███ ████ █████
   █████ ████ ███ ████ █████
   █████ ████▄▄▄▄▄████ █████
    ▀███ █████████████ ███▀
      ▀█ ███ ▄▄▄▄▄ ███ █▀
         ▀█▌▐█████▌▐█▀
            ███████
"""

asciiArt="""
	   ▄▄▄▄▄▄▄▄▄
        ▄█████████████▄ 
█████  █████████████████  █████
▐████▌ ▀███▄       ▄███▀ ▐████▌
 █████▄  ▀███▄   ▄███▀  ▄█████    NOTIFIKASI LAS via TELEGRAM
"""

asciiArt = asciiArt +" ▐██▀███▄  ▀███▄███▀  ▄███▀██▌    "+RegionName
asciiArt = asciiArt +"""
  ███▄▀███▄  ▀███▀  ▄███▀▄███     
  ▐█▄▀█▄▀███ ▄▀ ▀▄ ███▀▄█▀▄█▌     (c) JANSEN SIMANULLANG
   ███▄▀█▄██ ██ ██ ██▄█▀▄███      MEI 2015 - JANUARI 2016
    ▀███▄▀██ ██ ██ ██▀▄███▀
   █▄ ▀█████ █████ █████▀ ▄█        \__/  \__/  \__/  \__/  \__/  \__/
   ███        ███	 ███      __/  \__/  \__/  \__/  \__/  \__/  \_
   ███▄    ▄█ ███ █▄	▄███        \__/  \__/  \__/  \__/  \__/  \__/ 
   █████ ▄███ ███ ███▄ █████     \__/  \__/  \__/  \__/  \__/  \__/  \_
   █████ ████ ███ ████ █████        \__/  \__/  \__/  \__/  \__/  \__/ 
   █████ ████ ███ ████ █████     \__/  \__/  \__/  \__/  \__/  \__/  \_ 
   █████ ████ ███ ████ █████        \__/  \__/  \__/  \__/  \__/  \__/ 
   █████ ████▄▄▄▄▄████ █████     \__/  \__/  \__/  \__/  \__/  \__/   
    ▀███ █████████████ ███▀    __/  \__/  \__/  \__/  \__/  \__/  \__/
      ▀█ ███ ▄▄▄▄▄ ███ █▀     /  \__/  \__/  \__/  \__/  \__/  \__/  
         ▀█▌▐█████▌▐█▀        \__/  \__/  \__/  \__/  \__/  \__/  \__/
            ███████        \__/  \__/  \__/  \__/  \__/  \__/  \__/  
"""
"""
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_

"""
def clearScreen():

	if os.name == 'posix':
		os.system('clear')
	else:
		os.system('cls')

def welcomeScreen():
	
	clearScreen()

	print asciiArt


def countDomainLevel(alamatURL):

	intDomainDepth = alamatURL.count('/') - 2*alamatURL.count('//')

	return intDomainDepth



def getDomainParts(alamatURL):

	parts = alamatURL.split('//')

	protocol = parts [0]

	arrDomainParts = parts[1].split('/', countDomainLevel(alamatURL))

	return protocol, arrDomainParts
	


def nLevelDomain(alamatURL, n):

	protocol, arrDomainParts = getDomainParts(alamatURL)

	urlnLevelDomain = ""

	for i in range (0, n):

		urlnLevelDomain = urlnLevelDomain + arrDomainParts[i]+"/"

	urlnLevelDomain = protocol + "//" + urlnLevelDomain

	return urlnLevelDomain



def getQueryContent(alamatURL, strQuery):
	
	parsed = urlparse.urlparse(alamatURL)
	QueryContent = str(urlparse.parse_qs(parsed.query)[strQuery][0])
	return QueryContent



def cleanUpHTML(strHTML):

	URLdomain = nLevelDomain(alamatURL, 1)
	URLdomain2 = nLevelDomain(alamatURL, 2)
	
	# fixing broken HTML
	strHTML = strHTML.replace('</tr><td>',"</tr><tr><td>")
	strHTML = strHTML.replace('</td></tr><td>','</td></tr><tr><td>')
	strHTML = strHTML.replace('<table class=fancy>','</td></tr></table><table class=fancy>')
	strHTML = strHTML.replace('</th>\n</tr>',"</th></tr><tr>")
	strHTML = strHTML.replace('</tr>\n\n<td>',"</tr><tr><td>")


	strHTML = strHTML.replace(' bgcolor>', '>')
	strHTML = strHTML.replace('<table class=fancy>','</td></tr></table><table class=fancy>')


	# translating relative to absolute reference
	strHTML = strHTML.replace('@import "/','@import "'+URLdomain)
	strHTML = strHTML.replace('href="/','href="'+URLdomain)
	strHTML = strHTML.replace("href='/","href='"+URLdomain)
	strHTML = strHTML.replace("href='./",'href="'+URLdomain)
	strHTML = strHTML.replace("href='../","href='"+URLdomain2)

	return strHTML
	


def fetchHTML(alamatURL):
	# fungsi ini hanya untuk mengambil stream string HTML dari alamat URL yang akan dimonitor
	# Content-Type utf-8 raises an error when meets strange character
	#print "fetching HTML from URL...\n", alamatURL

	strHTML = urllib2.urlopen(urllib2.Request(alamatURL, headers={ 'User-Agent': 'Mozilla/5.0' })).read()

	strHTML = strHTML.decode("windows-1252")

	strHTML = strHTML.encode('ascii', 'ignore')

	strHTML = cleanUpHTML(strHTML)

	mysoup = BeautifulSoup(strHTML)
	
	#print ">> URL fetched."

	return strHTML



def getTableList(strHTML):

	#print "\ngetting Table List...\n"

	mysoup = BeautifulSoup(strHTML)

	arrTable = mysoup.findAll('table')

	#print "there are:", len(arrTable), "tables."

	return arrTable



def getStyleList(strHTML):

	#print "\ngetting Style List...\n"

	mysoup = BeautifulSoup(strHTML)

	arrStyle = mysoup.findAll('link', rel = "stylesheet" )

	strStyle = ""

	for i in range (0, len(arrStyle)):

		strStyle = strStyle + str(arrStyle[i])
	
	return strStyle



def getHeading(strHTML):

	#print "\ngetting Heading...\n"

	strHTML = cleanUpHTML(strHTML)

	mysoup = BeautifulSoup(strHTML)

	heading1 = mysoup.findAll('h1')

	if heading1 != []:

		strHeading = heading1[0].getText().upper()
		strHeading = strHeading.replace("BY REGION", RegionName)


	heading3 = mysoup.findAll('h3')

	if heading3 != []:

		strHeading = heading3[0].getText().upper()
		strHeading = strHeading.replace("REGION: "+RegionName+" - ", "")
		strHeading = strHeading.replace("FOR REGION", "")



	else:
		strHeading = 'AVAILABILITY ATM BRI ' + RegionName
	

	#
	strHeading = strHeading.replace("LIST OF", "")

	# avoid semicolon, slash and double space by deleting them
	strHeading = strHeading.replace(":", "")
	strHeading = strHeading.replace("/", " ")
	strHeading = strHeading.replace("  ", " ")

	return strHeading.strip()



def getLargestTable(arrTable):

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

	table = largest_table

	#if table:
		#print ">> the largest from table list is chosen."

	return table



def getWidestTable(arrTable):

	# pilihlah tabel yang terbesar yang memiliki jumlah baris terbanyak

	widest_table = None

	max_cols = 0

	for table in arrTable:

		# cek satu per satu jumlah baris yang ada pada masing-masing tabel dalam array kumpulan tabel
		# simpan dalam variabel bernama numRows

		numCols = len(table.contents[1])
		
		# jika jumlah baris pada suatu tabel lebih besar daripada '0' maka jadikan sebagai max_rows sementara
		# proses ini diulangi terus menerus maka max_rows akan berisi jumlah baris terbanyak

		if numCols > max_cols:
			
		        widest_table = table
			max_cols = numCols

	# ini hanya mengembalikan penyebutan 'tabel terbesar' hanya sebagai 'tabel'

	table = widest_table

	#if table:
		#print ">> the widest from table list is chosen."

	return table



def getColsNumber(table):

	# bagaimana cara menentukan berapa jumlah kolomnya?

	numCols = len(table.contents[1])
	
	return numCols



def getRowsNumber(table):

	# bagaimana cara menentukan berapa jumlah kolomnya?

	numRows = len(table.findAll(lambda tag: tag.name == 'tr' and tag.findParent('table') == table))
	
	return numRows



def getRowsHeadNumber(table):

	# bagaimana cara menentukan berapa jumlah baris yang terpakai sebagai header?

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')
	numRows = len(table.findAll(lambda tag: tag.name == 'tr' and tag.findParent('table') == table))

	# inisialisasi variabel numRowsHead sebagai jumlah baris yang mengandung header

	numRowsHead = 0	
	
	# periksa satu per satu setiap baris

	for i in range (0, numRows):
		
		# apabila dalam suatu baris tertentu terdapat tag <th>
		if rows[i].findAll('th'):
			
			# maka numRows bertambah 1
			numRowsHead = i + 1


	# hasil akhir fungsi getTableDimension ini menghasilkan jumlah baris, jumlah baris yang terpakai header, jumlah kolom dan isi tabel itu sendiri

	return numRowsHead



def getTableDimension(table):
	
	numRows = getRowsNumber(table)
	numRowsHead = getRowsHeadNumber(table)
	numCols = getColsNumber(table)
	
	return numRows, numRowsHead, numCols



def fileCreate(strNamaFile, strData):
	f = open(strNamaFile, "w")
	f.writelines(str(strData))
	f.close()


    
def fileAppend(strNamaFile, strData):
	f = open(strNamaFile, "a")
	f.writelines(str(strData))
	f.close()



def getTableHeader(table):

	numRowsHead = getRowsHeadNumber(table)

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr', limit=numRowsHead)
	strHTMLTableHeader = ""
	
	for i in range (0, numRowsHead):

		strHTMLTableHeader = strHTMLTableHeader + str(rows[i])
	
	return strHTMLTableHeader



def getSpecificRows(table, rowIndex):

	#print "Let's take a look at the specific rows of index", rowIndex

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')
	strHTMLTableRows = ""

	for i in range (rowIndex, rowIndex+1):

		strHTMLTableRows = str(rows[i])
	
	return strHTMLTableRows



def getTableContents(table):

	numRows = getRowsNumber(table)
	numRowsHead = getRowsHeadNumber(table)

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')
	strHTMLTableContents = ""

	for i in range (numRowsHead, numRows):

		strHTMLTableContents = strHTMLTableContents + str(rows[i])
	
	return strHTMLTableContents



def getRowIndex(table, strSearchKey):

	# fungsi ini untuk mendapatkan nomor indeks baris yang mengandung satu kata kunci

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')
	
	numRows = len(table.findAll(lambda tag: tag.name == 'tr' and tag.findParent('table') == table))

	rowIndex = 0

	for i in range (0, numRows):

		trs = BeautifulSoup(str(rows[i]))
		tdcells = trs.findAll("td")
			
		for j in range (0, len(tdcells)):

			if tdcells[j].getText().upper() == strSearchKey.upper():
				
				rowIndex = i

				print "we got the index = ", rowIndex, "from ", numRows, "for search key ='"+strSearchKey+"'"
	return rowIndex


def getNamaFile(strHTML):

	strHeading = getHeading(strHTML)

	protocol, arrDomainParts = getDomainParts(alamatURL) 

	namaSkrip = arrDomainParts[-1].split('?')[0].replace('.pl','')

	strNamaFile = strHeading + "-" + namaSkrip +".html"

	strNamaFile = prepareDirectory('OUTPUT') + strNamaFile

	return strNamaFile



def prepareFile(strNamaFile):

	#print "preparing HTML file as canvas...", strNamaFile, "\n"

	strHTML = fetchHTML(alamatURL)


	strData = '<HTML><HEAD><TITLE>MONITORING ATM '+ RegionName +'</TITLE><META HTTP-EQUIV="REFRESH" CONTENT="3600">' + getStyleList(strHTML) + '</HEAD><body>'

	strData = strData + "<h1>"+ getHeading(strHTML) + "</h1><h3>per tanggal " + time.strftime("%d.%m.%Y jam %H:%M:%S") + "</h3>"

   	fileCreate(strNamaFile, strData)


def prepareTextFile(strNamaFile, strData):

	#print "preparing Text file...\n"

	strNamaFile = prepareDirectory('OUTPUT') + strNamaFile

	fileCreate(strNamaFile, strData)

	return strNamaFile




def getHTMLnWritefromURLList(strNamaFile, arrURL):

	strHTML = ""

	strHTML = '<div id="content"><table class="tabel2">'

	fileAppend(strNamaFile, strHTML)
	
	strHTMLTableContents = ""

	for i in range (0, 1):

		alamatURL = arrURL[i]

		arrTable = getTableList(fetchHTML(alamatURL))

		table = getLargestTable(arrTable)

		strHTMLTableContents = strHTMLTableContents + getTableContents(table)
		
	strHTML = getTableHeader(table) + strHTMLTableContents	

	fileAppend(strNamaFile, strHTML)	

		
	for i in range (1, len(arrURL)):

		alamatURL = arrURL[i]

		arrTable = getTableList(fetchHTML(alamatURL))

		table = getLargestTable(arrTable)

		strHTMLTableContents = getTableContents(table)

		fileAppend(strNamaFile, strHTMLTableContents)

	strHTML = '</table></div>'

	fileAppend(strNamaFile, strHTML)

	###
	
	#print "\a\n>>>>FILE CREATED :\n", strNamaFile, "<<<<\a\n"

	### TODO: play a beep sound
		


def ExtractLinksToFile(alamatURL):

	strHTML = fetchHTML(alamatURL)
	
	strNamaFile = getNamaFile(strHTML) 

	prepareFile(strNamaFile)

	arrTable = getTableList(strHTML)

	table = getLargestTable(arrTable)

	arrURL = [alamatURL]

	getHTMLnWritefromURLList(strNamaFile, arrURL)



def extractURL(strHTML):

	# this function finds all non-'0" links
	# nLevelDomain(alamatURL, 3)  --> http://172.18.65.42/monitorATM/dashboardNew/

	URLdomain = nLevelDomain(alamatURL, 0) 

	mysoup = BeautifulSoup(strHTML)

	arrURL = mysoup.findAll('a')

	numZeros = 0

	indexZero = [None]

	for i in range(0, len(arrURL)):

		if arrURL[i].getText() == "0":
			
			numZeros = numZeros + 1
			indexZero.append(i)

		else:

			arrURL[i] = arrURL[i].get('href')
		
	#print "We have", len(arrURL), "URLs."

	if numZeros:

		indexZero.remove(None)

		#print "There are", numZeros, "URLs containing zero at index:", indexZero

		for i in range (0, len(indexZero)):

			# there is a shift of index after every removal of list components

			arrURL.remove(arrURL[indexZero[i]-i])


		#print "So, we have remaining", len(arrURL), "URLs to fetch."

	return arrURL



def prepareDirectory(strOutputDir):
	# siapkan struktur direktori untuk penyimpanan data
	# struktur direktori adalah ['OUTPUT', 'ATM', '2015', '04-APR', 'DAY-28'] makes './OUTPUT/ATM/2015/04-APR/DAY-28'

	arrDirectoryStructure = [strOutputDir, 'LAS', time.strftime("%Y"), time.strftime("%m-%b").upper() , "DAY-"+time.strftime("%d")]

	fullPath = scriptDirectory

	for i in range (0, len(arrDirectoryStructure)):
	
		fullPath = fullPath + arrDirectoryStructure[i] + "/"

		if not os.path.exists(fullPath):

			#print "creating directories:", arrDirectoryStructure[i]
			os.mkdir(fullPath)
			os.chdir(fullPath)

	#print fullPath

	return fullPath

def readBranchCode():

	arrBranchCode = []
	arrBranchName = []

	fName = scriptDirectory +"conf/branchCode.888"
		
	f = open(fName)

	for baris in f.readlines():

		col = baris.strip().split("|")
		arrBranchCode.append(col[0])
		arrBranchName.append(col[1])


	f.close()

	return arrBranchCode, arrBranchName

def getBranchCode(alamatURL):

	strHTML = fetchHTML(alamatURL)

	table = getWidestTable(getTableList(strHTML))

	soup = BeautifulSoup(str(table))
	
	rows = soup.findAll('tr')

	numRows = getRowsNumber(table)

	numRowsHead = getRowsHeadNumber(table)

	if numRows == numRowsHead:

		#print "waiting the page to show data"
		#time.sleep(60)
		arrBranchCode, arrBranchName = readBranchCode()

		

	arrBranchCode = [None]*numRows
	arrBranchName = [None]*numRows

	for i in range (numRowsHead, numRows):

		trs = BeautifulSoup(str(rows[i]))
		tdcells = trs.findAll("td")

		try:

			if tdcells[1].getText().isdigit():

				arrBranchCode[i] = tdcells[1].getText()
				arrBranchName[i] = tdcells[2].getText().upper()
				#createfile

		except:
			print "tidak ada data"

	try:	
	# remove unnecessary items containing None in the 1st, 2nd and the last
		arrBranchCode.remove(arrBranchCode[0])
		arrBranchCode.remove(arrBranchCode[0])
		arrBranchCode.remove(arrBranchCode[-1])

		arrBranchName.remove(arrBranchName[0])
		arrBranchName.remove(arrBranchName[0])
		arrBranchName.remove(arrBranchName[-1])

	except IndexError:
		pass
		

	return arrBranchCode, arrBranchName

def getBranchURL(arrBranchCode):

	arrBranchURL=[None] * len(arrBranchCode)

	for i in range(0, len(arrBranchCode)):
		
		arrBranchURL[i] = "http://172.18.65.42/statusatm/viewbybranch6.pl?AREA_ID="+arrBranchCode[i]

		#print arrBranchURL[i]
	
	return arrBranchURL

def getBranchPage(alamatURL):
	
	try:
		strHTML = fetchHTML(alamatURL)

		table = getWidestTable(getTableList(strHTML))
	except:
		table = getBranchPage(alamatURL)

	return table

#-------------------------------------------------------


#-------------------------------------------------------
def getLASOFFStats(table, branchCode):

	#print "getting List of ATMs requires attention..."
	
	soup = BeautifulSoup(str(table))
	
	rows = soup.findAll('tr')

	numRows = getRowsNumber(table)

	numRowsHead = getRowsHeadNumber(table)

	msgBody = ""

	numOFF = 0
	arrOFF = []



	for i in range (numRowsHead, numRows):

		trs = BeautifulSoup(str(rows[i]))
		tdcells = trs.findAll("td")

#----------- OFF

		if tdcells[8].getText() == branchCode:

			numOFF = numOFF + 1

			pid = tdcells[1].getText()
			username = tdcells[4].getText()


			arrOFF.append(str(numOFF) + ") " + pid + " " + username )

	if numOFF:

		#msgBody = msgBody + "\n[PROBLEM LAS OFFLINE]\n"

		msgBody = msgBody + "\nOFFLINE: "+str(numOFF) + "\n" + "\n".join(arrOFF) + "\n"

	if msgBody:

		msgBody = msgBody
	else:

		msgBody = "\nNO OFFLINE...\n"

	return msgBody


def getLASNOPStats(table, branchCode):

	#print "getting List of ATMs requires attention..."
	
	soup = BeautifulSoup(str(table))
	
	rows = soup.findAll('tr')

	numRows = getRowsNumber(table)

	numRowsHead = getRowsHeadNumber(table)

	msgBody = ""

	numOFF = 0
	arrOFF = []



	for i in range (numRowsHead, numRows):

		trs = BeautifulSoup(str(rows[i]))
		tdcells = trs.findAll("td")

#----------- OFF

		if tdcells[8].getText() == branchCode:

			numOFF = numOFF + 1

			pid = tdcells[1].getText()
			username = tdcells[4].getText()


			arrOFF.append(str(numOFF) + ") " + pid + " " + username )

	if numOFF:

		#msgBody = msgBody + "\n[PROBLEM LAS OFFLINE]\n"

		msgBody = msgBody + "\nTIDAK DIPAKAI: "+str(numOFF) + "\n" + "\n".join(arrOFF) + "\n"

	if msgBody:

		msgBody = msgBody
	else:

		msgBody = "ALL USED..."

	return msgBody




def TelegramCLISender(telegramName, strNamaFile):

	telegramCommand = 'echo "send_text '+telegramName+' '+strNamaFile+'" | nc 127.0.0.1 8885'
	telegramCommand = 'proxychains telegram-cli -W -e "send_text '+telegramName+' '+strNamaFile+'"'
	print telegramCommand + "\n"
	os.system(telegramCommand)
	
	#telegramName = 'Jansen_Simanullang'
	#os.system('echo "send_text Jansen_Simanullang '+strNamaFile+'" | nc 127.0.0.1 888')
	#TelegramCLISender(telegramName, strNamaFile)



def TelegramBotSender(chat_id, strText):

	secretKey = "115651882:AAGDNzHXwLKNqOWmHWC8vMXg-Vy_fZD0350"

	encText=urllib.quote_plus(strText)

	strURL = "https://api.telegram.org/bot"+secretKey+"/sendMessage?chat_id="+chat_id+"&text="+urllib.quote_plus(strText)

	os.system('proxychains w3m -dump "'+ strURL+'"')





def readTextFile(strNamaFile):

	fText = open(strNamaFile)

	strText = ""
					
	for baris in fText.readlines():

		strText += baris

	fText.close()

	return strText



def prepareMessage(alamatURL, branchCode):

	msgBody = ""
	table = ""

	try:

		table = getBranchPage(alamatURL)

		msgBody = getLASOFFStats(getBranchPage(alamatURL), branchCode)


		#print "@@@@@@@@@@@\n"+msgBody+"@@@@@@@@@@@"

		

	except IndexError:
		
		print "site data not yet ready, sleeping for one minute..."

		time.sleep(60)

		msgBody = prepareMessage(alamatURL, branchCode)


	return msgBody



def NotifikasiLAS():

	global alamatURL, strHTML, RegionName, table, arrBranchCode

	alamatURL = firstURL

	strHTML = fetchHTML(firstURL)

	table = getWidestTable(getTableList(strHTML))

	strHTMLTableRows = getSpecificRows(table, getRowIndex(table, RegionName))

	arrURL = extractURL(strHTMLTableRows)
	
	alamatURLOFF = arrURL[2] 	# dapatkan dashboard OFFLINE
	alamatURLNOP = arrURL[5] 	# dapatkan dashboard OFFLINE

	#print alamatURL #--> alamat URL se-Kanwil yang diinginkan
		
	#arrBranchCode, arrBranchName = getBranchCode(alamatURL)

	#arrBranchURL = getBranchURL(arrBranchCode)

	print "Mengirimkan notifikasi "

	arrBranchCode, arrBranchName = readBranchCode()

	for i in range(0, 37):

		#msgSubject = "NOTIFIKASI LASS OFFLINE "+arrBranchName[i] +" ("+ arrBranchCode[i] +")\n"+time.strftime("%d.%m.%Y-%H:%M")

		#percentAvail = getAvailBranch(arrBranchCode[i])

		#strColor = colorPercent(float(percentAvail))

		#availText = "------------------------------------\nAvailability = " + percentAvail +"% -- "+ strColor

		#msgBody = msgSubject +"\n"+ availText +"\n"+ str(prepareMessage(arrBranchURL[i]))

		#print msgBody
		

		#msgBody = "TEST" + arrBranchName[i]
		msgBody = "NOTIFIKASI LAS RITEL " + arrBranchName[i] +" (" +arrBranchCode[i] + ")\nper " + time.strftime("%d.%m.%Y-%H:%M") +"\n------------------------------------\n"
		msgBody += getLASOFFStats(getBranchPage(alamatURLOFF), arrBranchCode[i])
		msgBody += getLASNOPStats(getBranchPage(alamatURLNOP), arrBranchCode[i])
		# create text file in the output folder
		#strNamaFile = ""

		strData = msgBody

		strNamaFile = prepareTextFile(arrBranchCode[i], strData)

		fName = scriptDirectory +"conf/LASRecipients.888"
		
		f = open(fName)

		for baris in f.readlines():

			col = baris.strip().split("|")

			if arrBranchCode[i] in col[0]:

				telegramName = str(col[2]).replace(" ","_")

				try:

					# sending using @jak3bot
					chat_id = str(col[1]).replace("#","")

					strText = readTextFile(strNamaFile)

					print "\n--------------------------------------------------\n"



					print arrBranchName[i]+"--->: "+ telegramName + "            \r"
					#print readTextFile(strNamaFile)

					TelegramBotSender(chat_id, strText)

					#print "CHAT ID = "+chat_id+ " TELEGRAM NAME = "+telegramName


				except Exception as inst:

					print inst

					# sending using "Kanwil Jakarta III"

					TelegramCLISender(telegramName, strNamaFile)

		f.close()

clearScreen()
welcomeScreen()
NotifikasiLAS()
