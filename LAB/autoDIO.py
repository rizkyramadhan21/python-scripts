#-*- coding: utf-8 -*-
#!/usr/bin/python
#---------------------------------------
# autoDIO.py
# (c) Jansen A. Simanullang
# 03.03.2016 19:24
# 04.03.2016 11:40
#---------------------------------------
# usage: autoDIO
# automated digital office
# print letters to pdf then send to team
# TODO: naming convention for PDF output
#---------------------------------------


from urllib import urlopen
from BeautifulSoup import BeautifulSoup
from splinter import Browser
import os, time, urlparse, pdfkit
from Crypto.Cipher import AES
import sys
#--------------------------------
key1 = 'ἀλήθεια,καὶἡζωή'
key2 = 'Ἰησοῦς88'
key1 = key1.decode("utf-8")
key1 = key1.encode("utf-8")
key2 = key2.decode("utf-8")
key2 = key2.encode("utf-8")
#--------------------------------

if os.name == 'posix':
	os.system('clear')
else:
	os.system('cls')

def decrypt(strInput, key1, key2):
	#--------------------------------
	# decrypt(strInput, key1, key2)
	# decrypt an encrypted string with key1 and key2
	#

	obj2 = AES.new(key1, AES.MODE_CBC, key2)
	decryptedText = obj2.decrypt(strInput)

	return decryptedText



def fileCreate(strNamaFile, strData):
	#--------------------------------
	# fileCreate(strNamaFile, strData)
	# create a text file
	#
	f = open(strNamaFile, "w")
	f.writelines(str(strData))
	f.close()



def readTextFile(strNamaFile):
	#--------------------------------
	# readTextFile(strNamaFile)
	# read from a text file
	#

	fText = open(strNamaFile)
	strText = ""
					
	for baris in fText.readlines():
		strText += baris
	fText.close()

	return strText

#-------------------------------------

def getUserPass(strPasswordFile):

	strText = readTextFile(strPasswordFile)

	decryptedText = decrypt(strText, key1, key2)
	decryptedText = decryptedText.strip()

	username = decryptedText.split(":")[0]
	password = decryptedText.split(":")[1]

	return username, password


def removeTags(arrTags, strHTML):
	#------------------------------
	# remove tag(s) from strHTML
	# tags is an array of tags
	# tags = ["script","style","h1"]
	#------------------------------
	strHTML = strHTML.decode("ascii", "ignore").encode("ascii")
	beSoup = BeautifulSoup(strHTML)
	
	for tag in beSoup(arrTags):
	
		tag.extract()
	
	strHTML = str(beSoup)
	
	#strHTML = ''.join(strHTML.splitlines())
	
	print "\n\n>> HTML removed from tag(s): " + ' '.join(arrTags)
	
	return strHTML




def getTanggalPerihal(strHTML):
	#--------------------------------
	# getTanggalPerihal(strHTML)
	# TODO: get from Table Surat Masuk
	strPerihal = ""
	strTanggal = ""
	HTMLSoup = BeautifulSoup(strHTML)
	strHTML = HTMLSoup.findAll("table", {"class" : "isi_surat"})

	HTMLSoup = BeautifulSoup(str(strHTML))
	strHTML = HTMLSoup.findAll("div",{"align":"left"})

	for i in range (0, len(strHTML)):
		
		dText = strHTML[i].getText()

		if "PERIHAL" in dText.upper():

			strPerihal = strHTML[i+2].getText()
			print "Perihal: " + strPerihal

		if "TANGGAL" in dText.upper():

			strTanggal = strHTML[i+2].getText()
			print "Tanggal: " + strTanggal


	return strTanggal, strPerihal




def makeFileName(strHTML):

	strTanggal, strPerihal = getTanggalPerihal(strHTML)

	strFileName = strTanggal + "-" + strPerihal

	return strFileName




def createTeam():
	TeamMembers = dict()
	TeamMembers["TSI"] = ["00001663","00067001","00069929","90096903","90101069","90102622","90103433","90106652","90113057"]
	TeamMembers["EDC"] = ["00085983","00067001","00069929","00206857","90113059","90114084","90115648"]
	TeamMembers["ATM"] = ["00060074","00067001","00069929","00169079","90091648","90102623","90103436"]
	TeamMembers["ALL"] = ["00001663","00060074", "00067001","00069929", "00085983"]

	return TeamMembers


TeamMembers = createTeam()

def mapTerms():

	teamTerms = dict()

	teamTerms["TSI"] = ["BUZZ", "PC", "VSAT", "V-SAT", "WEB", "LAS"]
	teamTerms["EDC"] = ["EDC"]
	teamTerms["ATM"] = ["ATM", "PONSEL", "HP"]
	teamTerms["ALL"] = ["RISIKO", "PULSA", "IT", "DEVICE", "PEMBERITAHUAN"]

	return teamTerms

TermsMap = mapTerms()


def findTeam(strKeyword, TermsMap):

	teamName = "ALL"
	
	for k,v in TermsMap.iteritems():

		if strKeyword in ' '.join(v):
		
			print "we got the keyword '" + strKeyword + "' that must be disposed to team: " + k

			teamName = k
		
			return teamName		
	


def getInbox(strHTML):

	soup = BeautifulSoup(strHTML)
	table = soup.findAll("table", {"class" : "boxsurat table table-striped table-hover table-condensed table-responsive table-bordered"})
	soup = BeautifulSoup(str(table))

	rows = soup.findAll("tr")
	read = soup.findAll("tr", {"status-baca":"Y"})
	unread = soup.findAll("tr", {"status-baca":"N"})
	
	soup = BeautifulSoup(str(rows[0]))
	headers = soup.findAll('th')
	
	colheaders = [] * len(headers)

	for i in range (0, len(headers)):

		colheaders.append(str(headers[i].getText()))

	return read, unread, colheaders



read, unread, colheaders = getInbox(readTextFile("inbox.html"))



def getLetter(read):
	
	print "letter to process: ", len(read)
	Letters = [] * len(read)

	for i in range(0, len(read)):
		
		tds = read[i].findAll('td')
		id = read[i].get('id')
		strPerihal = tds[colheaders.index('Perihal')].get('title').strip()
		strTanggal = tds[colheaders.index('Tanggal')].getText()

		strPerihal = strPerihal.replace("/"," ")
		strPerihal = strPerihal.replace("&amp;","&")

		if "Hari Ini" in strTanggal:

			strTanggal = time.strftime("%d-%m-%Y")

		Letters.append(str(id)+"|"+strPerihal+"|"+strTanggal)

	return Letters


username, password = getUserPass(".pass")


def login(username, password):
	#--------------------------------
	# login(username, password)
	# uncomment below only for debugging, do not use at production
	# print username, len(username), password, len(password)
	#
	browser = Browser()
	browser.driver.maximize_window()

	browser.visit('https://bristars.bri.co.id/bristars/user/login')
	
	button = browser.find_by_xpath("//button")
	time.sleep(1)
	button.last.click()
	#
	# why last button to be clicked?
	# because it is the last button which contains 'x'
	# i= 0
	# for abutton in button:
	#	i += 1
	#	print abutton.text, i
	time.sleep(2)

	browser.fill('pernr', username)
	browser.fill('password', password)

	browser.find_by_name("login").first.click()
	time.sleep(2)
	
	browser.visit('https://bristars.bri.co.id/bristars/menus/childs/MTE%3D')
	time.sleep(1)
	browser.find_by_text(" Digital Office DiO [A]").first.click()
	time.sleep(2)
	browser.visit('http://172.18.65.190/eoffice/surat/surat_masuk')
	time.sleep(1)

	strHTML = browser.html
	read, unread, colheaders = getInbox(strHTML)
	anyReadUnread = len(read)+len(unread)

	while (anyReadUnread):
	
		print "loop continues"
		#----------------------------------------------------------------
		# cek surat yang belum dibaca
		#----------------------------------------------------------------
		if len(unread):

			divs = browser.find_by_xpath('//div[@class="list-group"]')
			trs = divs.find_by_xpath('//tr[@status-baca="N"]')

			Letters = getLetter(unread)
			strPerihal = Letters[0].split("|")[1]
			strTanggal = Letters[0].split("|")[2]
	

		#----------------------------------------------------------------
		# cek surat yang sudah dibaca
		#----------------------------------------------------------------
		if len(read):

			divs = browser.find_by_xpath('//div[@class="list-group"]')
			trs = divs.find_by_xpath('//tr[@status-baca="Y"]')
			Letters = getLetter(read)
			strPerihal = Letters[0].split("|")[1]
			strTanggal = Letters[0].split("|")[2]
		
		print strPerihal
		trs.first.click()
		browser.driver.execute_script("window.scrollTo(0, 0)")
		time.sleep(3)
		browser.find_by_text("LIHAT INFORMASI SURAT").first.click()
		time.sleep(1)

		#----------------------------------------------------------------
		# clicking available button for demonstration purposes
		#----------------------------------------------------------------
	
		# button = browser.find_by_id('lihat')
		# print button.text
		# time.sleep(3)
		# button.click()

		# button = browser.find_by_id('sembunyi')
		# print button.text
		# time.sleep(3)
		# button.click()

		window_before = browser.driver.window_handles[0]

		#----------------------------------------------------------------
		# clicking the print button
		#----------------------------------------------------------------
	
	
		divs = browser.find_by_xpath('//div[@class="pull-right"]')
		button = divs.find_by_id('btn_print')
		print button.text
		time.sleep(3)
		divs.first.click()
		time.sleep(3)

		window_after = browser.driver.window_handles[1]

		#----------------------------------------------------------------
		# switch to another window, grab the HTML, remove 'script' tag, 
		# dump cleaned HTML to HTML file, convert HTML file to PDF
		#----------------------------------------------------------------

		browser.driver.switch_to_window(window_after)

		strHTML = browser.html
		strHTML = strHTML.encode('ascii', 'ignore').decode('ascii')

		strNamaFile = "result.html"
		strHTML = removeTags(["script"], strHTML)

		fileCreate(strNamaFile, str(strHTML))
		strNamaFile = strTanggal+"-" + strPerihal + '.pdf'
	
		pdfkit.from_file("/home/administrator/NOTIFIKASI/LAB/result.html", strNamaFile)
		browser.driver.close()

		browser.driver.switch_to_window(window_before)
		print browser.driver.current_url

		#----------------------------------------------------------------
		# DISPOSITION
		#----------------------------------------------------------------

		button = browser.find_by_xpath('//button[text()="Disposisi"]')
		print button.text
		time.sleep(1)
		button.click()

		button = browser.find_by_xpath('//input[@value="banyak"]')
		button.click()

		element = browser.find_by_xpath('//select[@id="banyak"]//option').last.click()

		element = browser.find_by_xpath('//input[@id="pilih_banyak"]').click()
	
		element = browser.find_by_xpath('//input[@class="banyak"]')

		#----------------------------------------------------------------
		# Find the team name to be disposed of the letters
		#----------------------------------------------------------------
	
		Keywords = ["ATM","EDC","IT", "BUZZ", "PONSEL", "VSAT", "PC", "V-SAT", "RISIKO", "PEMBERITAHUAN", "HP"]

		Words = strPerihal.upper().split(" ")

		for keyword in Keywords:

			for word in Words:
				print word, keyword
				if word == keyword :

					teamName = findTeam(keyword, TermsMap)

					print teamName, word

		#----------------------------------------------------------------
		# clicking the name of each worker
		#----------------------------------------------------------------

		for elem in element:

			for team in TeamMembers[teamName]:
			
				if elem["value"] == team:

					print team, elem["value"], "--> box checked"

					elem.click()
					time.sleep(2)

		browser.fill("CATATAN_BANYAK", strPerihal+ " - Disposisi by bot")

	

		button = browser.find_by_xpath('//button[@id="btn_proses"]')
		print button.text
		time.sleep(1)
		button.click()
		time.sleep(1)
		#----------------------------------------------------------------
		# LOOP ENDS HERE
		# back to loop until all letters read and disposed
		#----------------------------------------------------------------
		browser.visit('http://172.18.65.190/eoffice/surat/surat_masuk')
		time.sleep(3)
		strHTML = browser.html
		read, unread, colheaders = getInbox(strHTML)				
		anyReadUnread = len(read)+len(unread)

	browser.driver.close()




login(username, password)
