#-*- coding: utf-8 -*-
#!/usr/bin/python
#---------------------------------------
# autoDIO.py
# Automated Digital Office
# (c) Jansen A. Simanullang
# 03.03.2016 19:24
# 07.03.2016 17:35
# 28.03.2016 16:17 disposisi_masuk
#---------------------------------------
# usage:
# python autoDIO.py
#
# TODO: send PDF via Telegram to team
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
defaultTeamName = "ALL"
scriptRoot = os.path.dirname(os.path.abspath(__file__)) + os.sep
#--------------------------------

if os.name == 'posix':
	os.system('clear')
else:
	os.system('cls')


def encrypt(strInput, key1, key2):
	#--------------------------------
	# encrypt(strInput, key1, key2)
	# encrypt a string input with key1 and key2
	#
	key1 = key1.decode("utf-8")
	key1 = key1.encode("utf-8")

	obj = AES.new(key1, AES.MODE_CBC, key2)

	remainder = len(strInput)/16.0 - len(strInput)/16 
	quotient = len(strInput)/16

	if remainder:
		message = strInput.ljust(16*(quotient+1))



	encryptedText = obj.encrypt(message)

	return encryptedText

def createPass():

	username = str(input('Enter your 8 digit personal number: '))
	username = username.zfill(8)
	print username
	password = str(raw_input('Enter your BRISTARS password: '))
	strInput = username + ":" + password
	encryptedText = encrypt(strInput, key1, key2)
	fileCreate(".pass",encryptedText)

	return username, password

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

	teamTerms["TSI"] = ["BUZZ", "PC", "VSAT", "V-SAT", "WEB", "LAS", "VIRUS"]
	teamTerms["EDC"] = ["EDC"]
	teamTerms["ATM"] = ["ATM", "CDM", "CRM", "PONSEL", "HP"]
	teamTerms["ALL"] = ["RISIKO", "PULSA", "IT", "DEVICE", "PEMBERITAHUAN", "RELOKASI", "BISS", "PENDAFTARAN", "SECURITY", "PERMOHONAN"]

	return teamTerms

TermsMap = mapTerms()


def findTeam(strKeyword, TermsMap):

	teamName = "ALL"
	
	for k,v in TermsMap.iteritems():

		if strKeyword in ' '.join(v):
		
			print "we got the keyword '" + strKeyword + "' that must be disposed to team: " + k

			teamName = k
		
	return teamName		
	

def allKeywords(TermsMap):

	Keywords = []
	
	for k,vs in TermsMap.iteritems():

		for v in vs:

			Keywords.append(v)
		
	return sorted(Keywords)



def getInbox(k, strHTML):

	soup = BeautifulSoup(strHTML)

	if k == 'surat_masuk':
		class_table = "boxsurat table table-striped table-hover table-condensed table-responsive table-bordered"
	elif k == 'disposisi_masuk':
		class_table = "boxsurat table table-hover table-condensed table-responsive table-bordered"

	table = soup.findAll("table", {"class" : class_table})
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

try:
	username, password = getUserPass(".pass")
except:
	createPass()
	print "User and password has been saved to .pass file.\nPlease delete the file if you want to change your credentials."
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
	time.sleep(3)
	
	browser.visit('https://bristars.bri.co.id/bristars/menus/childs/MTE%3D')
	time.sleep(1)
	browser.find_by_text(" Digital Office DiO [A]").first.click()
	time.sleep(2)

	Inbox = {'surat_masuk':'http://172.18.65.190/eoffice/surat/surat_masuk', 'disposisi_masuk':'http://172.18.65.190/eoffice/disposisi/disposisi_masuk'}

	for k, v in Inbox.iteritems():

		browser.visit(v)
		time.sleep(1)

		strHTML = browser.html
		global colheaders

		read, unread, colheaders = getInbox(k, strHTML)

		if k == 'surat_masuk':
			anyReadUnread = len(read)+len(unread)

		if k == 'disposisi_masuk':
			anyReadUnread = len(unread)

		while (anyReadUnread):
	
			print "loop continues", k, len(unread)
			#----------------------------------------------------------------
			# cek surat yang belum dibaca
			#----------------------------------------------------------------
			if len(unread):

				divs = browser.find_by_css('.boxsurat')
				trs = divs.find_by_xpath('//tr[@status-baca="N"]')

				Letters = getLetter(unread)
				strPerihal = Letters[0].split("|")[1]
				strTanggal = Letters[0].split("|")[2]

			#----------------------------------------------------------------
			# cek surat masuk yang sudah dibaca namun belum disposisi
			#----------------------------------------------------------------
			if len(read) and k == 'surat_masuk':

				divs = browser.find_by_css('.boxsurat')
				trs = divs.find_by_xpath('//tr[@status-baca="Y"]')
				Letters = getLetter(read)
				strPerihal = Letters[0].split("|")[1]
				strTanggal = Letters[0].split("|")[2]
		
			print strPerihal

			trs.first.click()

			browser.driver.execute_script("window.scrollTo(0, 0)")
			time.sleep(5)
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
	
			pdfkit.from_file(scriptRoot + "result.html", "OUTPUT/"+strNamaFile)
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

			option = browser.find_by_xpath('//select[@id="banyak"]//option')

			for i in range(0, len(option)):

				if tujuanDisposisi.upper() in option[i].text:
			
					idxOption = i

			option[idxOption].click()

			element = browser.find_by_xpath('//input[@id="pilih_banyak"]').click()
	
			element = browser.find_by_xpath('//input[@class="banyak"]')

			#----------------------------------------------------------------
			# Find the team name to be disposed of the letters
			#----------------------------------------------------------------
	
			Keywords = allKeywords(TermsMap)

			Words = strPerihal.upper().split(" ")

			teamName = defaultTeamName

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
						time.sleep(1)

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
			browser.visit(v)
			time.sleep(4)
			strHTML = browser.html
			read, unread, colheaders = getInbox(k, strHTML)

			if k == 'surat_masuk':
				anyReadUnread = len(read)+len(unread)

			if k == 'disposisi_masuk':
				anyReadUnread = len(unread)



	browser.driver.close()



tujuanDisposisi = 'pekerja' # atau 'pimpinan'

login(username, password)
