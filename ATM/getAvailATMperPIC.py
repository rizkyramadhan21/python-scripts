# -*- coding: utf-8 -*-
#!/usr/bin/python
#---------------------------------------
# getRekapATMperPIC.py
# (c) Jansen A. Simanullang, 
# 26.01.2016 17:55:45
# 27.01.2016 13:42:38
# 29.01.2016 19:48:47
# 12.02.2016 12:54
# to be used with PICATM.csv
#---------------------------------------
# usage:
# getRekapATMperPIC
#---------------------------------------
from __future__ import division
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
import os, sys, time, urlparse, smtplib, pdfkit


from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage

atmproIP = "172.18.65.42"
################################################################################################
firstURL='http://'+atmproIP+'/statusatm/dashboard_3.pl?ERROR=CLOSE_ST'
RegionName = "JAKARTA III"
################################################################################################
print "AVAILABILITY, OOS, OFF, NOP dan PROB OPS ATM\nPER PIC KANWIL JAKARTA III" +"\nposisi "+ time.strftime("%d-%m-%Y pukul %H:%M") + "\n"

scriptDirectory = os.path.dirname(os.path.abspath(__file__)) + "/"

asciiArt="""
	   ▄▄▄▄▄▄▄▄▄
        ▄█████████████▄ 
█████  █████████████████  █████
▐████▌ ▀███▄       ▄███▀ ▐████▌
 █████▄  ▀███▄   ▄███▀  ▄█████
 ▐██▀███▄  ▀███▄███▀  ▄███▀██▌    
  ███▄▀███▄  ▀█ █▀  ▄███▀▄███ 
  ▐█▄▀█▄▀███ ▄▄ ▄▄ ███▀▄█▀▄█▌
   ███▄▀█▄██ ██ ██ ██▄█▀▄███
    ▀███▄▀██ ██ ██ ██▀▄███▀
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
 █████▄  ▀███▄   ▄███▀  ▄█████    NOTIFIKASI ATM via TELEGRAM
"""

asciiArt = asciiArt +" ▐██▀███▄  ▀███▄███▀  ▄███▀██▌    "+RegionName
asciiArt = asciiArt +"""
  ███▄▀███▄  ▀███▀  ▄███▀▄███     
  ▐█▄▀█▄▀███ ▄▀ ▀▄ ███▀▄█▀▄█▌     (c) JANSEN SIMANULLANG
   ███▄▀█▄██ ██ ██ ██▄█▀▄███      MEI 2015
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
	strHTML = urlopen(alamatURL).read()

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

	print "\ngetting Heading...\n"

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

				#print "we got the index = ", rowIndex, "from ", numRows, "for search key ='"+strSearchKey+"'"
	return rowIndex



def getATMProbUKOCRO(table):

	try:

		#print "getting List of ATMs requires attention..."
	
		soup = BeautifulSoup(str(table))
	
		rows = soup.findAll('tr')

		numRows = getRowsNumber(table)

		numRowsHead = getRowsHeadNumber(table)

		numProbUKO = 0
		numProbCRO = 0

		for i in range (numRowsHead, numRows):

			trs = BeautifulSoup(str(rows[i]))
			tdcells = trs.findAll("td")

			if "ATM CENTER" in tdcells[6].getText():

				numProbCRO = numProbCRO + 1

		numProbUKO = numRows - numProbCRO -numRowsHead

		#print "number of CRO problem(s)", numProbCRO, "number of UKO problem(s):", numProbUKO

	except IndexError:

		numProbUKO, numProbCRO = getATMProbUKOCRO(table)

	except RuntimeError:

		numProbUKO, numProbCRO = "0","0"


	return int(numProbUKO), int(numProbCRO)



def getATMProbUKOCRO2(table):

	try:

		#print "getting List of ATMs requires attention..."
	
		soup = BeautifulSoup(str(table))
	
		rows = soup.findAll('tr')

		numRows = getRowsNumber(table)

		numRowsHead = getRowsHeadNumber(table)

		numProbUKO = 0
		numProbCRO = 0

		for i in range (numRowsHead, numRows):

			trs = BeautifulSoup(str(rows[i]))
			tdcells = trs.findAll("td")

			if "ATM CENTER" in tdcells[8].getText():

				numProbCRO = numProbCRO + 1

		numProbUKO = numRows - numProbCRO -numRowsHead

		#print "number of CRO problem(s)", numProbCRO, "number of UKO problem(s):", numProbUKO

	except IndexError:

		numProbUKO, numProbCRO = getATMProbUKOCRO(table)

	except RuntimeError:

		numProbUKO, numProbCRO = "0","0"


	return int(numProbUKO), int(numProbCRO)



def getATMProbUKOCRO3(table):
	
	try:

		#print "getting List of ATMs requires attention..."
	
		soup = BeautifulSoup(str(table))
	
		rows = soup.findAll('tr')

		numRows = getRowsNumber(table)

		numRowsHead = getRowsHeadNumber(table)

		numProbUKO = 0
		numProbCRO = 0

		for i in range (numRowsHead, numRows):

			trs = BeautifulSoup(str(rows[i]))
			tdcells = trs.findAll("td")

			if "ATM CENTER" in tdcells[7].getText():

				numProbCRO = numProbCRO + 1

		numProbUKO = numRows - numProbCRO -numRowsHead

		#print "number of CRO problem(s)", numProbCRO, "number of UKO problem(s):", numProbUKO

	except IndexError:

		numProbUKO, numProbCRO = getATMProbUKOCRO(table)

	except RuntimeError:

		numProbUKO, numProbCRO = "0","0"


	return int(numProbUKO), int(numProbCRO)



def makeAvailabilityDict(table):

	dictAvailability = {}

	try:
		#percentAvail = "0"
		#print "getting List of ATMs requires attention..."
	
		soup = BeautifulSoup(str(table))
	
		rows = soup.findAll('tr')

		numRows = getRowsNumber(table)

		numRowsHead = getRowsHeadNumber(table)
		
		#print "numRowsHead", numRowsHead, numRows


		for i in range (numRowsHead-1, numRows-1):

			trs = BeautifulSoup(str(rows[i]))

			tdcells = trs.findAll("td")

			if tdcells:		

				BranchCode = tdcells[1].getText()
				BranchAvail = str(tdcells[24].getText()).strip()

				if BranchAvail == "":
					BranchAvail = "0.0"

				dictAvailability[BranchCode] = BranchAvail


	except:

		#print "ada kesalahan"

		dictAvailability = makeAvailabilityDict(table)

	return dictAvailability



def makeStatusDict(table, strStatusofInterest):

	dictStatus = {}

	if strStatusofInterest == "OOS":

		ColumnofInterest = 12

	if strStatusofInterest == "OFF":

		ColumnofInterest = 13

	if strStatusofInterest == "NOP G":

		ColumnofInterest = 4

	if strStatusofInterest == "NOP NG":

		ColumnofInterest = 5

	if strStatusofInterest == "PROB OPS":

		ColumnofInterest = 8

	if strStatusofInterest == "AVAILABILITY":

		ColumnofInterest = 24

	try:
		#percentAvail = "0"
		#print "getting List of ATMs requires attention..."
	
		soup = BeautifulSoup(str(table))
	
		rows = soup.findAll('tr')

		numRows = getRowsNumber(table)

		numRowsHead = getRowsHeadNumber(table)
		
		#print "numRowsHead", numRowsHead, numRows


		for i in range (numRowsHead-1, numRows-1):

			trs = BeautifulSoup(str(rows[i]))

			tdcells = trs.findAll("td")

			if tdcells:		

				BranchCode = tdcells[1].getText()
				BranchStatus = str(tdcells[ColumnofInterest].getText()).strip()

				if BranchStatus == "":
					BranchStatus = 0

				dictStatus[BranchCode] = BranchStatus


	except:

		#print "ada kesalahan"

		dictStatus = makeStatusDict(table, strStatusofInterest)

	return dictStatus




def colorPercent(percentAvail):

	strColor = str(percentAvail)

	if percentAvail >= 0.00:
		strColor = "Merah"
	if percentAvail >= 87.00:
		strColor = "Kuning"
	if percentAvail >= 93.00:
		strColor = "Hijau Muda"
	if percentAvail >= 97.00:
		strColor = "Hijau Tua"


	return strColor


def findValuebyKey(dictObj, strKey):
	value = ""
	#print locals()
	#print type(dictObj)
	#print dictObj.items()
	for k, v in dictObj.items():

		k = k.encode('ascii','ignore')
		strKey = strKey.strip()
		#print k, strKey, type(k), type(strKey), k == strKey.strip()
		if k == strKey:
			#print "okay"
			value = value + str(v)

	return value

alamatURL = 'http://'+atmproIP+'/statusatm/dashboard_cabang.pl?REGID=15&REGNAME=Jakarta%20III'
table = getLargestTable(getTableList(fetchHTML(alamatURL)))

#percentAvail = makeAvailabilityDict(table, "0071")

#print percentAvail, colorPercent(percentAvail)

# desain output
# REKAP PER PIC
# -------------------
# PIC 1
# Kanca A 100.0
# Kanca B 100.0
# Kanca C 100.0
# Kanca D 100.0
# Kanca E 100.0
# AVG = 100.0 Hijau Tua
# -------------------
# -------------------
# -------------------
# -------------------
# PIC 5
# Kanca V 100.0
# Kanca W 100.0
# Kanca X 100.0
# Kanca Y 100.0
# Kanca Z 100.0
# AVG = 100.0 Hijau Tua
# -------------------
# -------------------

def readPICNames():

	fName = scriptDirectory + "conf/PICNames.csv"

	arrPICs = [""]

	f = open(fName)

	for baris in f.readlines():

		col = baris.strip().split(",")
		
		PICName = col[1]
				
		arrPICs.append(PICName)
		
				
	f.close()

	arrPICs.remove(arrPICs[0])

	return arrPICs

arrPICs = readPICNames()
numPICs = len(arrPICs)



def MsgBodyRekapPICATM():

	alamatURL = 'http://'+atmproIP+'/statusatm/dashboard_cabang.pl?REGID=15&REGNAME=Jakarta%20III'
	table = getLargestTable(getTableList(fetchHTML(alamatURL)))

	dictAvailability = makeStatusDict(table, "AVAILABILITY")
	dictOOS = makeStatusDict(table, "OOS")
	dictOFF = makeStatusDict(table, "OFF")
	dictNOPG = makeStatusDict(table, "NOP G")
	dictNOPNG = makeStatusDict(table, "NOP NG")
	dictPROBOPS = makeStatusDict(table, "PROB OPS")
	
	fName = scriptDirectory + "conf/PICATM.csv"

	#BranchAvail = ""
	count = 0
	BranchAvailSum = 0.0

	SumPerPic = [0.0] * (numPICs+1)
	countPerPic = [0] * (numPICs+1)
	avgPerPic = [0.0] * (numPICs+1)

	sumOOSPerPic = [0] * (numPICs+1)
	sumOFFPerPic = [0] * (numPICs+1)
	sumNOPGPerPic = [0] * (numPICs+1)
	sumNOPNGPerPic = [0] * (numPICs+1)
	sumPROBOPSPerPic = [0] * (numPICs+1)

	f = open(fName)

	for baris in f.readlines():

		col = baris.strip().split(",")
		
		for i in range (0, numPICs+1):
			
			if str(i) == col[0].strip():
				
				BranchCode = col[1]
				BranchName = str(col[2])
				
				BranchAvail = findValuebyKey(dictAvailability, BranchCode)

				BranchOOS = findValuebyKey(dictOOS, BranchCode)
				BranchOFF = findValuebyKey(dictOFF, BranchCode)
				BranchNOPG = findValuebyKey(dictNOPG, BranchCode)
				BranchNOPNG = findValuebyKey(dictNOPNG, BranchCode)
				BranchPROBOPS = findValuebyKey(dictPROBOPS, BranchCode)

				#BranchAvailSum = float(BranchAvailSum) + float(BranchAvail)
				#print BranchAvail
				SumPerPic[i] = 	SumPerPic[i] + float(BranchAvail)
				countPerPic[i] = 	countPerPic[i] + 1

				sumOOSPerPic[i] = sumOOSPerPic[i] + int(BranchOOS)
				sumOFFPerPic[i] = sumOFFPerPic[i] + int(BranchOFF)
				sumNOPGPerPic[i] = sumNOPGPerPic[i] + int(BranchNOPG)
				sumNOPNGPerPic[i] = sumNOPNGPerPic[i] + int(BranchNOPNG)
				sumPROBOPSPerPic[i] = sumPROBOPSPerPic[i] + int(BranchPROBOPS)

				
				if countPerPic[i] == 1:
					print "------------------------\n" + str(i) +" - "+arrPICs[i-1].upper()+  "\n------------------------"
				print countPerPic[i], BranchName, BranchAvail, "(" + str(BranchOOS) + "," + str(BranchOFF)+"," + str(int(BranchNOPG)+int(BranchNOPNG)) + "," + str(BranchPROBOPS) + ")"

	avgPerPic.remove(avgPerPic[0])
	countPerPic.remove(avgPerPic[0])
	SumPerPic.remove(SumPerPic[0])

	sumOOSPerPic.remove(sumOOSPerPic[0])
	sumOFFPerPic.remove(sumOFFPerPic[0])
	sumNOPGPerPic.remove(sumNOPGPerPic[0])
	sumNOPNGPerPic.remove(sumNOPNGPerPic[0])
	sumPROBOPSPerPic.remove(sumPROBOPSPerPic[0])
	

	f.close()				
	
	print "------------------------\nAVAILABILITY, OOS, OFF, NOP dan PROB OPS ATM\nPER PIC KANWIL JAKARTA III" +"\nposisi "+ time.strftime("%d-%m-%Y pukul %H:%M") + "\n"

	for i in range (0, numPICs):
		
		avgPerPic[i] = SumPerPic[i] / countPerPic[i]
	
	for i in range (0, numPICs):

		print arrPICs[i].split(" ")[0]+" = ", '{0:.2f}'.format(avgPerPic[i]), "~",colorPercent(avgPerPic[i]) + " (" + str(sumOOSPerPic[i])+ "," + str(sumOFFPerPic[i])+ "," + str(sumNOPGPerPic[i] + sumNOPNGPerPic[i])+ "," + str(sumPROBOPSPerPic[i])+")"
		
	print "------------------------"





MsgBodyRekapPICATM()
