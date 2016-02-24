#!/usr/bin/python
#---------------------------------------
# fetchStatusATMPro.py
# (c) Jansen A. Simanullang, 12:38
# 2106.01.06
# to be used with telegram-bot plugin
#---------------------------------------
# usage: fetchStatusATMPro 0509
# script name followed by space and branchCode
#---------------------------------------

from BeautifulSoup import BeautifulSoup
import sys, time
import urllib2

atmproIP = "172.18.65.42"

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



def cleanUpHTML(strHTML):

	# fixing broken HTML
	strHTML = strHTML.replace('</tr><td>',"</tr><tr><td>")
	strHTML = strHTML.replace('</td></tr><td>','</td></tr><tr><td>')
	strHTML = strHTML.replace('<table class=fancy>','</td></tr></table><table class=fancy>')
	strHTML = strHTML.replace('</th>\n</tr>',"</th></tr><tr>")
	strHTML = strHTML.replace('</tr>\n\n<td>',"</tr><tr><td>")


	strHTML = strHTML.replace(' bgcolor>', '>')
	strHTML = strHTML.replace('<table class=fancy>','</td></tr></table><table class=fancy>')


	return strHTML



def getTableList(strHTML):

	#print "\ngetting Table List...\n"

	mysoup = BeautifulSoup(strHTML)

	arrTable = mysoup.findAll('table')

	#print "there are:", len(arrTable), "tables."

	return arrTable



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
	#	print ">> the largest from table list is chosen."

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
	#	print ">> the widest from table list is chosen."

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


def getATMStats(table):

	soup = BeautifulSoup(str(table))
	
	rows = soup.findAll('tr')

	numRows = getRowsNumber(table)

	numCols = getColsNumber(table)

	numRowsHead = getRowsHeadNumber(table)

	#print numRowsHead, numRows
	msgBody = ""

	seqNo = 0
	
	for i in range (0, numRows):

		trs = BeautifulSoup(str(rows[i]))

		tdcells = trs.findAll("td")
		thcells = trs.findAll("th")

		#print len(tdcells), len(thcells)



		if tdcells:


			msgBody += "\n"+tdcells[0].getText().upper()+") "+ tdcells[1].getText()+", " + tdcells[2].getText().replace("HYOSUNG","HYOSUNG ") +"\nLOKASI: "+ tdcells[4].getText() +"\nAREA: "+ tdcells[5].getText()+"\nDURASI: "+ tdcells[6].getText().replace("days","hari ").replace("hours","jam") +"\n"+"\n"
	if msgBody == "":
		msgBody = "Tidak ada ATM PROBLEM OPS di wilayah kerja Anda."
	return msgBody



def getATMStatsCRO(table):

	soup = BeautifulSoup(str(table))
	
	rows = soup.findAll('tr')

	numRows = getRowsNumber(table)

	numCols = getColsNumber(table)

	numRowsHead = getRowsHeadNumber(table)

	#print numRowsHead, numRows
	msgBody = ""

	seqNo = 0
	
	for i in range (0, numRows):

		trs = BeautifulSoup(str(rows[i]))

		tdcells = trs.findAll("td")
		thcells = trs.findAll("th")

		#print len(tdcells), len(thcells)


		if tdcells:

			if "ATM CENTER" in tdcells[6].getText():

				seqNo = seqNo +1

				msgBody += "\n"+str(seqNo)+") "+"CRO: " + tdcells[6].getText().replace("ATM CENTER (","").replace(")","")+ "\nTID: " +tdcells[1].getText()+", " + tdcells[2].getText().replace("HYOSUNG","HYOSUNG ") +"\nLOKASI: "+ tdcells[5].getText()+"\nDURASI: "+ tdcells[8].getText().replace("days","hari ").replace("hours","jam") +"\nUKER: "+tdcells[7].getText().upper()+"\n"
	if msgBody == "":
		msgBody = "Tidak ada ATM PROBLEM OPS CRO kategori ini di wilayah kerja Anda."
	return msgBody


def getATMProbStats(table):

	#print "getting List of ATMs requires attention..."
	
	soup = BeautifulSoup(str(table))
	
	rows = soup.findAll('tr')

	numRows = getRowsNumber(table)

	numRowsHead = getRowsHeadNumber(table)

	msgBody = ""

	numCOUKO = 0
	numCOCRO = 0
	numCLUKO = 0
	numCLCRO = 0
	numDFUKO = 0
	numDFCRO = 0
	numOOSUKO = 0
	numOOSCRO = 0
	numCOMUKO = 0
	numCOMCRO = 0
	numCCRUKO = 0
	numCCRCRO = 0

	arrCOUKO = []
	arrCOCRO = []
	arrCLUKO = []
	arrCLCRO = []
	arrDFUKO = []
	arrDFCRO = []
	arrOOSUKO = []
	arrOOSCRO = []
	arrCOMUKO = []
	arrCOMCRO = []
	arrCCRUKO = []
	arrCCRCRO = []


	for i in range (numRowsHead, numRows):

		trs = BeautifulSoup(str(rows[i]))
		tdcells = trs.findAll("td")

#----------- COM

		if tdcells[7].getText() == "OFFLINE":

			tid = tdcells[1].getText()
			tidlocation = cleanupLocation(tdcells[5].getText())

			strPengelola, strSupervisi = getPengelolaSupervisi(tid)

			if ("ATM CENTER" in strPengelola or "VENDOR" in strPengelola):

				numCOMCRO = numCOMCRO + 1

				arrCOMCRO.append(str(numCOMCRO) + ") " + tid + "\t" + tidlocation + ", " + cleanupLocation(strPengelola))
			else:
				numCOMUKO = numCOMUKO + 1
				
				arrCOMUKO.append(str(numCOMUKO) + ") " + tid + "\t" + tidlocation + ", " + cleanupLocation(strPengelola))


#----------- CO

		if tdcells[8].getText() == "CASH OUT":

			tid = tdcells[1].getText()
			tidlocation = cleanupLocation(tdcells[5].getText())

			strPengelola, strSupervisi = getPengelolaSupervisi(tid)

			if ("ATM CENTER" in strPengelola or "VENDOR" in strPengelola):

				numCOCRO = numCOCRO + 1

				arrCOCRO.append(str(numCOCRO) + ") " + tid + "\t" + tidlocation + ", " + cleanupLocation(strPengelola))
			else:
				numCOUKO = numCOUKO + 1
				
				arrCOUKO.append(str(numCOUKO) + ") " + tid + "\t" + tidlocation + ", " + cleanupLocation(strPengelola))
	
#----------- CL
		if tdcells[9].getText() == "LOW":

			tid = tdcells[1].getText()
			tidlocation = cleanupLocation(tdcells[5].getText())

			strPengelola, strSupervisi = getPengelolaSupervisi(tid)

			if ("ATM CENTER" in strPengelola or "VENDOR" in strPengelola):

				numCLCRO = numCLCRO + 1

				arrCLCRO.append(str(numCLCRO) + ") " + tid + "\t" + tidlocation + ", " + cleanupLocation(strPengelola))
			else:
				numCLUKO = numCLUKO + 1
				
				arrCLUKO.append(str(numCLUKO) + ") " + tid + "\t" + tidlocation + ", " + cleanupLocation(strPengelola))
	

#----------- CCR

		if tdcells[10].getText() == "CARD READER":

			tid = tdcells[1].getText()
			tidlocation = cleanupLocation(tdcells[5].getText())

			strPengelola, strSupervisi = getPengelolaSupervisi(tid)

			if ("ATM CENTER" in strPengelola or "VENDOR" in strPengelola):

				numCCRCRO = numCCRCRO + 1

				arrCCRCRO.append(str(numCCRCRO) + ") " + tid + "\t" + tidlocation + ", " + cleanupLocation(strPengelola))
			else:
				numCCRUKO = numCCRUKO + 1
				
				arrCCRUKO.append(str(numCCRUKO) + ") " + tid + "\t" + tidlocation + ", " + cleanupLocation(strPengelola))

#----------- DISP STATUS/ DF
		if tdcells[11].getText() == "FAIL":

			tid = tdcells[1].getText()
			tidlocation = cleanupLocation(tdcells[5].getText())

			strPengelola, strSupervisi = getPengelolaSupervisi(tid)

			if ("ATM CENTER" in strPengelola or "VENDOR" in strPengelola):

				numDFCRO = numDFCRO + 1

				arrDFCRO.append(str(numDFCRO) + ") " + tid + "\t" + tidlocation + ", " + cleanupLocation(strPengelola))
			else:
				numDFUKO = numDFUKO + 1
				
				arrDFUKO.append(str(numDFUKO) + ") " + tid + "\t" + tidlocation + ", " + cleanupLocation(strPengelola))
	



#-----------
	#arrOOSUKO.remove(arrOOSUKO[0])
	#arrOOSCRO.remove(arrOOSCRO[0])
	#arrCOUKO.remove(arrCOUKO[0])
	#arrCOCRO.remove(arrCOCRO[0])
	#arrCLUKO.remove(arrCLUKO[0])
	#arrCLCRO.remove(arrCLCRO[0])
	#arrDFUKO.remove(arrDFUKO[0])
	#arrDFCRO.remove(arrDFCRO[0])

	if ((numOOSUKO > 0) or (numCOUKO > 0) or (numCLUKO > 0) or (numDFUKO > 0) or (numCOMUKO > 0) or (numCCRUKO > 0)):
		
		msgBody = msgBody + "\n[PROBLEM ATM UKO]\n"

	if numCOUKO:

		msgBody = msgBody + "\nCASH OUT: "+str(numCOUKO) + "\n" + "\n".join(arrCOUKO) + "\n"

	if numCLUKO:

		msgBody = msgBody + "\nCASH LOW: "+str(numCLUKO) + "\n" + "\n".join(arrCLUKO) + "\n"

	if numDFUKO:

		msgBody = msgBody + "\nDISPENSER FAILURE: "+str(numDFUKO) + "\n" + "\n".join(arrDFUKO) + "\n"

	if numOOSUKO:

		msgBody = msgBody + "\nOOS: "+str(numOOSUKO) + "\n" + "\n".join(arrOOSUKO) + "\n"

	if numCOMUKO:

		msgBody = msgBody + "\nCOM: "+str(numCOMUKO) + "\n" + "\n".join(arrCOMUKO) + "\n"

	if numCCRUKO:

		msgBody = msgBody + "\nCCR: "+str(numCCRUKO) + "\n" + "\n".join(arrCCRUKO) + "\n"


	if (numOOSCRO !=0 or numCOCRO !=0 or numCLCRO !=0 or numDFCRO !=0 or numCOMCRO !=0 or numCCRCRO !=0):
		
		msgBody = msgBody + "\n[PROBLEM ATM CRO]\n"

	if numCOCRO:

		msgBody = msgBody + "\nCASH OUT: "+str(numCOCRO) + "\n" + "\n".join(arrCOCRO) + "\n"

	if numCLCRO:

		msgBody = msgBody + "\nCASH LOW: "+str(numCLCRO) + "\n" + "\n".join(arrCLCRO) + "\n"

	if numDFCRO:

		msgBody = msgBody + "\nDISPENSER FAILURE: "+str(numDFCRO) + "\n" + "\n".join(arrDFCRO) + "\n"

	if numOOSCRO:

		msgBody = msgBody + "\nOOS: "+str(numOOSCRO) + "\n" + "\n".join(arrOOSCRO) + "\n"

	if numCOMCRO:

		msgBody = msgBody + "\nCOM: "+str(numCOMCRO) + "\n" + "\n".join(arrCOMCRO) + "\n"

	if numCCRCRO:

		msgBody = msgBody + "\nCCR: "+str(numCCRCRO) + "\n" + "\n".join(arrCCRCRO) + "\n"

	if msgBody:

		msgBody = msgBody
	else:

		msgBody = "\nEXCELLENT WORK! EVERYTHING IS OKAY!"

	return msgBody

def cleanupLocation(tidlocation):
	tidlocation = tidlocation.replace("("," (")
	tidlocation = tidlocation.replace(") ("," ")
	tidlocation = tidlocation.replace(" ]","]")
	tidlocation = tidlocation.replace("-"," ")
	tidlocation = tidlocation.replace("BG III (","(BG III ")
	tidlocation = tidlocation.replace("(SWADARMA SARANA (","(SSI ")
	tidlocation = tidlocation.replace("BRINGIN GIGANTARA","BG")
	tidlocation = tidlocation.replace("ATM CENTER ( ","(")
	tidlocation = tidlocation.replace("ATM CENTER","")
	tidlocation = tidlocation.replace("JAKARTA UNIT","UNIT")
	tidlocation = tidlocation.replace("JAKARTA KCP","KCP")
	tidlocation = tidlocation.replace("JAKARTA KC","KC")
	tidlocation = tidlocation.replace("JAKARTA KK","KK")
	tidlocation = tidlocation.replace("JAKARTA 1 ","")
	tidlocation = tidlocation.replace("JAKARTA 2 ","")
	tidlocation = tidlocation.replace("JAKARTA 3 ","")
	tidlocation = tidlocation.replace("JAKARTA3 ","")
	tidlocation = tidlocation.replace("KANWIL 3 ","")
	tidlocation = tidlocation.replace("JKT 1","")
	tidlocation = tidlocation.replace("JKT 2","")
	tidlocation = tidlocation.replace("JKT 3","")
	tidlocation = tidlocation.replace("JKT1 ","")	
	tidlocation = tidlocation.replace("JKT2 ","")
	tidlocation = tidlocation.replace("JKT3 ","")
	tidlocation = tidlocation.replace("JAK 3","")
	tidlocation = tidlocation.replace("JAK3 ","")
	tidlocation = tidlocation.replace("BRI ","")
	tidlocation = tidlocation.replace("( ","(")
	tidlocation = tidlocation.replace("  "," ")

	return tidlocation.strip()

def getPengelolaSupervisi(strTID):

	try:	
		strURL = "http://172.18.65.42/statusatm/viewatmdetail.pl?ATM_NUM="+strTID

		strHTML = fetchHTML(strURL)

		table = getLargestTable(getTableList(strHTML))

		strHTMLTableRows = getSpecificRows(table, getRowIndex(table, "Pengelola"))

		mysoup = BeautifulSoup(strHTMLTableRows)

		arrTDs = mysoup.findAll('td')
	
		strPengelola = arrTDs[1].getText()
		
		strHTMLTableRows = getSpecificRows(table, getRowIndex(table, "KC Supervisi"))

		mysoup = BeautifulSoup(strHTMLTableRows)

		arrTDs = mysoup.findAll('td')

		strSupervisi = arrTDs[1].getText()

	except IndexError:
	
		strPengelola, strSupervisi = getPengelolaSupervisi(strTID)

	except RuntimeError:

		strPengelola, strSupervisi = "Kanca BRI Bumi Serpong Damai", "KANWIL BRI JAKARTA III"

	return strPengelola, strSupervisi



def getAvailBranch(branchCode):

	try:	
		strURL = 'http://172.18.65.42/statusatm/dashboard_cabang.pl?REGID=15&REGNAME=Jakarta%20III'

		strHTML = fetchHTML(strURL)

		table = getLargestTable(getTableList(strHTML))

		strHTMLTableRows = getSpecificRows(table, getRowIndex(table, branchCode))

		mysoup = BeautifulSoup(strHTMLTableRows)

		arrTDs = mysoup.findAll('td')
	
		percentAvail = arrTDs[24].getText()
		

	except IndexError:
	
		percentAvail = getAvailBranch(branchCode)

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


def getATMStatsUKO(table):

	soup = BeautifulSoup(str(table))
	
	rows = soup.findAll('tr')

	numRows = getRowsNumber(table)

	numCols = getColsNumber(table)

	numRowsHead = getRowsHeadNumber(table)

	#print numRowsHead, numRows
	msgBody = ""

	seqNo = 0

	
	for i in range (numRowsHead, numRows):

		trs = BeautifulSoup(str(rows[i]))

		tdcells = trs.findAll("td")
		thcells = trs.findAll("th")

		#print len(tdcells), len(thcells)


		if tdcells:

			if "ATM CENTER" not in tdcells[6].getText():

				seqNo = seqNo +1

				msgBody += "\n"+str(seqNo)+") " + tdcells[7].getText().upper() + "\nTID: " + tdcells[1].getText()+", " + tdcells[2].getText().replace("HYOSUNG","HYOSUNG ") +"\nLOKASI: "+ tdcells[5].getText()+"\nDURASI: "+ tdcells[8].getText().replace("days","hari ").replace("hours","jam")+"\n"
	if msgBody == "":
		msgBody = "Tidak ada ATM OPS UKO kategori ini di wilayah kerja Anda."
	return msgBody



msgBody =""

timestamp = "\nper "+ time.strftime("%d-%m-%Y pukul %H:%M")

if len(sys.argv) > 0:

	AREAID = sys.argv[1]

	strHeaderLine = "\n----------------------------------------------\n"

	if AREAID.isdigit():
	

		alamatURL = "http://172.18.65.42/statusatm/viewbybranch6.pl?AREA_ID="+ AREAID + "&gr=H"

		msgBody = getATMProbStats(table=getWidestTable(getTableList(fetchHTML(alamatURL))))

		if msgBody:

			percentAvail = getAvailBranch(AREAID)

			strColor = colorPercent(float(percentAvail))

			availText = "\nAvailability = " + percentAvail +"%\nWarna = "+ strColor 

			msgBody = strHeaderLine +"AVAILABILITY ATM\nSUPERVISI UKER: "+ AREAID.upper() +timestamp+ availText+ strHeaderLine + msgBody
			print msgBody





