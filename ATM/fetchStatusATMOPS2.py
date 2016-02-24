#!/usr/bin/python
#---------------------------------------
# fetchStatusATMOPS.py
# (c) Jansen A. Simanullang, 11:15:55
# 11.02.2016 19:05
# to be used with telegram-bot plugin
#---------------------------------------
# usage:
# fetchStatusATMOPS [TID/cro/uko/idm/alfa]
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


def getATMStatsUKO(table):

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

			if "ATM CENTER" not in tdcells[6].getText():

				seqNo = seqNo +1

				msgBody += "\n"+str(seqNo)+") " + tdcells[7].getText().upper() + "\nTID: " + tdcells[1].getText()+", " + tdcells[2].getText().replace("HYOSUNG","HYOSUNG ") +"\nLOKASI: "+ tdcells[5].getText()+"\nDURASI: "+ tdcells[8].getText().replace("days","hari ").replace("hours","jam")+"\n"
	if msgBody == "":
		msgBody = "Tidak ada ATM OPS UKO kategori ini di wilayah kerja Anda."
	return msgBody








def cleanUpLocation(strLocation):

	strLocation = strLocation.replace("JKT3","")
	strLocation = strLocation.replace("INDOMARET","IDM")
	strLocation = strLocation.replace("JAKARTA 3","")
	strLocation = strLocation.replace("JKT 3","")
	strLocation = strLocation.replace("PUBL","")
	strLocation = strLocation.strip()

	return strLocation


def getATMStatsIDM(table):

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

			if "INDOMARET" in tdcells[5].getText() or "IDM" in tdcells[5].getText() :

				seqNo = seqNo +1

				strLocation = cleanUpLocation(tdcells[5].getText())

				msgBody += "\n"+str(seqNo)+") " + "TOKO: "+ strLocation+"\n\nBRI: " + tdcells[7].getText() +"\nTID:" +tdcells[1].getText()+", " + tdcells[2].getText().replace("HYOSUNG","HYOSUNG ") +"\nDURASI: "+ tdcells[8].getText().replace("days", "hari ").replace("hours","jam") + "\n"

				if tdcells[9].getText():

					msgBody += "KETERANGAN: "+ tdcells[9].getText().lower() + "\n"

	if msgBody == "":
		msgBody = "Tidak ada ATM PROB OPS INDOMARET kategori ini di wilayah kerja Anda."

	return msgBody



def getATMStatsALFA(table):

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

			if "ALFA" in tdcells[5].getText():

				strLocation = cleanUpLocation(tdcells[5].getText())

				seqNo = seqNo +1

				msgBody += "\n"+str(seqNo)+") " + "TOKO: "+ strLocation+"\n\nBRI: " + tdcells[7].getText() +"\nTID:" +tdcells[1].getText()+", " + tdcells[2].getText().replace("HYOSUNG","HYOSUNG ") +"\nDURASI: "+ tdcells[8].getText().replace("days", "hari ").replace("hours","jam") + "\n"

				if tdcells[9].getText():

					msgBody += "KETERANGAN:\n"+ tdcells[9].getText().lower() + "\n"

	if msgBody == "":
		msgBody = "Tidak ada ATM PROB OPS ALFA kategori ini di wilayah kerja Anda."

	return msgBody









msgBody =""

timestamp = "\nper "+ time.strftime("%d-%m-%Y pukul %H:%M")

if len(sys.argv) > 0:

	AREAID = sys.argv[1]

	strHeaderLine = "\n----------------------------------------------\n"

	if AREAID.isdigit():
	

		alamatURL = "http://172.18.65.42/statusatm/viewbyoldstaggingcabang.pl?AREAID="+ AREAID + "&gr=H"

		msgBody = getATMStats(table=getWidestTable(getTableList(fetchHTML(alamatURL))))

		if msgBody:	

			msgBody = strHeaderLine +"ATM PROBLEM OPS "+ AREAID.upper() +timestamp+ strHeaderLine + msgBody
			print msgBody


	if AREAID.lower() == "cro":

		alamatURL = "http://172.18.65.42/statusatm/viewbyoldstagging.pl?REGID=15&gr=H"

		msgBody = getATMStatsCRO(table=getWidestTable(getTableList(fetchHTML(alamatURL))))

		if msgBody:	

			msgBody = strHeaderLine +"ATM PROBLEM OPS "+ AREAID.upper() +timestamp+ strHeaderLine + msgBody
			print msgBody




	if AREAID.lower() == "uko":

		alamatURL = "http://172.18.65.42/statusatm/viewbyoldstagging.pl?REGID=15&gr=H"

		msgBody = getATMStatsUKO(table=getWidestTable(getTableList(fetchHTML(alamatURL))))

		if msgBody:	

			msgBody = strHeaderLine +"ATM PROBLEM OPS "+ AREAID.upper() +timestamp+ strHeaderLine + msgBody
			print msgBody





	if AREAID.lower() == "idm":

		alamatURL = "http://172.18.65.42/statusatm/viewbyoldstagging.pl?REGID=15&gr=H"

		msgBody = getATMStatsIDM(table=getWidestTable(getTableList(fetchHTML(alamatURL))))

		if msgBody:	

			msgBody = strHeaderLine +"ATM PROBLEM OPS "+ AREAID.upper() +timestamp+ strHeaderLine + msgBody
			print msgBody





	if AREAID.lower() == "alfa":

		alamatURL = "http://172.18.65.42/statusatm/viewbyoldstagging.pl?REGID=15&gr=H"

		msgBody = getATMStatsALFA(table=getWidestTable(getTableList(fetchHTML(alamatURL))))

		if msgBody:	

			msgBody = strHeaderLine +"ATM PROBLEM OPS "+ AREAID.upper() +timestamp+ strHeaderLine + msgBody
			print msgBody


