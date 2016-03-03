#-*- coding: utf-8 -*-
#!/usr/bin/python
#---------------------------------------
# autoDIO.py
# (c) Jansen A. Simanullang
# 03.03.2016 19:24
#---------------------------------------
# usage: autoDIO
# automated digital office
# print letters to pdf then send to team
# TODO: remove '<script>' tag from HTML
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


username, password = getUserPass(".pass")


def login(username, password):
	#--------------------------------
	#login(username, password)
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
	time.sleep(1)

	browser.fill('pernr', username)
	browser.fill('password', password)

	browser.find_by_name("login").first.click()
	time.sleep(2)
	
	browser.visit('https://bristars.bri.co.id/bristars/menus/childs/MTE%3D')
	time.sleep(1)
	browser.find_by_text(" Digital Office DiO [A]").first.click()
	time.sleep(1)
	browser.visit('http://172.18.65.190/eoffice/surat/surat_masuk')
	time.sleep(2)
	#----------------------------------------------------------------
	# cek surat yang belum dibaca
	#----------------------------------------------------------------

	divs = browser.find_by_xpath('//div[@class="list-group"]')
	trs = divs.find_by_xpath('//tr[@status-baca="N"]')
	#print trs.text

	print "------------------------------------------------"
	print "Surat yang belum dibaca"
	print "------------------------------------------------"
	for tr in trs:
		try:
			print tr.text
			if "ATM" in tr.text:
				print "DISPOSISI KE SIE ATM"
			elif "EDC" in tr.text:
				print "DISPOSISI KE SIE EDC"
			elif "HP" in tr.text:
				print "DISPOSISI KE SIE ATM"
			else:
				print "DISPOSISI KE STAFF"

		except:
			pass

	#----------------------------------------------------------------
	# cek surat yang sudah dibaca
	#----------------------------------------------------------------

	divs = browser.find_by_xpath('//div[@class="list-group"]')
	trs = divs.find_by_xpath('//tr[@status-baca="Y"]')
	#print trs.text
	#time.sleep(1)
	print "------------------------------------------------"
	print "Surat yang sudah dibaca namun belum terdisposisi"
	print "------------------------------------------------"
	for tr in trs:
		try:
			dText = tr.text
			print dText
			if "ATM" in dText:
				print "DISPOSISI KE SIE ATM"
			elif "EDC" in dText:
				print "DISPOSISI KE SIE EDC"
			elif "HP" in dText.upper():
				print "DISPOSISI KE SIE ATM"
			elif "PONSEL" in dText.upper():
				print "DISPOSISI KE SIE ATM"
			else:
				print "DISPOSISI KE STAFF"

		except:
			pass

	time.sleep(2)
	trs.first.click()
	time.sleep(2)
	browser.find_by_text("LIHAT INFORMASI SURAT").first.click()
	time.sleep(1)
	
	button = browser.find_by_id('lihat')
	print button.text
	time.sleep(3)
	button.click()
	button = browser.find_by_id('sembunyi')
	print button.text
	time.sleep(3)
	button.click()

	window_before = browser.driver.window_handles[0]

	#----------------------------------------------------------------
	# cetak surat
	#----------------------------------------------------------------
	
	
	divs = browser.find_by_xpath('//div[@class="pull-right"]')
	button = divs.find_by_id('btn_print')
	print button.text
	time.sleep(3)
	divs.first.click()
	time.sleep(3)

	window_after = browser.driver.window_handles[1]

	#----------------------------------------------------------------
	# pindah window
	#----------------------------------------------------------------


	browser.driver.switch_to_window(window_after)

	#----------------------------------------------------------------
	# cetak PDF
	#----------------------------------------------------------------
	
	strHTML = browser.html
	strHTML = strHTML.encode('ascii', 'ignore').decode('ascii')
	print strHTML
	strNamaFile = "result.html"
	fileCreate(strNamaFile, str(strHTML))
	pdfkit.from_file("/home/administrator/NOTIFIKASI/LAB/result.html", 'out.pdf')

	browser.driver.close()


login(username, password)
