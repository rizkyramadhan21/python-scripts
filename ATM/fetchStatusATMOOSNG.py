#!/usr/bin/python
#---------------------------------------
# fetchStatusATMOOSNG.py
# (c) Jansen A. Simanullang, 11:15:55
# 14 Januari 2016 09:04:11
# 13 Agustus 2016 13:58:28 - 15:30, 16:33
# 15 Agustus 2016 20:46 detail durasi hingga kini
# 20.08.2016 16:04
# to be used with telegram-bot plugin
#---------------------------------------
# usage: fetchStatusATMOOSNG cro/uko/kode cabang
# script name followed by cro/uko or branchCode
#---------------------------------------

from BeautifulSoup import BeautifulSoup
import sys, time
import urllib2
from operator import itemgetter

atmproIP = "172.18.65.42"
regionName = "JAKARTA III"
strHeaderLine = "\n----------------------------------------------\n"

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


def getTOutOS(table):

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')
	numRows = getRowsNumber(table)
	numCols = getColsNumber(table)
	numRowsHead = getRowsHeadNumber(table)

	#Initialize
	TOutOS = []
	
	for i in range (0, numRows):

		trs = BeautifulSoup(str(rows[i]))
		tdcells = trs.findAll("td")
		thcells = trs.findAll("th")

		if tdcells:
			strTID = tdcells[1].getText()
			strLocation = tdcells[5].getText()
			strLocation = cleanUpLocation(strLocation)
			strArea = tdcells[6].getText()

			if "ATM CENTER" in strArea:
				intCRO = 1
				namaCROUKO = cleanUpNamaCRO(strArea)
			else:
				intCRO = 0
				namaCROUKO = cleanupNamaUker(strArea)
				
			strCabang = tdcells[7].getText()
			strKodeCabang = strCabang[:4]
			strNamaCabang = strCabang[6:]
			TOutOS.append((strKodeCabang, namaCROUKO, intCRO, strArea, strLocation, strTID, strNamaCabang))

	TOutOS = sorted(TOutOS, key=itemgetter(1, 3, 2), reverse = False)

	return TOutOS 


def getTOutOSCabang(TOutOS, branchCode):

	#Initialize
	msgBody = ""
	
	TOutOSKanca = []
	TOutOSUKO = []
	TOutOSCRO = []

	for i in range(0, len(TOutOS)):
		if TOutOS[i][0] == branchCode.zfill(4):
			strNamaCabang = cleanupNamaUker(TOutOS[i][-1])
			TOutOSKanca.append(TOutOS[i])

	for i in range(0, len(TOutOSKanca)):
		if TOutOSKanca[i][2] == 0:
			TID = TOutOSKanca[i][5]
			TOutOSUKO.append((TOutOSKanca[i][3], TID, getLastTunai(TID)))

	for i in range(0, len(TOutOSKanca)):
		if TOutOSKanca[i][2] == 1:
			TID = TOutOSKanca[i][5]
			TOutOSCRO.append((TOutOSKanca[i][1], TOutOSKanca[i][4], TID, getLastTunai(TID)))

	if TOutOSUKO or TOutOSCRO:
		msgBody = strHeaderLine +"ATM OOS G "+ strNamaCabang.upper() +timestamp+ strHeaderLine + msgBody + "\n"
	else:

		msgBody = strHeaderLine +"ATM OOS G "+ branchCode +timestamp+ strHeaderLine + msgBody + "\nTidak ada ATM kategori ini di wilayah Anda!"

	if TOutOSUKO:
		msgBody += "[UKO]\n"
		for i in range(0, len(TOutOSUKO)):
					msgBody += str(i+1)+" "+ str(TOutOSUKO[i][0])+", "+str(TOutOSUKO[i][1])+", "+durasiHinggaKini(str(TOutOSUKO[i][2]))+"\n"
		msgBody += "\n"			

	if TOutOSCRO:
		msgBody += "[CRO]\n"
		for i in range(0, len(TOutOSCRO)):
					msgBody += str(i+1)+" "+ str(TOutOSCRO[i][0]) +": "+str(TOutOSCRO[i][1])+", "+str(TOutOSCRO[i][2])+", "+durasiHinggaKini(str(TOutOSCRO[i][3]))+"\n"

	return 	msgBody


def getTOutOSCRO(TOutOS, selectedCRO):

	#Initialize
	msgBody = ""
	seqNo = 0
	counter = 0
	TOutOSCRO = []
	arrCRO = ["BG", "G4S", "KEJAR", "SSI", "TAG"]

	if selectedCRO == 0:

		selectedCRO = "ALL"
		strCRO = "[ALL CRO]"

		for i in range(0, len(TOutOS)):
			if TOutOS[i][2] == 1:
				strNamaCabang = cleanupNamaUker(TOutOS[i][-1])
				TID = TOutOS[i][5]
				TOutOSCRO.append((TOutOS[i][1], TOutOS[i][4], TID, getLastTunai(TID)))

	elif selectedCRO in arrCRO:

		arrCRO = [""]
		arrCRO.append(selectedCRO)
		strCRO = "["+selectedCRO+"]"
	
		for i in range(0, len(TOutOS)):

			if TOutOS[i][1] == selectedCRO:
				strNamaCabang = cleanupNamaUker(TOutOS[i][-1])
				TID = TOutOS[i][1]
				TOutOSCRO.append((TOutOS[i][1], TOutOS[i][4], TID, getLastTunai(TID)))

	if TOutOSCRO:

		msgBody += strCRO+"\n"

		if len(TOutOSCRO) <= 2:
				msgBody +=  "\n["+str(TOutOSCRO[0][0]) + "]\n"

		for i in range(0, len(TOutOSCRO)):

			if TOutOSCRO[i-1][0] != TOutOSCRO[i][0]:
				msgBody += "\n[" + str(TOutOSCRO[i][0]) + "]\n"
				seqNo = 0

			for j in range(0, len(arrCRO)):

				if str(TOutOSCRO[i][0]) == arrCRO[j]:
					seqNo += 1
					counter += 1
					msgBody += str(seqNo)+") "+ str(TOutOSCRO[i][1])+", "+str(TOutOSCRO[i][2])+", "+durasiHinggaKini(str(TOutOSCRO[i][3]))+"\n"

		msgBody += "\n"+regionName + "-[TOTAL OOS CRO "+selectedCRO+"]: "+str(counter)

	return 	msgBody


def getTOutOSUKO(TOutOS):

	#Initialize
	msgBody = ""
	seqNo = 0
	counter = 0
	TOutOSUKO = []

	for i in range(0, len(TOutOS)):
	
		if TOutOS[i][2] == 0:
			strNamaCabang = cleanupNamaUker(TOutOS[i][-1])
			TID = TOutOS[i][5]
			TOutOSUKO.append((strNamaCabang.upper(), TOutOS[i][4], TID, getLastTunai(TID)))

	TOutOSUKO = sorted(TOutOSUKO, key=itemgetter(0), reverse = False)

	if TOutOSUKO:
	
		msgBody += "[UKO]\n"
		for i in range(0, len(TOutOSUKO)):
			if TOutOSUKO[i-1][0] != TOutOSUKO[i][0]:
				msgBody +=  "\n"+str(TOutOSUKO[i][0]) + "\n"
				seqNo = 0

			seqNo += 1
			counter += 1
			msgBody += str(seqNo)+") "+ str(TOutOSUKO[i][1])+", "+str(TOutOSUKO[i][2])+", "+durasiHinggaKini(str(TOutOSUKO[i][3]))+"\n"

		msgBody += "\n"+regionName + "-[TOTAL OOS UKO]: "+str(counter)

	return 	msgBody


def getTOutOSACI(TOutOS, selectedACI):

	msgBody = ""
	seqNo = 0
	counter = 0
	TOutOSACI = []

	for i in range(0, len(TOutOS)):

		if selectedACI in TOutOS[i][4]:
			seqNo += 1
			strNamaCabang = cleanupNamaUker(TOutOS[i][-1])
			TID = TOutOS[i][5]
			strLocation = TOutOS[i][4]
			TOutOSACI.append((strNamaCabang.upper(), strLocation, TID, getLastTunai(TID)))

	TOutOSACI = sorted(TOutOSACI, key=itemgetter(0), reverse = False)
	seqNo = 0
	if TOutOSACI:

		if len(TOutOSACI) == 1:
				msgBody +=  "\n"+str(TOutOSACI[0][0]) + "\n"

		for i in range(0, len(TOutOSACI)):
			if TOutOSACI[i-1][0] != TOutOSACI[i][0]:
				msgBody +=  "\n"+str(TOutOSACI[i][0]) + "\n"
				seqNo = 0
			seqNo += 1
			counter += 1
			msgBody += str(seqNo)+") "+ str(TOutOSACI[i][1])+", "+str(TOutOSACI[i][2])+", "+durasiHinggaKini(str(TOutOSACI[i][3]))+"\n"

		msgBody += "\n"+regionName + "-[TOTAL OOS "+selectedACI.upper()+"]: "+str(counter)

	return 	msgBody


def cleanUpNamaCRO(strText):

	strText = strText.replace("ATM CENTER","")
	strText = strText.replace("(","")
	strText = strText.replace(")","")
	strText = strText.replace("BRINGIN GIGANTARA","BG")
	strText = strText.replace("BG III","BG")
	strText = strText.replace("BG II","BG")
	strText = strText.replace("SWADARMA SARANA","SSI")
	strText = strText.replace("SECURICOR","G4S")

	return strText.strip()

def cleanupNamaUker(namaUker):


	namaUker = namaUker.replace("JAKARTA","")
	namaUker = namaUker.replace("Jakarta ","") 
	namaUker = namaUker.replace("JKT ","")
	namaUker = namaUker.replace("KANCA ","")
	namaUker = namaUker.replace("KC ","")

	return namaUker.strip()

def cleanUpLocation(strLocation):

	strLocation = strLocation.replace("JKT3","")
	strLocation = strLocation.replace("INDOMARET","IDM")
	strLocation = strLocation.replace("JAK 3","")
	strLocation = strLocation.replace("JAKARTA 3","")
	strLocation = strLocation.replace("JAKARTA 1","")
	strLocation = strLocation.replace("JAKARTA3","")
	strLocation = strLocation.replace("KANWIL 3","")
	strLocation = strLocation.replace("JAKARTA","")
	strLocation = strLocation.replace("JKT 3","")
	strLocation = strLocation.replace("JKT","")
	strLocation = strLocation.replace("PUBL","")
	strLocation = strLocation.replace("G4S ","")
	strLocation = strLocation.replace("TAG ","")
	strLocation = strLocation.replace("SSI ","")
	strLocation = strLocation.replace("CRO ","")
	strLocation = strLocation.replace("-","")
	strLocation = strLocation.strip()

	return strLocation

def getLastTunai(TID):

	alamatURL = "http://172.18.65.42/statusatm/viewatmdetail.pl?ATM_NUM="+ TID
	table = getLargestTable(getTableList(fetchHTML(alamatURL)))

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')
	numRows = getRowsNumber(table)
	msgBody = ""
	
	for i in range (0, numRows):
		trs = BeautifulSoup(str(rows[i]))
		tdcells = trs.findAll("td")
		if tdcells:
			if "TUNAI" in tdcells[0].getText().upper() :
					msgBody += tdcells[0].getText().upper()+": "+ tdcells[1].getText() +"\n"

	return msgBody.replace("SUKSES TRX. TUNAI:","").strip()


def durasiHinggaKini(strDate):

	from datetime import datetime
	format1 = '%d/%m/%Y %H:%M'
	span = datetime.now() - datetime.strptime(strDate.replace('_',' '), format1)
	return ':'.join(str(span).split('.')[:1]).replace('days','hari')



msgBody =""

timestamp = "\nper "+ time.strftime("%d-%m-%Y pukul %H:%M")

if len(sys.argv) > 0:

	alamatURL = "http://atmpro.bri.co.id/statusatm/viewbyregionprobooscr.pl?REGID=15&ERROR=CLOSE_ST&gr=N"

	try:
		AREAID = sys.argv[1]

		if AREAID.isdigit():

			TOutOS = getTOutOS(table=getWidestTable(getTableList(fetchHTML(alamatURL))))
			msgBody = getTOutOSCabang(TOutOS, AREAID)

			if msgBody:	
				print msgBody

	
		if AREAID[0].isalpha():

			if AREAID.upper() == "UKO":

				try:

					TOutOS = getTOutOS(table=getWidestTable(getTableList(fetchHTML(alamatURL))))
					msgBody = getTOutOSUKO(TOutOS)

					if msgBody:	
						msgBody = strHeaderLine +"ATM OOS NG "+ AREAID.upper() + " - "+regionName+ timestamp+ strHeaderLine + msgBody
						print msgBody

				except:
					print "Ada kesalahan."

			elif AREAID.upper() == "CRO":

				try:

					TOutOS = getTOutOS(table=getWidestTable(getTableList(fetchHTML(alamatURL))))
					msgBody = getTOutOSCRO(TOutOS, 0)

					if msgBody:	
						msgBody = strHeaderLine +"ATM OOS NG "+ AREAID.upper() + " - "+regionName+ timestamp+ strHeaderLine + msgBody
						print msgBody

				except:
					print "Ada kesalahan."

			else:

				try:

					TOutOS = getTOutOS(table=getWidestTable(getTableList(fetchHTML(alamatURL))))
					msgBody = getTOutOSACI(TOutOS, AREAID.upper())

					if msgBody:	
						msgBody = strHeaderLine +"ATM OOS NG "+ AREAID.upper() + " - "+regionName+ timestamp+ strHeaderLine + msgBody
						print msgBody

				except:
					print "CRO tidak dikenal."

	except:

		print "ANDA belum meng-input kode UKO/ CRO."
