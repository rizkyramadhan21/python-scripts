#!/usr/bin/python
#---------------------------------------
# TabularEDCperPIC.py
# (c) Jansen A. Simanullang, 01.08.2016
# 05.08.2016
#---------------------------------------
# usage: python TabularEDCperPIC.py
#---------------------------------------
from BeautifulSoup import BeautifulSoup
import os, requests, time, urlparse, sys
import urllib2, pdfkit, xlwt, xlutils
from operator import itemgetter

#---------------------------------------
# CONFIGURABLE PARAMETER
#---------------------------------------
RegionName = 'JAKARTA 3'
#---------------------------------------


firstURL = 'http://172.18.44.66/edcpro/index.php/main/home/index.php'
scriptDirectory = os.path.dirname(os.path.abspath(__file__)) + os.sep



def readPICNumber(branchCode):

	fName = scriptDirectory + "conf/PICEDC.csv"

	arrPICs = [""]
	PICNumber = 0

	f = open(fName)

	for baris in f.readlines():

		col = baris.strip().split(",")
			
		if col[1] == branchCode:

			PICNumber=col[0]
				
	f.close()

	return PICNumber


def readPICName(PICNumber):

	fName = scriptDirectory + "conf/PICNames.csv"

	arrPICs = [""]
	PICName = 0

	f = open(fName)

	for baris in f.readlines():

		col = baris.strip().split(",")

		if col[0] == PICNumber:		

			PICName = col[1]
		
				
	f.close()

	return PICName



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

	print "TABULAR EDC AVAILABILITY & TRANSACTION \n\n\n"


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

	#print "Let's take a look at the specific rows of index", rowIndex

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

				#print "we got the index = ", rowIndex, "from ", numRows, "for search key ='"+strSearchKey+"'"
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

	#print fullPath

	return fullPath



def fileCreate(strNamaFile, strData):
	f = open(strNamaFile, "w")
	f.writelines(str(strData))
	f.close()


    
def fileAppend(strNamaFile, strData):
	f = open(strNamaFile, "a")
	f.writelines(str(strData))
	f.close()



def getTableContents(table):

	numRows = getNumRows(table)
	numRowsHead = getNumRowsHead(table)
	numRowsFoot = getNumRowsFoot(table)

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')
	strHTMLTableContents = ""
	percentPerUker = []

	# EDC MERCHANT

	for i in range (numRowsHead, numRows-numRowsFoot):

		trs = BeautifulSoup(str(rows[i]))
	
		tdcells = trs.findAll("td")

		dText = tdcells[0].getText()

		if not dText[0].isalpha():

			kodeCabang = dText[0:dText.index(' -')].zfill(4)

			namaCabang = cleanupNamaUker(dText[dText.index('-')+2:].upper())

			NOP = int(tdcells[7].getText())

			JumEDC = int(tdcells[8].getText())

			Avail = float(tdcells[9].getText())

			PICName = readPICName(readPICNumber(dText[0:dText.index(' -')]))

			#print kodeCabang, namaCabang, NOP, JumEDC, Avail

			percentPerUker.append((kodeCabang, namaCabang, NOP, JumEDC, Avail, PICName))


	print "RANKING EDC MERCHANT PER PIC\n"

	merchant = sorted(percentPerUker, key=itemgetter(5, 4, 3), reverse = True)

	for e in merchant:

		if e[3]: # jika Jumlah EDC tidak nihil berarti punya EDC
		
			print e[0], e[1], e[2], e[3], "%.2f" % e[4]

	percentPerUker = []
	# EDC BRILINK
	shift = 8

	for i in range (numRowsHead, numRows-numRowsFoot):

		trs = BeautifulSoup(str(rows[i]))
	
		tdcells = trs.findAll("td")

		dText = tdcells[0].getText()

		if not dText[0].isalpha():

			kodeCabang = dText[0:dText.index(' -')].zfill(4)

			namaCabang = cleanupNamaUker(dText[dText.index('-')+2:].upper())

			NOP = int(tdcells[7+shift].getText())

			JumEDC = int(tdcells[8+shift].getText())

			Avail = float(tdcells[9+shift].getText())

			PICName = readPICName(readPICNumber(dText[0:dText.index(' -')]))

			#print kodeCabang, namaCabang, NOP, JumEDC, Avail

			percentPerUker.append((kodeCabang, namaCabang, NOP, JumEDC, Avail, PICName))


	print "\nRANKING EDC BRILINKS\n"

	brilinks = sorted(percentPerUker, key=itemgetter(5, 4, 3), reverse = True)

	print brilinks

	#for e in brilinks:

	#	if e[3]: # jika Jumlah EDC tidak nihil berarti punya EDC
		
	#		print e[0], e[1], e[2], e[3], "%.2f" % e[4]

	return merchant, brilinks



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

	#print fullPath

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


def cleanupNamaUker(namaUker):


	namaUker = namaUker.replace("JAKARTA ","")
	namaUker = namaUker.replace("Jakarta ","")
	namaUker = namaUker.replace("JKT ","")
	namaUker = namaUker.replace("KANCA ","")
	namaUker = namaUker.replace("KC ","")

	return namaUker.strip()




def getRowInterest(table, keyword):

	strHTMLTableRows = getSpecificRow(table, getRowIndex(table, keyword))
	
	mysoup = BeautifulSoup(strHTMLTableRows)

	arrTDs = mysoup.findAll('td')

	return arrTDs[1].getText()


def colorPercent(percentAvail):

	strColor = str(percentAvail)

	if percentAvail >= 0.00:
		strColor = "merah"
	if percentAvail >= 80.00:
		strColor = "kuning"
	if percentAvail >= 90.00:
		strColor = "hijau_muda"
	if percentAvail >= 100.00:
		strColor = "hijau_tua"


	return strColor


def putDataXL(offRow, offCol, merchant, brilinks, jenisPersen):

	book = xlwt.Workbook()

	# add new colour to palette and set RGB colour value
	xlwt.add_palette_colour("sky_blue_10", 0x21)
	book.set_colour_RGB(0x21, 153,204,255)
	xlwt.add_palette_colour("blue_classic", 0x22)
	book.set_colour_RGB(0x22, 207,231,245)
	xlwt.add_palette_colour("hijau_tua", 0x23)
	book.set_colour_RGB(0x23, 0,204,0)
	xlwt.add_palette_colour("hijau_muda", 0x24)
	book.set_colour_RGB(0x24, 153,255,153)
	xlwt.add_palette_colour("kuning", 0x25)
	book.set_colour_RGB(0x25, 255,255,0)
	xlwt.add_palette_colour("merah", 0x26)
	book.set_colour_RGB(0x26, 255,51,51)


	sheet1 = book.add_sheet(jenisPersen, cell_overwrite_ok = True)
	#sheet1 = book.add_sheet(jenisPersen)
	sheet1.row(0).height_mismatch = True
	sheet1.row(0).height = 360
	styleTitle = 'pattern: pattern solid, fore_colour white;'
	styleTitle += 'align: vertical center, horizontal center, wrap on;'
	styleTitle += 'font: name Tahoma, height 280, bold 1;'

	sheet1.write_merge(offRow, offRow, offCol, offCol+12, jenisPersen + ' EDC PRO PER PIC ' + RegionName , xlwt.easyxf(styleTitle))
	shiftDown = 1

	sheet1.row(1).height_mismatch = True
	sheet1.row(1).height = 360
	sheet1.write_merge(offRow+shiftDown, offRow+shiftDown, offCol, offCol+12, 'posisi tanggal ' +time.strftime("%d/%m/%Y-%H:%M") , xlwt.easyxf(styleTitle))
	contentAlignmentHorz = ["center", "right", "center", "center", "left", "center"]


	def styler(strColor,  fontHeight):

		styleHeader = 'pattern: pattern solid, fore_colour '+strColor+';'
		styleHeader += 'align: vertical center, horizontal center, wrap on;'
		styleHeader += 'borders: top thin, bottom thin;'
		styleHeader += 'font: name Tahoma, height '+str(fontHeight)+', bold 1;'
				
		return styleHeader


	# MERCHANT ----------------------------------------------------



	def makeHeader(xRow, yCol, jenisEDC, jenisPersen):

		sheet1.write_merge(xRow+2*shiftDown, xRow+2*shiftDown, yCol, yCol+5, jenisEDC + ' '+jenisPersen, xlwt.easyxf(styler('sky_blue_10', 240)))
	
		arrJudul = ["CODE", "BRANCH", "NOP", "EDC", "%", "PIC"]

		for i in range (0, len(arrJudul)):

			sheet1.write(xRow+3*shiftDown , i+yCol, arrJudul[i], xlwt.easyxf(styler('blue_classic', 180)))

	makeHeader(offRow, offCol, 'MERCHANT', jenisPersen)
	shiftDownSeparator = 0

	for i in range (0, len(merchant)):

		if merchant[i-1][5] != brilinks[i][5]:
			separatorStyle = 'borders: top thin, bottom thin;'
			separatorStyle += 'font: name Tahoma, height 180, bold 1;'
			separatorStyle += 'pattern: pattern solid, fore_colour white;'
			separatorStyle += 'align: horiz left'
			shiftDownSeparator +=1
			sepStyle = xlwt.easyxf(separatorStyle)
			r = i+offRow+4*shiftDown+shiftDownSeparator-1
			c = offCol
			sheet1.write(r, c, i, sepStyle)
			sheet1.write_merge(r, r, c, c+5, merchant[i][5].upper(), sepStyle)

		for j in range(0,len(merchant[i])):

			strColor = colorPercent(merchant[i][4])
			jumlahEDC = merchant[i][3]
			if jumlahEDC == 0:
				strColor = 'white'
			contentStyle = 'font: name Tahoma, height 180;'
			contentStyle += 'pattern: pattern solid, fore_colour '+strColor+';'
			contentStyle += 'align: horiz '+contentAlignmentHorz[j]
			sheet1.col(offCol+0).width = 6*256
			sheet1.col(offCol+1).width = 27*256
			sheet1.col(offCol+2).width = 6*256
			sheet1.col(offCol+3).width = 6*256
			sheet1.col(offCol+4).width = 7*256
			style = xlwt.easyxf(contentStyle)
			sheet1.write(i+offRow+4*shiftDown+shiftDownSeparator, j+offCol, merchant[i][j], style)


	# BRILINKS ----------------------------------------------------

	shiftLeft = 7

	makeHeader(offRow, offCol+shiftLeft, 'BRILINK', jenisPersen)
	shiftDownSeparator = 0

	for k in range (0, len(brilinks)):

		if brilinks[k-1][5] != brilinks[k][5]:
			separatorStyle = 'borders: top thin, bottom thin;'
			separatorStyle += 'font: name Tahoma, height 180, bold 1;'
			separatorStyle += 'pattern: pattern solid, fore_colour white;'
			separatorStyle += 'align: horiz left'
			shiftDownSeparator +=1
			sepStyle = xlwt.easyxf(separatorStyle)
			r = k+offRow+4*shiftDown+shiftDownSeparator-1
			c = offCol+shiftLeft
			sheet1.write(r, c, k, sepStyle)
			sheet1.write_merge(r, r, c, c+5, brilinks[k][5].upper(), sepStyle)

		for l in range(0,len(brilinks[k])):

			strColor = colorPercent(brilinks[k][4])
			jumlahEDC = brilinks[k][3]

			contentStyle = 'font: name Tahoma, height 180;'
			contentStyle += 'pattern: pattern solid, fore_colour '+strColor+';'
			contentStyle += 'align: horiz '+contentAlignmentHorz[l]

			sheet1.col(offCol+shiftLeft+0).width = 6*256
			sheet1.col(offCol+shiftLeft+1).width = 27*256
			sheet1.col(offCol+shiftLeft+2).width = 6*256
			sheet1.col(offCol+shiftLeft+3).width = 6*256
			sheet1.col(offCol+shiftLeft+4).width = 7*256
			style = xlwt.easyxf(contentStyle)

			sheet1.write(k+offRow+4*shiftDown+shiftDownSeparator, l+offCol+shiftLeft, brilinks[k][l], style)
		


	book.save(RegionName + "-EDC " +jenisPersen + "-PIC-" +time.strftime("%Y%m%d-%H")+'.xls')


	
def main():

	#clearDirectory('OUTPUT')
	alamatURL = firstVisit(firstURL)

	print "AVAILABILITY"
	# availability
	strHTML = fetchHTML(alamatURL)
	table = getLargestTable(getTableList(strHTML))
	merchant, brilinks = getTableContents(table)
	putDataXL(0, 0, merchant, brilinks, 'AVAILABILITY')

	print "TRANSACTIONAL"
	# transactional
	alamatURL = alamatURL.replace('main', 'transactional')
	strHTML = fetchHTML(alamatURL)
	table = getLargestTable(getTableList(strHTML))
	merchantt, brilinkst = getTableContents(table)
	putDataXL(0, 0, merchantt, brilinkst, 'TRANSACTIONAL')


main()

