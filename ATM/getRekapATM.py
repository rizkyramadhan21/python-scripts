# -*- coding: utf-8 -*-
#!/usr/bin/python
### Jansen A. Simanullang
### 22.04.2015 18:36:34 getEDCUKONOPKanwil.py
### 07.08.2015 12:32:17
### 13.08.2015 14:27:48 added percent availability and color indicator name
### 30.12.2015 08:39 ProbOPS dan RSK
### AVG dan ALL 18:44
### 22.12.2016 AVG deleted, AVG == ALL, getProbOPS using getWidestTable

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
periodeMonitoring=3600*4
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




def getAvailability(table):

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

			percentAvail = tdcells[29].getText()
			colorCode = tdcells[8].getText()

	

	except IndexError:

		percentAvail = getAvailability(table)

	return percentAvail

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


totalATMUKOProblem = 0
totalATMCROProblem = 0

# CO1 
alamatURL = 'http://172.18.65.42/statusatm/viewbyregionprobco1.pl?REGID=15&ERROR=CSHOUT_ST_1'
table = getLargestTable(getTableList(fetchHTML(alamatURL)))
numProbUKO, numProbCRO = getATMProbUKOCRO(table)

COText1 = "CO1 = " + str(numProbUKO + numProbCRO) + " = "+ str(numProbUKO) + " + " +str(numProbCRO)



# CO2 
alamatURL = 'http://172.18.65.42/statusatm/viewbyregionprobco2.pl?REGID=15&ERROR=CSHOUT_ST_2'
table = getLargestTable(getTableList(fetchHTML(alamatURL)))
numProbUKO, numProbCRO = getATMProbUKOCRO(table)

COText2 = "CO2 = " + str(numProbUKO + numProbCRO) + " = "+ str(numProbUKO) + " + " +str(numProbCRO)



# CO3 
alamatURL = 'http://172.18.65.42/statusatm/viewbyregionprobco3.pl?REGID=15&ERROR=CSHOUT_ST_3'
table = getLargestTable(getTableList(fetchHTML(alamatURL)))
numProbUKO, numProbCRO = getATMProbUKOCRO(table)

COText3 = "CO3 = " + str(numProbUKO + numProbCRO) + " = "+ str(numProbUKO) + " + " +str(numProbCRO)



# CL 
alamatURL = 'http://172.18.65.42/statusatm/viewbyregionprob.pl?REGID=15&ERROR=CSHLOW_ST'
table = getLargestTable(getTableList(fetchHTML(alamatURL)))
numProbUKO, numProbCRO = getATMProbUKOCRO(table)

CLText = "CL = " + str(numProbUKO + numProbCRO) + " = "+ str(numProbUKO) + " + " +str(numProbCRO)



# DF1 
alamatURL = 'http://172.18.65.42/statusatm/viewbyregionprobdf1.pl?REGID=15&ERROR=DISP_ST'
table = getLargestTable(getTableList(fetchHTML(alamatURL)))
numProbUKO, numProbCRO = getATMProbUKOCRO(table)

DFText1 = "DF1 = " + str(numProbUKO + numProbCRO) + " = "+ str(numProbUKO) + " + " +str(numProbCRO)



# DF2 
alamatURL = 'http://172.18.65.42/statusatm/viewbyregionprobdf2.pl?REGID=15&ERROR=DISP_ST'
table = getLargestTable(getTableList(fetchHTML(alamatURL)))
numProbUKO, numProbCRO = getATMProbUKOCRO(table)

DFText2 = "DF2 = " + str(numProbUKO + numProbCRO) + " = "+ str(numProbUKO) + " + " +str(numProbCRO)



# DF3 
alamatURL = 'http://172.18.65.42/statusatm/viewbyregionprobdf3.pl?REGID=15&ERROR=DISP_ST'
table = getLargestTable(getTableList(fetchHTML(alamatURL)))
numProbUKO, numProbCRO = getATMProbUKOCRO(table)

DFText3 = "DF3 = " + str(numProbUKO + numProbCRO) + " = "+ str(numProbUKO) + " + " +str(numProbCRO)



# OOS GARANSI
alamatURL = 'http://172.18.65.42/statusatm/viewbyregionprobooscr.pl?REGID=15&ERROR=CLOSE_ST&gr=Y'
table = getLargestTable(getTableList(fetchHTML(alamatURL)))
numProbUKO1, numProbCRO1 = getATMProbUKOCRO(table)

totalATMUKOProblem += numProbUKO1
totalATMCROProblem += numProbCRO1

#print totalATMUKOProblem, totalATMCROProblem

# OOS NON GARANSI
alamatURL = 'http://172.18.65.42/statusatm/viewbyregionprobooscr.pl?REGID=15&ERROR=CLOSE_ST&gr=N'
table = getLargestTable(getTableList(fetchHTML(alamatURL)))
numProbUKO2, numProbCRO2 = getATMProbUKOCRO(table)


totalATMUKOProblem += numProbUKO2
totalATMCROProblem += numProbCRO2
#print totalATMUKOProblem, totalATMCROProblem

# TOTAL OOS
OOSText= "OOS = " + str(numProbUKO1 + numProbUKO2 + numProbCRO1 + numProbCRO2) + " = "+ str(numProbUKO1 + numProbUKO2) + " + " +str(numProbCRO1 + numProbCRO2)



# OFF
alamatURL = 'http://172.18.65.42/statusatm/viewbyoffline.pl?REGID=15&ERROR=DOWN_ST'
table = getLargestTable(getTableList(fetchHTML(alamatURL)))
numProbUKO, numProbCRO = getATMProbUKOCRO3(table)
OFFText = "OFF1 = " + str(numProbUKO + numProbCRO) + " = "+ str(numProbUKO) + " + " +str(numProbCRO)+ "  (<6 jam)"

totalATMUKOProblem += numProbUKO
totalATMCROProblem += numProbCRO
#print totalATMUKOProblem, totalATMCROProblem

# OFF2
alamatURL = 'http://172.18.65.42/statusatm/viewbyoffline2.pl?REGID=15&ERROR=DOWN_ST'
table = getLargestTable(getTableList(fetchHTML(alamatURL)))
numProbUKO, numProbCRO = getATMProbUKOCRO3(table)
OFFText += "\nOFF2 = " + str(numProbUKO + numProbCRO) + " = "+ str(numProbUKO) + " + " +str(numProbCRO) + "   (>= 6 jam)"

totalATMUKOProblem += numProbUKO
totalATMCROProblem += numProbCRO
#print totalATMUKOProblem, totalATMCROProblem


# NOP GARANSI
alamatURL = 'http://172.18.65.42/statusatm/viewbynop.pl?REGID=15&gr=Y'
table = getLargestTable(getTableList(fetchHTML(alamatURL)))
numProbUKO1, numProbCRO1 = getATMProbUKOCRO(table)

totalATMUKOProblem += numProbUKO1
totalATMCROProblem += numProbCRO1
#print totalATMUKOProblem, totalATMCROProblem


# NOP NON GARANSI
alamatURL = 'http://172.18.65.42/statusatm/viewbynop.pl?REGID=15&gr=N'
table = getLargestTable(getTableList(fetchHTML(alamatURL)))
numProbUKO2, numProbCRO2 = getATMProbUKOCRO(table)

totalATMUKOProblem += numProbUKO2
totalATMCROProblem += numProbCRO2
#print totalATMUKOProblem, totalATMCROProblem


# TOTAL NOP
NOPText= "NOP = " + str(numProbUKO1 + numProbUKO2 + numProbCRO1 + numProbCRO2) + " = "+ str(numProbUKO1 + numProbUKO2) + " + " +str(numProbCRO1 + numProbCRO2)

#-----------------------------------------------------------------
# RSK
alamatURL = 'http://172.18.65.42/statusatm/viewbyrsk.pl?REGID=15&gr=N'
table = getLargestTable(getTableList(fetchHTML(alamatURL)))
numProbUKO, numProbCRO = getATMProbUKOCRO(table)
RSKText = "RSK = " + str(numProbUKO + numProbCRO) + " = "+ str(numProbUKO) + " + " +str(numProbCRO)

#-----------------------------------------------------------------
# PROB OPS
alamatURL = 'http://172.18.65.42/statusatm/viewbyoldstagging.pl?REGID=15&gr=H'
table = getWidestTable(getTableList(fetchHTML(alamatURL)))
numProbUKO, numProbCRO = getATMProbUKOCRO(table)
ProbOPSText = "OPS = " + str(numProbUKO + numProbCRO) + " = "+ str(numProbUKO) + " + " +str(numProbCRO)

#-----------------------------------------------------------------
def getLargestTableProbOPS(arrTable):

	# pilihlah tabel yang terbesar yang memiliki jumlah baris terbanyak

	largest_table = None

	max_cols = 0

	for table in arrTable:

		# cek satu per satu jumlah baris yang ada pada masing-masing tabel dalam array kumpulan tabel
		# simpan dalam variabel bernama numRows

		numCols = len(table.findAll(lambda tag: tag.name == 'td' and tag.findParent('table') == table))
		
		# jika jumlah baris pada suatu tabel lebih besar daripada '0' maka jadikan sebagai max_rows sementara
		# proses ini diulangi terus menerus maka max_rows akan berisi jumlah baris terbanyak

		if numCols > max_cols:
			
			largest_table = table
			max_cols = numCols

	# ini hanya mengembalikan penyebutan 'tabel terbesar' hanya sebagai 'tabel'

	table = largest_table

	#if table:
		#print ">> the largest from table list is chosen."

	return table

#-----------------------------------------------------------------

def getATMTunaiNonTunai(table):

	try:

		#print "getting List of ATMs requires attention..."
	
		soup = BeautifulSoup(str(table))
	
		rows = soup.findAll('tr')

		numRows = getRowsNumber(table)

		numRowsHead = getRowsHeadNumber(table)

		numUPUKO = 0
		numUPCRO = 0

		for i in range (numRowsHead, numRows):

			trs = BeautifulSoup(str(rows[i]))
			tdcells = trs.findAll("td")

			if "ATM CENTER" in tdcells[5].getText():

				numUPCRO = numUPCRO + 1

		numUPUKO = numRows - numUPCRO -numRowsHead

		#print "number of CRO problem(s)", numProbCRO, "number of UKO problem(s):", numProbUKO

	except IndexError:

		numUPUKO, numUPCRO = getATMTunaiNonTunai(table)

	except RuntimeError:

		numUPUKO, numUPCRO = "0","0"


	return int(numUPUKO), int(numUPCRO)


def getSumATMTunaiNonTunai():

	totalUPUKO = 0
	totalUPCRO = 0

	alamatURL = "http://172.18.65.42/statusatm/viewbyuptunai.pl?REGID=15"
	table = getLargestTable(getTableList(fetchHTML(alamatURL)))
	TunaiUKO, TunaiCRO = getATMTunaiNonTunai(table)

	alamatURL = "http://172.18.65.42/statusatm/viewbyupnontunai.pl?REGID=15"
	table = getLargestTable(getTableList(fetchHTML(alamatURL)))
	nonTunaiUKO, nonTunaiCRO = getATMTunaiNonTunai(table)

	totalUPUKO = TunaiCRO + nonTunaiUKO 
	totalUPCRO = TunaiCRO + nonTunaiCRO

	return TunaiUKO, TunaiCRO, nonTunaiUKO, nonTunaiCRO

TunaiUKO, TunaiCRO, nonTunaiUKO, nonTunaiCRO = getSumATMTunaiNonTunai()

TunaiText = "TUNAI = " + str(TunaiUKO) + " + " +str(TunaiCRO)
nonTunaiText = "NON TUNAI = " + str(nonTunaiUKO) + " + " +str(nonTunaiCRO)

#-----------------------------------------------------------------

# Availability
upATMUKO = 629
upATMUKO = TunaiUKO + nonTunaiUKO
upATMCRO = 1473
upATMCRO = TunaiCRO + nonTunaiCRO

#print totalATMUKOProblem, totalATMCROProblem

percentAvailUKO = upATMUKO / (upATMUKO + totalATMUKOProblem)*100
percentAvailCRO = upATMCRO / (upATMCRO + totalATMCROProblem)*100

alamatURL = 'http://'+atmproIP+'/statusatm/dashboard_cabang.pl?REGID=15&REGNAME=Jakarta%20III'
table = getLargestTable(getTableList(fetchHTML(alamatURL)))

AvailText0 = "Availability"

percentAvailAll = (upATMUKO+ upATMCRO) / (upATMUKO+ upATMCRO + totalATMUKOProblem + totalATMCROProblem) *100
AvailText1 = "(ALL) = " + str("{0:.2f}".format(percentAvailAll)) +"% -- " + colorPercent(float(percentAvailAll))
AvailText2 = "(UKO) = " + str("{0:.2f}".format(percentAvailUKO)) +"% -- " + colorPercent(float(percentAvailUKO))
AvailText3 = "(CRO) = " + str("{0:.2f}".format(percentAvailCRO)) +"% -- " + colorPercent(float(percentAvailCRO))

msgBody = "----------------------------------------------------\n"
msgBody = msgBody + "REKAPITULASI ATM PRO "+RegionName + "\n"
msgBody = msgBody + "per "+ time.strftime("%d-%m-%Y pukul %H:%M") + "\n"
msgBody = msgBody + "----------------------------------------------------\n"
msgBody = msgBody + "Prob = UKO + CRO\n"
msgBody = msgBody + CLText + "\n"
msgBody = msgBody + COText1 + "   (<=5 hari)\n"
msgBody = msgBody + COText2 + "   (6-15 hari)\n"
msgBody = msgBody + COText3 + "   (> 16 hari)\n"
msgBody = msgBody + "----------------------------------------------------\n"
msgBody = msgBody + TunaiText + "\n"
msgBody = msgBody + nonTunaiText + "\n"
msgBody = msgBody + "----------------------------------------------------\n"
msgBody = msgBody + DFText1 + "   (<=5 hari)\n"
msgBody = msgBody + DFText2 + "   (6-15 hari)\n"
msgBody = msgBody + DFText3 + "   (> 16 hari)\n"
msgBody = msgBody + "----------------------------------------------------\n"
msgBody = msgBody + OOSText + "\n"
msgBody = msgBody + OFFText + "\n"
msgBody = msgBody + NOPText + "\n"
msgBody = msgBody + "----------------------------------------------------\n"
msgBody = msgBody + RSKText + "\n"
msgBody = msgBody + ProbOPSText + "\n"
msgBody = msgBody + "----------------------------------------------------\n"
msgBody = msgBody + AvailText0 + "\n"
msgBody = msgBody + AvailText1 + "\n"
msgBody = msgBody + AvailText2 + "\n"
msgBody = msgBody + AvailText3 + "\n"
msgBody = msgBody + "----------------------------------------------------\n"

print msgBody
