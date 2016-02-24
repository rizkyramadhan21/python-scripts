# -*- coding: utf-8 -*-
#!/usr/bin/python
#---------------------------------------
# getAvailEDCperPIC.py
# (c) Jansen A. Simanullang, 
# 26.01.2016 14:35:44 - 17:33:45
# 29.01.2016 19:43:40
# 12.02.2016 10:19 Unified genre
# PIC Names shown at the recap
# to be used with PICEDC.csv
# to be used as telegram-bot plugin
#---------------------------------------
# usage: 
# getAvailEDCperPIC [merchant/brilink/uko]
#---------------------------------------

from __future__ import division
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
import os, sys, time, urlparse, smtplib, pdfkit


from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage

atmproIP = "172.18.65.42"
#---------------------------------------
RegionName = "JAKARTA III"
#---------------------------------------
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
		strHeading = 'AVAILABILITY EDC BRI ' + RegionName
	

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







def makeAvailabilityDict(table, strGenre):

	#alamatURL = 'http://172.18.44.66/edcpro/index.php/main/kanwil_implementor?kanwil=Q'
	#table = getLargestTable(getTableList(fetchHTML(alamatURL)))
	dictAvailability = {}

	if strGenre.upper() == "MERCHANT":

		columnNumber = 9

	if strGenre.upper() == "BRILINK":

		columnNumber = 17

	if strGenre.upper() == "UKO":

		columnNumber = 25

	#print columnNumber

	try:
	
		soup = BeautifulSoup(str(table))
	
		rows = soup.findAll('tr')

		numRows = getRowsNumber(table)

		numRowsHead = getRowsHeadNumber(table)



		for i in range (3, numRows-3):

			trs = BeautifulSoup(str(rows[i]))

			tdcells = trs.findAll("td")

			if tdcells:		
				BranchCode = tdcells[0].getText().split("-")[0].strip()
				BranchAvail = float(tdcells[columnNumber].getText())
				#print BranchCode, BranchAvail
				dictAvailability[BranchCode] = BranchAvail

				#print dictAvailability[BranchCode]


		#print "dictAvailability", dictAvailability

	except:

		#print "ada kesalahan"

		dictAvailability = makeAvailabilityDict(table, strGenre)

	return dictAvailability


def makeNOPDict(table, strGenre):

	#alamatURL = 'http://172.18.44.66/edcpro/index.php/main/kanwil_implementor?kanwil=Q'
	#table = getLargestTable(getTableList(fetchHTML(alamatURL)))
	dictNOP = {}

	if strGenre.upper() == "MERCHANT":

		columnNumber = 7

	if strGenre.upper() == "BRILINK":

		columnNumber = 15

	if strGenre.upper() == "UKO":

		columnNumber = 23

	#print columnNumber

	try:
	
		soup = BeautifulSoup(str(table))
	
		rows = soup.findAll('tr')

		numRows = getRowsNumber(table)

		numRowsHead = getRowsHeadNumber(table)



		for i in range (3, numRows-3):

			trs = BeautifulSoup(str(rows[i]))

			tdcells = trs.findAll("td")

			if tdcells:		
				BranchCode = tdcells[0].getText().split("-")[0].strip()
				BranchNOP = int(tdcells[columnNumber].getText())
				#print BranchCode, BranchAvail
				dictNOP[BranchCode] = BranchNOP

				#print dictAvailability[BranchCode]


		#print "dictAvailability", dictAvailability

	except:

		print "ada kesalahan"

		dictNOP = makeNOPDict(table, strGenre)

	return dictNOP



def colorPercent(percentAvail):

	strColor = str(percentAvail)

	if percentAvail >= 0.00:
		strColor = "Merah"
	if percentAvail >= 60.00:
		strColor = "Kuning"
	if percentAvail >= 70.00:
		strColor = "Hijau Muda"
	if percentAvail >= 80.00:
		strColor = "Hijau Tua"


	return strColor


def findValuebyKey(dictObj, strKey):
	value = ""
	#print locals()
	#print type(dictObj)
	#print dictObj.items()
	#strKey = str(strKey)
	for k, v in dictObj.items():

		k = k.encode('ascii','ignore')
		strKey = strKey.strip()
		#print k, strKey, type(k), type(strKey), k == strKey.strip()
		if k == strKey:
			#print "okay"
			value = value + str(v)

	return value

alamatURL = 'http://172.18.44.66/edcpro/index.php/main/kanwil_implementor?kanwil=Q'
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

def MsgBodyRekapPICEDC(strGenre):

	alamatURL = 'http://172.18.44.66/edcpro/index.php/main/kanwil_implementor?kanwil=Q'
	table = getLargestTable(getTableList(fetchHTML(alamatURL)))

	dictAvailability = makeAvailabilityDict(table, strGenre)
	dictNOP = makeNOPDict(table, strGenre)

	fName = scriptDirectory + "conf/PICEDC.csv"

	#BranchAvail = ""
	count = 0
	BranchAvailSum = 0.0

	SumPerPic = [0.0] * (numPICs+1)
	countPerPic = [0] * (numPICs+1)
	NOPPerPic = [0] * (numPICs+1)
	avgPerPic = [0.0] * (numPICs+1)

	f = open(fName)

	for baris in f.readlines():

		col = baris.strip().split(",")
		
		for i in range (0, numPICs+1):
			
			if str(i) == col[0].strip():
				
				BranchCode = str(int(col[1]))
				BranchName = str(col[2])
				
				BranchAvail = findValuebyKey(dictAvailability, BranchCode)
				BranchNOP = findValuebyKey(dictNOP, BranchCode)

				SumPerPic[i] = 	SumPerPic[i] + float(BranchAvail)
				NOPPerPic[i] = 	NOPPerPic[i] + int(BranchNOP)
				countPerPic[i] = 	countPerPic[i] + 1
				
				if countPerPic[i] == 1:
					print "------------------------\n" + str(i) +" - "+arrPICs[i-1].upper()+  "\n------------------------"
				print countPerPic[i], BranchName, '{0:.2f}'.format(float(BranchAvail))+" ("+ BranchNOP+ ")"

	SumPerPic.remove(SumPerPic[0])
	NOPPerPic.remove(NOPPerPic[0])
	countPerPic.remove(countPerPic[0])
	avgPerPic.remove(avgPerPic[0])
	

	f.close()				

	print "------------------------\nAVERAGE AVAILABILITY dan JUMLAH NOP EDC "+strGenre.upper()+"\nPER PIC KANWIL JAKARTA III" +"\nposisi "+ time.strftime("%d-%m-%Y pukul %H:%M") + "\n"

	for i in range (0, numPICs):
		
		avgPerPic[i] = SumPerPic[i] / float(countPerPic[i])
	
	for i in range (0, numPICs):

		print arrPICs[i].split(" ")[0]+" = ", '{0:.2f}'.format(avgPerPic[i]), "~",colorPercent(avgPerPic[i])," ("+str(NOPPerPic[i])+")"
		
	print "------------------------"



defaultGenre = "BRILINK"

if len(sys.argv) > 0:

#-----------------------------------------------------------------------------------

	try:
		
		strGenre = sys.argv[1]
		#print strGenre

	except IndexError:

		strGenre = defaultGenre

	print "AVAILABILITY dan NOP EDC "+strGenre.upper()+"\nPER PIC KANWIL JAKARTA III" +"\nposisi "+ time.strftime("%d-%m-%Y pukul %H:%M") + "\n"
	MsgBodyRekapPICEDC(strGenre)

