#!/usr/bin/python
#---------------------------------------
# NotifikasiATMMerput.py
# (c) Jansen A. Simanullang
# 28.01.2017 13:10:40 - 08.03.2017 15:26
# to be used with cron job scheduler
#---------------------------------------
# usage: NotifikasiATMMerput
# script name followed by nothing
#---------------------------------------

from BeautifulSoup import BeautifulSoup
import os, sys, time
import urllib, urllib2, pymysql
from operator import itemgetter

atmproIP = "172.18.65.42"
regionName = "JAKARTA III"
firstURL='http://172.18.65.42/statusatm/dashboard_3.pl?ERROR=CLOSE_ST'
strHeaderLine = "\n----------------------------------------------\n"
RegionName = "JAKARTA III"
scriptDirectory = os.path.dirname(os.path.abspath(__file__)) + "/"

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


def getTProRatih(table):
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

			columnMap = {"OOS":3, "OFF":4, "CCR":6, "CO":8, "CL":9}

			for key in columnMap:

				if tdcells[columnMap[key]].getText() == "FAIL":

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


					TProRatih.append((strKodeCabang, strNamaCabang, key, strReplenish, str(intCRO), namaCROUKO, strTID, strLocation,  strLastTunai))
			
	TProRatih = sorted(TProRatih, key=itemgetter(1, 2, 3, 4), reverse = False)

	return TProRatih


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


def printMessageBody():

	msgBody =""

	timestamp = "per "+ time.strftime("%d-%m-%Y pukul %H:%M")

	alamatURL = "http://172.18.65.42/statusatm/viewbyregion3drp.pl?REGID=15"

	table=getLargestTable(getTableList(fetchHTML(alamatURL)))
	TProRatih = getTProRatih(table)

	numProb = len(TProRatih)
	count = 0
	msgBody = ""
	dictMsgBody = {}

	for i in range(0,numProb):

		strEntry = TProRatih[i][5]+", "+ TProRatih[i][6]+", "+ TProRatih[i][7]+", "+ TProRatih[i][8]

		# if same branch code
		if TProRatih[i][0] == TProRatih[i-1][0]:

			# if same problem category
			if TProRatih[i][2] == TProRatih[i-1][2]:
				#print TProRatih[i][2]
				count = count + 1
				msgBody = "\n("+str(count)+")"+strEntry
				dictMsgBody[TProRatih[i][0]] += msgBody


			else:
				count = 1
				msgBody = "\n*"+TProRatih[i][2]+"*\n("+str(count)+")"+ strEntry
				dictMsgBody[TProRatih[i][0]] += msgBody
		

		else:
			count = 1
			msgBody = "\n\n*NOTIFIKASI ATM MERAH PUTIH*\n*"+TProRatih[i][1].upper()+" ("+TProRatih[i][0]+")*\n"+timestamp+"\n----------------------------\n*"+ TProRatih[i][2]+ "*\n("+str(count)+")"+ strEntry
			dictMsgBody[TProRatih[i][0]] = msgBody

	#print msgBody
	return dictMsgBody


def TelegramBotSender(chat_id, strText):

	secretKey = "115651882:AAGDNzHXwLKNqOWmHWC8vMXg-Vy_fZD0350"

	encText=urllib.quote_plus(strText)

	strURL = "https://api.telegram.org/bot"+secretKey+"/sendMessage?parse_mode=Markdown&chat_id="+chat_id+"&text="+urllib.quote_plus(strText)
	# comment out this line below for testing purposes
	os.system('proxychains w3m -dump "'+ strURL+'"')


def NotifikasiATM():

	dictMsgBody = printMessageBody()

	print "Mengirimkan notifikasi "

	for key,value in dictMsgBody.iteritems():
	
		conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='br1j4k4rt43', db='mantel')
		cur = conn.cursor()
		cur.execute('select telegram_id from notif1 where branchcode like "'+key+'" and active="1"')


		for row in cur:

			telegram_id =(row[0])
			#------------------------------------
			# only for verbose debugging purpose
			kur = conn.cursor()
			kur.execute('select telegram_name from mantab where telegram_id="'+telegram_id+'"')

			for baris in kur:

				telegram_name = baris[0]

			kur.close()
			#print "chat_id", chat_id
			#------------------------------------

			# sending using @jak3bot
			strText = value
			print strText
			#print "\n--------------------------------------------------\n"
			print key+"--->: "+ telegram_name + "            \r"
		

			TelegramBotSender(telegram_id, value)

		cur.close()
		conn.close()

NotifikasiATM()
