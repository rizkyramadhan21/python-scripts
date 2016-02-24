#!/usr/bin/python
#=================================================================================#
#
# 19.05.2015 10:56:27 getTableHeader from thead, getNumRowsFoot and getNumRowsHead
# 01.06.2015 16:36:49 importing urllib2
#=================================================================================#
from BeautifulSoup import BeautifulSoup
import os, sys, time, urlparse, smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import urllib2
#=================================================================================#
# CONFIGURABLE PARAMETER
#=================================================================================#
RegionName = 'JAKARTA 3'
#=================================================================================#
edcproIP = '172.18.44.66'

firstURL = 'http://172.18.44.66/edcpro/index.php/main/home/index.php'
scriptDirectory = os.path.dirname(os.path.abspath(__file__)) + "/"



def firstVisit(firstURL):

	strHTML = fetchHTML(firstURL)
	table = getLargestTable(getTableList(strHTML))
	strHTMLTableRows = getSpecificRow(table, getRowIndex(table, RegionName))
	
	soup = BeautifulSoup(strHTMLTableRows)
	rows = soup.findAll('a')
	alamatURL = str(rows[0].get('href'))

	return alamatURL


def welcomeScreen():

	if os.name == "posix":
		os.system("clear")
	else:
		os.system("cls")

	print "NOTIFIKASI EDC UKER \n\n\n"


def fetchHTML(alamatURL):

	#print "fetching HTML from URL...\n", alamatURL
	strHTML = urllib2.urlopen(urllib2.Request(alamatURL, headers={ 'User-Agent': 'Mozilla/5.0' })).read()
	strHTML = strHTML.decode("windows-1252")

	strHTML = strHTML.encode('ascii', 'ignore')
	mysoup = BeautifulSoup(strHTML)
	
	#print ">> URL fetched."

	return strHTML



def getStyleList(strHTML):

	#print "\ngetting Style List...\n"

	mysoup = BeautifulSoup(strHTML)

	arrStyle = mysoup.findAll('link', rel = "stylesheet" )

	strStyle = ""

	for i in range (0, len(arrStyle)):

		strStyle = strStyle + str(arrStyle[i])
	
	return strStyle



def getTableList(strHTML):

	#print "\ngetting Table List...\n"

	mysoup = BeautifulSoup(strHTML)

	arrTable = mysoup.findAll('table')

	#print "there are:", len(arrTable), "tables."
	
	return arrTable



def getLargestTable(arrTable):

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
	#	print ">> the largest from table list is chosen."

	return table



def getNumCols(table):

	# bagaimana cara menentukan berapa jumlah kolomnya?

	soup = BeautifulSoup(str(table))

	numCols = len(soup.findAll('tbody')[0].findAll('tr')[0].findAll('td'))

	#print "number of columns is", numCols

	return numCols


def getNumRows(table):

	# bagaimana cara menentukan berapa jumlah kolomnya?

	numRows = len(table.findAll(lambda tag: tag.name == 'tr' and tag.findParent('table') == table))
	
	return numRows


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



def getNumRowsHead(table):

	# bagaimana cara menentukan berapa jumlah baris yang terpakai sebagai header?

	soup = BeautifulSoup(str(table))
	head = soup.findAll('thead')

	numRowsHead = 0

	for i in range (0, len(head)):

		numRowsHead += len(head[i].findAll('tr'))

	#print "there is", len(head), "header with", numRowsHead, "rows"
		
	return numRowsHead



def getNumRowsFoot(table):

	# bagaimana cara menentukan berapa jumlah baris yang terpakai sebagai footer?

	soup = BeautifulSoup(str(table))
	foot = soup.findAll('tfoot')

	numRowsFoot = 0

	for i in range (0, len(foot)):

		numRowsFoot += len(foot[i].findAll('tr'))

	#print "there is", len(foot), "footer with", numRowsFoot, "rows"
		
	return numRowsFoot



def getTableDimension(table):
	
	numRows = getNumRows(table)
	numRowsHead = getNumRowsHead(table)
	numCols = getNumCols(table)
	
	return numRows, numRowsHead, numCols



def getSpecificRow(table, rowIndex):

	print "Let's take a look at the specific rows of index", rowIndex

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')
	strHTMLTableRows = ""

	for i in range (rowIndex, rowIndex+1):

		strHTMLTableRows = str(rows[i])
	
	return strHTMLTableRows



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


def getSpecificRows(table, rowIndex):

	print "Let's take a look at the specific rows of index", rowIndex

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')
	strHTMLTableRows = ""

	for i in range (rowIndex, rowIndex+1):

		strHTMLTableRows = str(rows[i])
	
	return strHTMLTableRows



def prepareDirectory(strOutputDir):
	# siapkan struktur direktori untuk penyimpanan data
	# struktur direktori adalah ['OUTPUT', 'EDC', '2015', '04-APR', 'DAY-28'] makes './OUTPUT/EDC/2015/04-APR/DAY-28'

	arrDirectoryStructure = [strOutputDir, 'EDC', time.strftime("%Y"), time.strftime("%m-%b").upper() , "DAY-"+time.strftime("%d")]

	fullPath = scriptDirectory

	for i in range (0, len(arrDirectoryStructure)):
	
		fullPath = fullPath + arrDirectoryStructure[i] + "/"

		if not os.path.exists(fullPath):

			print "creating directories:", arrDirectoryStructure[i]
		    	os.mkdir(fullPath)
			os.chdir(fullPath)

	print fullPath

	return fullPath



def fileCreate(strNamaFile, strData):
	f = open(strNamaFile, "w")
	f.writelines(str(strData))
	f.close()


    
def fileAppend(strNamaFile, strData):
	f = open(strNamaFile, "a")
	f.writelines(str(strData))
	f.close()


def makeFileName(alamatURL):
	# makes title of a section based on a URL

	strFileName = getQueryContent(alamatURL, "peruntukkan")

	statusAvail = getQueryContent(alamatURL, "status_available")

	if statusAvail == '5':

		strFileName = strFileName + " NOP LEBIH 30 HARI"

	if statusAvail == '4':

		strFileName = strFileName + " NOP 16-30 HARI"

	strFileName = "[" + strFileName + "]"
	# embraced by a parentheses

	return strFileName


def prepareHTMLFile(alamatURL):

	strNamaFile = makeFileName(alamatURL)

	strHTML = fetchHTML(alamatURL)

	arrTable = getTableList(fetchHTML(alamatURL))

	table = getLargestTable(arrTable)

	NamaKanca = BeautifulSoup(getSpecificRows(table, 2)).findAll('td')[9]

	print "preparing HTML file as canvas...", strNamaFile, "\n"

	strHTML = '<HTML><HEAD><TITLE>MONITORING EDC '+ RegionName +'</TITLE>' + getStyleList(strHTML) + '</HEAD><body>'

	strHTML += "<h5>" +strNamaFile + " - " + RegionName + "</h5>---fetched " + time.strftime("%d.%m.%Y - %H:%M:%S") + "---"

	strHTML += '<table class="tabledata">' + getTableHeader(table)

	strNamaFile = prepareDirectory('OUTPUT') + strNamaFile + ".html"

   	fileCreate(strNamaFile, strHTML)

	return strNamaFile



def updateHTMLFile(alamatURL):

	strNamaFile = makeFileName(alamatURL)

	strHTML = fetchHTML(alamatURL)

	arrTable = getTableList(fetchHTML(alamatURL))

	table = getLargestTable(arrTable)

	strHTMLTableContents =  getTableContents(table)
		
	strHTML = strHTMLTableContents

	strNamaFile = prepareDirectory('OUTPUT') + strNamaFile + ".html"

   	fileAppend(strNamaFile, strHTML)

	return strNamaFile



def finaleHTMLFile(alamatURL):

	strNamaFile = makeFileName(alamatURL)

	strHTML = fetchHTML(alamatURL)

	arrTable = getTableList(fetchHTML(alamatURL))

	table = getLargestTable(arrTable)

	numCols = getNumCols(table)

	strHTML = '<tfoot><th colspan="'+str(numCols)+'">***</th></tfoot></table>'

	strNamaFile = prepareDirectory('OUTPUT') + strNamaFile + ".html"

   	fileAppend(strNamaFile, strHTML)

	return strNamaFile



def getTableHeader(table):

	numRowsHead = getNumRowsHead(table)

	soup = BeautifulSoup(str(table))
	head = soup.findAll('thead')
	strHTMLTableHeader = ""
	
	for i in range (0, len(head)):

		strHTMLTableHeader = strHTMLTableHeader + str(head[i])
	
	return strHTMLTableHeader



def getTableContents(table):

	numRows = getNumRows(table)
	numRowsHead = getNumRowsHead(table)
	numRowsFoot = getNumRowsFoot(table)

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')
	strHTMLTableContents = ""

	for i in range (numRowsHead, numRows-numRowsFoot):

		strHTMLTableContents = strHTMLTableContents + str(rows[i])

	return strHTMLTableContents



def getColIndex(table, strSearchKey1, strSearchKey2):

	# fungsi ini untuk mendapatkan nomor indeks kolom yang mengandung satu kata kunci

	numCols = getNumCols(table)
	numRowsHead = getNumRowsHead(table)

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')

	colIndex1 = -1

	for i in range (0, 1):

		trs = BeautifulSoup(str(rows[i]))
		thcells = trs.findAll("th")
			
		for i in range (0, len(thcells)):

			if ("colspan" in str(thcells[i]) and thcells[i].findAll('a')[0].getText().upper() == strSearchKey1.upper()):

				intColSpan = int(thcells[i]['colspan'])

				print i, intColSpan

				colIndex1 = (i-1) * intColSpan + 1

				
			elif ("rowspan" in str(thcells[i]) and thcells[i].getText().upper() == strSearchKey1.upper()):

				intColSpan = 1

				colIndex1 = (i-1) * intColSpan + 1 

				print i, "rowspan"
	#colIndex2 = 0
	for i in range (1, 2):
					
		soup = BeautifulSoup(str(rows[i]))
		thcells2 = soup.findAll("th")

		# the length must be limited to the colindex of the above search
		maxIndex = len(thcells2)
		maxIndex = colIndex1 - 1

		for i in range (0, maxIndex):
		
			if thcells2[i].getText().upper() == strSearchKey2.upper():
				colIndex2 = i+3 # the factor +3 is due to the two columns with the rowspan before
				


				
	print "we got the col index = (", colIndex1, ") from ", numCols-1, "index for search key ='"+strSearchKey1+"'"
	print "we got the col index = (", colIndex2, ") from ", numCols-1, "index for search key ='"+strSearchKey2+"'"
	return colIndex2



def getQueryContent(alamatURL, strQuery):
	
	parsed = urlparse.urlparse(alamatURL)
	QueryContent = str(urlparse.parse_qs(parsed.query)[strQuery][0])
	return QueryContent



def prepareDirectory(strOutputDir):
	# siapkan struktur direktori untuk penyimpanan data
	# struktur direktori adalah ['OUTPUT', 'EDC', '2015', '04-APR', 'DAY-28'] makes './OUTPUT/EDC/2015/04-APR/DAY-28'

	arrDirectoryStructure = [strOutputDir, 'EDC', time.strftime("%Y"), time.strftime("%m-%b").upper() , "DAY-"+time.strftime("%d")]

	fullPath = scriptDirectory

	for i in range (0, len(arrDirectoryStructure)):
	
		fullPath = fullPath + arrDirectoryStructure[i] + "/"

		if not os.path.exists(fullPath):

			print "creating directories:", arrDirectoryStructure[i]
		    	os.mkdir(fullPath)
			os.chdir(fullPath)

	print fullPath

	return fullPath



def clearDirectory(strOutputDir):

	# clear directory from previous call within the same date

	arrDirectoryStructure = [strOutputDir, 'EDC', time.strftime("%Y"), time.strftime("%m-%b").upper() , "DAY-"+time.strftime("%d")]

	fullPath = scriptDirectory

	for i in range (0, len(arrDirectoryStructure)):
	
		fullPath = fullPath + arrDirectoryStructure[i] + "/"

	if os.path.exists(fullPath):

		print "clearing today's data directory:...\n", fullPath
	    	os.system('rm -rf '+ fullPath)


def fileCreate(strNamaFile, strData):
	f = open(strNamaFile, "w")
	f.writelines(str(strData))
	f.close()


    
def fileAppend(strNamaFile, strData):
	f = open(strNamaFile, "a")
	f.writelines(str(strData))
	f.close()

def createTextFile(namaFile):
	# create a text file
	print "preparing text file...", namaFile.split("/")[-1]
	
	strTitle = "NOTIFIKASI EDC " + namaFile.split("/")[-1].replace("_"," ").replace("[","").replace("]","") +"\n"+time.strftime("%d.%m.%Y-%H:%M") + "\n"
	# make a title for this purpose

	fileCreate(namaFile, strTitle)


def updateTextFile(namaFile, strData):
	# update a text file of namaUker with a strData

	strNamaFile = prepareDirectory('OUTPUT') + namaFile
	# make a full file name

	if not os.path.exists(strNamaFile):
	# if the full file name does not exist then create it

		createTextFile(strNamaFile) # try changing this from namaFile to strNamaFile

	print "updating text file...", namaFile

   	fileAppend(strNamaFile, strData)


def getSectionTitle(alamatURL):
	# makes title of a section based on a URL

	strTitle = getQueryContent(alamatURL, "peruntukkan")

	statusAvail = getQueryContent(alamatURL, "status_available")

	if statusAvail == '5':

		strTitle = strTitle + " NOP > 30 HARI"

	if statusAvail == '4':

		strTitle = strTitle + " NOP 16-30 HARI"

	strTitle = "[" + strTitle + "]\n\n"
	# embraced by a parentheses

	return strTitle



def getLastPageNum(alamatURL):


	strHTML = fetchHTML(alamatURL)

	mysoup = BeautifulSoup(strHTML)

	arrURL = mysoup.findAll('tfoot')[0].findAll('tr')[0].findAll('a')
	
	maxPage = 0

	if arrURL:
		
		for i in range (0, len(arrURL)):

			lastPageNum = int(arrURL[i].get('href').split('/')[7].split('?')[0])

			if lastPageNum > maxPage:

				maxPage = lastPageNum

		lastPageNum = maxPage
		
	else:
		lastPageNum = 0
	print "last page number is:", lastPageNum
	return int(lastPageNum)



def getQueryContent(alamatURL, strQuery):
	
	parsed = urlparse.urlparse(alamatURL)
	QueryContent = str(urlparse.parse_qs(parsed.query)[strQuery][0])
	return QueryContent

	# sample:
	# alamatURL = 'http://172.18.44.66/edcpro/index.php/detail/merchant?kanwil_implementor=Q&uker_implementor=170'
	# print getQueryContent(alamatURL, "uker_implementor")
	# 170



def getLastPageNum(alamatURL):
	# this function searches the last page number by comparing each page number and choose the greatest
	
	strHTML = fetchHTML(alamatURL)

	mysoup = BeautifulSoup(strHTML)

	arrURL = mysoup.findAll('tfoot')[0].findAll('tr')[0].findAll('a')
	
	# this initializes the maximum page as zero	
	maxPage = 0

	if arrURL:
	# if arrURL is not empty then search for each page number
	
		for i in range (0, len(arrURL)):

			PageNum = int(arrURL[i].get('href').split('/')[7].split('?')[0])
			# page number is a string and must be converted to integer
			# to be able to be compared

			if PageNum > maxPage:
			# if the page number

				maxPage = PageNum

		PageNum = maxPage
		
	else:
	# if arrURL is empty then PageNum equals zero

		PageNum = 0

	print "last page number is:", PageNum

	return int(PageNum)



def getArrURLPages(alamatURL):
	# this function makes an array of URLs
	# based on the last page number

	intLastPage = getLastPageNum(alamatURL)
	arrURL = []

	for i in range (0, intLastPage/50+1):

		arrURL.append(alamatURL.replace("merchant?","merchant/"+str(i*50)+"?"))

	return arrURL



def getURLfromFoot(columnIndex, table):
	# this function gets url form footer in a column 
	# the column position is in index columnIndex

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')

	numRowsHead =getNumRowsHead(table)
	numRows =getNumRows(table)
	numRowsFoot =getNumRowsFoot(table)
	
	for i in range(numRows-1, numRows):

		ths = rows[i].findAll('th')[columnIndex]
		# collect all the <th>s that is at the columnIndex

		if ths.findAll('a'):
		# check only <th>s containing <a>
			
			alamatURL = ths.findAll('a')[0].get('href')
			# save the 'href' content as alamatURL

	return alamatURL


def getUkerImplementor(alamatURL):

	strHTML = fetchHTML(alamatURL)
	arrTable = getTableList(strHTML)
	# get all the table and display in a list

	for i in range (0, len(arrTable)):

		if "Implementor" in str(arrTable[i]):
		# if a keyword 'Implementor' is in the table

			indexTable = i
			# then index table that contains the keyword is 'i'

	table = arrTable[indexTable]
	# we choose only the table that matches our criteria at the index
		
	strHTMLTableRows = getSpecificRow(table, getRowIndex(table, "Sub Channel"))
	# we choose the specific row contains the keyword 'Sub Channel'

	mysoup = BeautifulSoup(strHTMLTableRows)
	# make a soup from the table row

	arrTDs = mysoup.findAll('td')
	# collect all the <td>s in an array

	strSubChannel = arrTDs[1].getText().strip()
	# save the text of the data

	strHTMLTableRows = getSpecificRow(table, getRowIndex(table, "Implementor"))
	# we choose the specific row contains the keyword 'Implementor'

	mysoup = BeautifulSoup(strHTMLTableRows)
	# make a soup from the table row

	arrTDs = mysoup.findAll('td')
	# collect all the <td>s in an array

	strImplementor = arrTDs[1].getText().upper().strip()
	# save the text of the data

	if not strImplementor:
	# if strImplementor is empty, which is almost all in the BRILINK NOP data

		strHTMLTableRows = getSpecificRow(table, getRowIndex(table, "Kanwil Implementor"))
		# we choose the specific row contains the keyword 'Implementor'

		mysoup = BeautifulSoup(strHTMLTableRows)
		# make a soup from the table row

		arrTDs = mysoup.findAll('td')
		# collect all the <td>s in an array

		strImplementor = arrTDs[1].getText().upper().strip()

	return strSubChannel, strImplementor



def getArrNamaUker():

	fName = scriptDirectory +"branchCode.888"
		
	f = open(fName)

	branchLine = f.readlines()


	arrNamaUker = ['']*(len(branchLine)-1)

	for i in range(0, len(arrNamaUker)-1):

		arrNamaUker[i] = branchLine[i].replace("\n","").split("|")[1]
		
	return arrNamaUker



def getArrKodeUker():

	fName = scriptDirectory +"branchCode.888"
		
	f = open(fName)

	branchLine = f.readlines()


	arrKodeUker = ['']*(len(branchLine)-1)

	for i in range(0, len(arrKodeUker)-1):

		arrKodeUker[i] = branchLine[i].replace("\n","").split("|")[0]
		
	return arrKodeUker



def getAvailabilityRank(table):

	try:

		#print "getting List of ATMs requires attention..."
	
		soup = BeautifulSoup(str(table))
	
		rows = soup.findAll('tr')

		numRows = getRowsNumber(table)

		numRowsHead = getRowsHeadNumber(table)

	
		arrBestBranchBri = []
		
		for a in range (2, numRows-1):

			trs = BeautifulSoup(str(rows[a]))
			tdcells = trs.findAll("td")

			percentAvailBri = float(tdcells[17].getText())
			ukerName = cleanUpNamaUker(tdcells[0].getText())

			if (percentAvailBri == 100.00):

				#arrBestBranch.append(ukerName+", "+jumlahATM)
				arrBestBranchBri.append(ukerName)

	except IndexError:

		arrBestBranchBri = getAvailabilityRank(table)

	return sorted(arrBestBranchBri)


def cleanUpNamaUker(strNama):

	strNama = strNama.split("-")[-1]
	strNama = strNama.replace("KC ", "")
	strNama = strNama.replace("KANCA ", "")
	strNama = strNama.replace("JAKARTA ", "")
	strNama = strNama.replace("Jakarta ", "")
	strNama = strNama.replace("JKT ", "")



	return strNama.title()


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

percentAvail = 0.0
alamatURL = 'http://172.18.44.66/edcpro/index.php/main/kanwil_implementor?kanwil=Q'
table = getLargestTable(getTableList(fetchHTML(alamatURL)))
arrBestBranchBri = getAvailabilityRank(table)


msgBody =""

if len(arrBestBranchBri):

		msgBody = msgBody + "100% AVAILABILITY: "+str(len(arrBestBranchBri)) + " KANCA \n\n* " + "\n* ".join(arrBestBranchBri)
AvailText = msgBody



msgBody = "----------------------------------------------------\n"
msgBody = msgBody + "KANCA with BEST AVAILABILITY EDC BRILINK\nKANWIL "+RegionName + "\n"
msgBody = msgBody + "per "+ time.strftime("%d-%m-%Y pukul %H:%M") + "\n"
msgBody = msgBody + "----------------------------------------------------\n"
msgBody = msgBody + AvailText + "\n"
msgBody = msgBody + "----------------------------------------------------\n"

print msgBody
	

