#!/usr/bin/python
#=================================================================================#
# (c) Jansen A. Simanullang: fetchAllDataEDCUkerImplementor
# 19.05.2015 10:56:27 getTableHeader from thead, getNumRowsFoot and getNumRowsHead
#=================================================================================#
from BeautifulSoup import BeautifulSoup
import os, requests, time, urlparse
from urllib import urlopen
#=================================================================================#
# CONFIGURABLE PARAMETER
#=================================================================================#
RegionName = 'JAKARTA 3'
#=================================================================================#


firstURL = 'http://172.18.44.66/edcpro/index.php'
scriptDirectory = os.path.dirname(os.path.abspath(__file__)) + "/"

def welcomeScreen():

	if os.name == "posix":
		os.system("clear")
	else:
		os.system("cls")

	print "FETCH ALL DATA EDC UKER IMPLEMENTOR\n\n\n"


def fetchHTML(alamatURL):

	print "fetching HTML from URL...\n", alamatURL
	strHTML = urlopen(alamatURL).read()	
	strHTML = strHTML.decode("utf-8")
	strHTML = strHTML.encode("utf-8")
	mysoup = BeautifulSoup(strHTML)
	
	print ">> URL fetched."

	return strHTML



def getStyleList(strHTML):

	print "\ngetting Style List...\n"

	mysoup = BeautifulSoup(strHTML)

	arrStyle = mysoup.findAll('link', rel = "stylesheet" )

	strStyle = ""

	for i in range (0, len(arrStyle)):

		strStyle = strStyle + str(arrStyle[i])
	
	return strStyle



def getTableList(strHTML):

	print "\ngetting Table List...\n"

	mysoup = BeautifulSoup(strHTML)

	arrTable = mysoup.findAll('table')

	print "there are:", len(arrTable), "tables."
	
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

	if table:
		print ">> the largest from table list is chosen."

	return table



def getNumCols(table):

	# bagaimana cara menentukan berapa jumlah kolomnya?

	soup = BeautifulSoup(str(table))

	numCols = len(soup.findAll('tbody')[0].findAll('tr')[0].findAll('td'))

	print "number of columns is", numCols

	return numCols



def getNumRows(table):

	# bagaimana cara menentukan berapa jumlah kolomnya?

	numRows = len(table.findAll(lambda tag: tag.name == 'tr' and tag.findParent('table') == table))
	
	return numRows



def getNumRowsHead(table):

	# bagaimana cara menentukan berapa jumlah baris yang terpakai sebagai header?

	soup = BeautifulSoup(str(table))
	head = soup.findAll('thead')

	numRowsHead = 0

	for i in range (0, len(head)):

		numRowsHead += len(head[i].findAll('tr'))

	print "there is", len(head), "header with", numRowsHead, "rows"
		
	return numRowsHead



def getNumRowsFoot(table):

	# bagaimana cara menentukan berapa jumlah baris yang terpakai sebagai footer?

	soup = BeautifulSoup(str(table))
	foot = soup.findAll('tfoot')

	numRowsFoot = 0

	for i in range (0, len(foot)):

		numRowsFoot += len(foot[i].findAll('tr'))

	print "there is", len(foot), "footer with", numRowsFoot, "rows"
		
	return numRowsFoot



def getTableDimension(table):
	
	numRows = getNumRows(table)
	numRowsHead = getNumRowsHead(table)
	numCols = getNumCols(table)
	
	return numRows, numRowsHead, numCols



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



def scrapeOne(firstURL):

	strHTML = fetchHTML(firstURL)
	table = getLargestTable(getTableList(strHTML))
	strHTMLTableRows = getSpecificRows(table, getRowIndex(table, RegionName))
	
	soup = BeautifulSoup(strHTMLTableRows)
	rows = soup.findAll('a')

	return str(rows[0].get('href'))
	


def scrapeTwo(secondURL):

	strHTML = fetchHTML(secondURL)

	table = getLargestTable(getTableList(strHTML))

	numRows = getNumRows(table)

	numRowsHead = getNumRowsHead(table)
	print "number of Rows Head", numRowsHead
	soup = BeautifulSoup(str(table))

	rows = soup.findAll('tr')
	
	arrURL = []
	
	for i in range (numRowsHead, numRows-1): 	# last row is not included

		urls = BeautifulSoup(str(rows[i])).findAll("td")[0].findAll("a")[0].get('href')
		arrURL.append(urls)

	return arrURL



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



def prepareHTMLFile(alamatURL):

	strNamaFile = getUkerImplementor(alamatURL)

	strHTML = fetchHTML(alamatURL)

	arrTable = getTableList(fetchHTML(alamatURL))

	table = getLargestTable(arrTable)

	NamaKanca = BeautifulSoup(getSpecificRows(table, 2)).findAll('td')[9]

	print "preparing HTML file as canvas...", strNamaFile, "\n"

	strData = '<HTML><HEAD><TITLE>MONITORING EDC '+ RegionName +'</TITLE>' + getStyleList(strHTML) + '</HEAD><body>'

	strData = strData + "<h1>" +strNamaFile + "-" + str(NamaKanca) + "</h1><h5>---fetched " + time.strftime("%d.%m.%Y - %H:%M:%S") + "---</h5>"

	strHTML = '<table class="tabledata">' + getTableHeader(table)

	strNamaFile = prepareDirectory('OUTPUT') + strNamaFile + ".html"

	strData = strData + strHTML

   	fileCreate(strNamaFile, strData)



def updateHTMLFile(alamatURL):

	strNamaFile = getUkerImplementor(alamatURL)

	strHTML = fetchHTML(alamatURL)

	arrTable = getTableList(fetchHTML(alamatURL))

	table = getLargestTable(arrTable)

	strHTMLTableContents =  getTableContents(table)
		
	strHTML = strHTMLTableContents

	strNamaFile = prepareDirectory('OUTPUT') + strNamaFile + ".html"

	strData = strHTML 

   	fileAppend(strNamaFile, strData)



def finaleHTMLFile(alamatURL):

	strNamaFile = getUkerImplementor(alamatURL)

	strHTML = fetchHTML(alamatURL)

	arrTable = getTableList(fetchHTML(alamatURL))

	table = getLargestTable(arrTable)

	numCols = getNumCols(table)

	strHTML = '<tfoot><th colspan="'+str(numCols)+'">***</th></tfoot></table></table>'

	strNamaFile = prepareDirectory('OUTPUT') + strNamaFile + ".html"

	strData = strHTML 

   	fileAppend(strNamaFile, strData)



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



def scrapeThree(arrURL):

	arrDetailKanca = []

	for i in range(0, len(arrURL)):

		lastPageNum = getLastPageNum(arrURL[i])

		for j in range (0, lastPageNum/50):
		
			alamatURL = arrURL[i].replace("merchant?", "merchant/"+str(j*50)+"?")
			arrDetailKanca.append(alamatURL)
			
	return arrDetailKanca
		
	

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



def getUkerImplementor(alamatURL):

	try:
		ukerImplementor = getQueryContent(alamatURL, "uker_implementor")

	except KeyError:

		ukerImplementor = "OTHERS"

	return 	ukerImplementor



def main():

	KanwilLink = scrapeOne(firstURL)
	KancaLinks = scrapeTwo(KanwilLink)
	
	arrDetailKanca = scrapeThree(KancaLinks)
	print len(KancaLinks)," links, detailed in ", len(arrDetailKanca), " links"

	for i in range (0, len(KancaLinks)):

		prepareHTMLFile(KancaLinks[i])

	for i in range (0, len(arrDetailKanca)):
		
		updateHTMLFile(arrDetailKanca[i])

	for i in range (0, len(KancaLinks)):
		finaleHTMLFile(arrDetailKanca[i])



def testmain():
	# testmain for testing purposes only
	KanwilLink = scrapeOne(firstURL)
	KancaLinks = scrapeTwo(KanwilLink)
	
	arrDetailKanca = scrapeThree(KancaLinks)
	print len(KancaLinks)," links, detailed in ", len(arrDetailKanca), " links"

	for i in range (0, 1):

		prepareHTMLFile(KancaLinks[i])

	for i in range (0, 1):
		
		updateHTMLFile(arrDetailKanca[i])

	for i in range (0, 1):
		finaleHTMLFile(arrDetailKanca[i])

	

main()
