#!/usr/bin/python
#---------------------------------------
# fetchStatusATMMerput.py
# (c) Jansen A. Simanullang, 11:15:55
# 27 Januari 2017 20:25:15
# to be used with telegram-bot plugin
#---------------------------------------
# usage: fetchStatusATMMerput
# script name followed by nothing
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
	#print table
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


def getTProRatih(table, strCmd):
	#print table
	# strCmd = OOS, OFF, CCR, CO, CL
	soup = BeautifulSoup(str(table))
	
	rows = soup.findAll('tr')

	numRows = getRowsNumber(table)
	numCols = getColsNumber(table)
	numRowsHead = getRowsHeadNumber(table)

	TProRatih = []
	
	for i in range (numRowsHead, numRows):

		trs = BeautifulSoup(str(rows[i]))
		tdcells = trs.findAll("td")

		
		if tdcells:

			colCMD = {"OOS":3, "OFF":4, "CCR":6, "CO":8, "CL":9}
			#print colCMD[strCmd.upper()]
			for key in colCMD:
				if tdcells[colCMD[key]].getText() == "FAIL":

					strTID = tdcells[1].getText()
					strLocation = tdcells[2].getText()
					strLocation = cleanUpLocation(strLocation)
					strReplenish, strKanca = getReplenishBy(strTID)

					strCabang = cleanupNamaUker(strKanca)
					strKodeCabang = strCabang[:4]
					strNamaCabang = strCabang[6:].strip()

					strLastTunai = tdcells[-2].getText()

					if strLastTunai:
						strLastTunai = durasiHinggaKini(strLastTunai)

					if "ATM CENTER" in strReplenish:
						intCRO = 1
						namaCROUKO = cleanUpNamaCRO(strReplenish)
					else:
						intCRO = 0
						namaCROUKO = "*"+cleanupNamaUker(strReplenish)+"*"

	
					#print strKodeCabang, namaCROUKO, intCRO, strReplenish, strLocation, strTID, strNamaCabang, strLastTunai
					TProRatih.append((strKodeCabang, strNamaCabang, key, strReplenish, str(intCRO), namaCROUKO, strTID, strLocation,  strLastTunai))
			
	TProRatih = sorted(TProRatih, key=itemgetter(1, 2, 3, 4), reverse = False)

	return TProRatih


def getTOfflineCabang(TOffline, strCmd, branchCode):

	#Initialize
	msgBody = ""
	
	TOfflineKanca = []
	TOfflineUKO = []
	TOfflineCRO = []

	for i in range(0, len(TOffline)):
		if TOffline[i][0] == branchCode.zfill(4):
			strNamaCabang = cleanupNamaUker(TOffline[i][-2])
			TOfflineKanca.append(TOffline[i])

	for i in range(0, len(TOfflineKanca)):
		if TOfflineKanca[i][2] == 0:
			TID = TOfflineKanca[i][5]
			strLastTunai = TOfflineKanca[i][-1]
			TOfflineUKO.append((TOfflineKanca[i][3], TID, strLastTunai))

	for i in range(0, len(TOfflineKanca)):
		if TOfflineKanca[i][2] == 1:
			TID = TOfflineKanca[i][5]
			strLastTunai = TOfflineKanca[i][-1]
			TOfflineCRO.append((TOfflineKanca[i][1], TOfflineKanca[i][4], TID, strLastTunai))

	if TOfflineUKO or TOfflineCRO:
		msgBody = strHeaderLine +"*ATM "+strCmd+" MERAH PUTIH "+ strNamaCabang.upper() +timestamp+ strHeaderLine + msgBody + "\n"
	else:

		msgBody = strHeaderLine +"*ATM "+strCmd+" MERAH PUTIH "+ branchCode +timestamp+ strHeaderLine + msgBody + "\nTidak ada ATM kategori ini di wilayah Anda!"

	if TOfflineUKO:
		msgBody += "*[UKO]*\n"
		for i in range(0, len(TOfflineUKO)):
			msgBody += str(i+1)+" "+ str(TOfflineUKO[i][0])+", "+str(TOfflineUKO[i][1])+"\n"
		msgBody += "\n"			

	if TOfflineCRO:
		msgBody += "*[CRO]*\n"
		for i in range(0, len(TOfflineCRO)):
			msgBody += str(i+1)+" "+ str(TOfflineCRO[i][0]) +": "+str(TOfflineCRO[i][1])+", "+str(TOfflineCRO[i][2])

			if str(TOfflineCRO[i][3]):
				msgBody += ", "+durasiHinggaKini(str(TOfflineCRO[i][3]))
			msgBody += "\n"

	return 	msgBody

def durasiHinggaKini(strDate):
	strDate = strDate.strip()
	from datetime import datetime
	format1 = '%d/%m/%Y %H:%M'
	span = datetime.now() - datetime.strptime(strDate.replace('_',' '), format1)
	return ':'.join(str(span).split('.')[:1]).replace('days','hari').replace('day','hari')


def cleanUpNamaCRO(strText):

	strText = strText.replace("ATM CENTER","")
	strText = strText.replace(")("," ")
	strText = strText.replace(")","")
	strText = strText.replace("(","")
	strText = strText.replace("BRINGIN GIGANTARA","BG")
	strText = strText.replace("BG III","BG")
	strText = strText.replace("BG II","BG")
	strText = strText.replace("SWADARMA SARANA","SSI")
	strText = strText.replace("SECURICOR","G4S")

	return strText



def cleanupNamaUker(namaUker):


	namaUker = namaUker.replace("JAKARTA","")
	namaUker = namaUker.replace("Jakarta ","") 
	namaUker = namaUker.replace("JKT ","")
	namaUker = namaUker.replace("KANCA ","")
	namaUker = namaUker.replace("KC ","")
	namaUker = namaUker.replace(")","")

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


def getReplenishBy(strTID):
	#print strTID
	alamatURL = "http://172.18.65.42/statusatm/viewatmdetail.pl?ATM_NUM="+ strTID
	table = getLargestTable(getTableList(fetchHTML(alamatURL)))
	#print table
	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')
	numRows = getRowsNumber(table)
	strCRO = ""
	strKanca = ""
	
	for i in range (0, numRows):
		trs = BeautifulSoup(str(rows[i]))
		tdcells = trs.findAll("td")
		if tdcells:

			if "Replenish By" in tdcells[0].getText():
					strReplenish = tdcells[1].getText()

			if "KC Supervisi" in tdcells[0].getText():
					strKanca = tdcells[1].getText()


	return strReplenish, strKanca


msgBody =""

timestamp = "*\nper "+ time.strftime("%d-%m-%Y pukul %H:%M")


alamatURL = "http://172.18.65.42/statusatm/viewbyupnontunai.pl?REGID=15"
alamatURL = "http://172.18.65.42/statusatm/viewbyregion3drp.pl?REGID=15"


strCmd = "OFF"
branchCode = "1144"

table=getLargestTable(getTableList(fetchHTML(alamatURL)))
TProRatih = getTProRatih(table, strCmd)

numProb = len(TProRatih)
count = 0
msgBody = ""

for i in range(0,numProb):

	strEntry = TProRatih[i][5]+", "+ TProRatih[i][6]+", "+ TProRatih[i][7]+", "+ TProRatih[i][8]
	# if same branch code
	if TProRatih[i][0] == TProRatih[i-1][0]:

		# if same problem category
		if TProRatih[i][2] == TProRatih[i-1][2]:
			#print TProRatih[i][2]
			count = count + 1
			msgBody += "\n("+str(count)+")"+strEntry


		else:
			count = 1
			msgBody += "\n"+TProRatih[i][2]+"\n("+str(count)+")"+ strEntry
		

	else:
		count = 1
		msgBody += "\n\n**ATM MERAH PUTIH**\n**"+TProRatih[i][1].upper()+" ("+TProRatih[i][0]+")**\n----------------------------\n"+ TProRatih[i][2]+ "\n("+str(count)+")"+ strEntry


print msgBody
