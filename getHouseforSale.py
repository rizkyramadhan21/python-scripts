#!/usr/bin/python
#---------------------------------------
# getRumahDijual.py
# (c) Jansen A. Simanullang
# 17.03.2016 15:55
#---------------------------------------
# usage: python getHouseforSale.py [area]
#
# example:
# python getHouseforSale.py bogor
# python getHouseforSale.py depok
#
# features:
# slow but sure crawler, avoid IP block:
# * random select fetching method:
# ** direct fetch or proxy fetch
# * random select proxy
# * random select user agent
#
# output: 
# csv file of selected area
# in OUTPUT folder
#
# main domain: rumahdijual.com
# 'rumahdijual' literally means house for sale
# 
# ALL RIGHTS RESERVED
# this script is provided as is
# without warranty or merchantability
# of any kind
# please use this script wisely
#---------------------------------------

from BeautifulSoup import BeautifulSoup
from splinter import Browser
import base64, os, sys, time, urllib2
from random import randint

alamatURL = "http://rumahdijual.com/"


def pickUserAgent():
  #
  # randomly picks user agent for crawlers
  #------------------------------------------

	customUserAgent =['Chilkat/1.0.0 (+http://www.chilkatsoft.com/ChilkatHttpUA.asp)','Mozilla/5.0 (iPhone; CPU iPhone OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A342 Safari/601.1','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36','Chilkat/1.0.0 (+http://www.chilkatsoft.com/ChilkatHttpUA.asp)','Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; Microsoft; Lumia 640 XL)','Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; Microsoft; Lumia 640 XL','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.5.2171.95 Safari/537.36']
	
	userAgent = customUserAgent[randint(0,len(customUserAgent)-1)]

	return userAgent
	
	

def directFetch(alamatURL):
	# fungsi ini hanya untuk mengambil stream string HTML dari alamat URL yang akan dimonitor
	# Content-Type utf-8 raises an error when meets strange character
	#print "fetching HTML from URL...\n", alamatURL
	
	
	try:
	
		userAgent = pickUserAgent()

		strHTML = urllib2.urlopen(urllib2.Request(alamatURL, headers={ 'User-Agent': userAgent})).read()

		strHTML = strHTML.decode("windows-1252")

		strHTML = strHTML.encode('ascii', 'ignore')

		#strHTML = cleanUpHTML(strHTML)

		mysoup = BeautifulSoup(strHTML)
		
		#print ">> URL fetched."
		
	except:
		
		print "waiting... (if the problem persists try disconnecting and reconnecting your connection without closing this window)"
		time.sleep(5)
		strHTML = proxyFetch(alamatURL)
		
	return strHTML



def getLastPage(strHTML):
  #
  # get the number of pages to crawl
  #------------------------------------------
	
	soup = BeautifulSoup(strHTML)
	pagenav = soup.find('div', {"class":"pagenav"})
	#print pagenav
	lastpage = pagenav.find('table').findAll('td')[0].getText().replace('Halaman 1 dari ','')
	
	return int(lastpage)
	
	
	
def getDatafromPage(strHTML):
  #
  # get data and dump to csv file
  #------------------------------------------
	
	soup = BeautifulSoup(strHTML)
	
	scriptDirectory = os.path.dirname(os.path.abspath(__file__)) + "/"
	
	fullPath = scriptDirectory + "OUTPUT/"
	outputfile = fullPath + AREA + ".csv"

	if not os.path.exists(fullPath):
		os.mkdir(fullPath)
		os.chdir(fullPath)

	if not os.path.isfile(outputfile):

		fileCreate(outputfile, "harga, tanah, bangunan, tidur, mandi, url\n")
		
		
  # get the premium advertised content
  
	resultset = soup.findAll('table', {"class":"tblSearchResultRow tblPremiumClass"})

	for result in resultset:
	
		tables = result.findAll('td')[0].getText()
	
		strURL = result.findAll('td')[-2].find('a')['href']
		
		strURL = correctURL(strURL) #+ ", " + strURL
		
		data = str(formatData(cleanUpText(tables))).strip("()") + ", " + strURL
		
		#if "None" not in data:
		
		fileAppend(outputfile, data+"\n")
		

	# get the forum content
	
	resultset = soup.find('table', {"id":"threadslist"}).findAll('tbody')

	for result in resultset:
	
		try:
		
			if "threadbits_forum" in result['id']:

				rows = result.findAll('tr')
				
				for row in rows:
					
					if len(row.attrs) == 0:
					
						selectedrows = row.findAll('td')
						
						for selectedrow in selectedrows:

							try:
							
								if selectedrow['class'] == 'alt1':
								
									data = selectedrow.getText()
									data = str(formatData(cleanUpText(data))).strip("()")
									
						
								if selectedrow['class'] == 'alt1 TdTitleDesc':
								
									strURL = selectedrow.find('a')['href']
									
						
							except:
							
								continue
								

						strURL = correctURL(strURL)
							
						data = data + ", " + strURL

						fileAppend(outputfile, data+"\n")

		except:
		
			continue
			

def cleanUpText(strText):
  #
  # add space for clarity
  # remove extra white space

	strText = 	strText.replace("juta"," juta")
	strText = 	strText.replace("juta","juta ")
	

	strText = 	strText.replace("miliar","miliar ")
	strText = 	strText.replace("miliar"," miliar")
	strText = 	strText.replace("m2","m2 ")
	strText = 	strText.replace("tanah", "tanah ")
	strText = 	strText.replace("bangunan", "bangunan ")
	
	strText = 	strText.replace("&nbsp;"," ")
	
	while "  " in strText:
	
		strText =	strText.replace("  "," ")

	return strText
	
	
	
def formatData(strText):
  #
  # format data

	strText = strText.split(" ")
	#print strText
	try:
		shiftIndex = 0
		if "juta" in strText:
			harga = 	int(strText[0])
		elif "miliar" in strText:
			harga = 	int(float(strText[0])*1000)
		else:
			harga = None
			shiftIndex = -2
	except:
	
		harga = None
		shiftIndex = -2
		
	try:
		tanah = None
		tanah = int(strText[2+shiftIndex])
	except:
		tanah = None
	try:
		bangunan = int(strText[5+shiftIndex])
	except:
		bangunan = None
	try:
		tidur = int(strText[8+shiftIndex])
	except:
		tidur = None
	try:	
		mandi = int(strText[9+shiftIndex])
	except:
		mandi = None
		
	return harga, tanah, bangunan, tidur, mandi
	
	
	
def fileCreate(strNamaFile, strData):
	#--------------------------------
	# fileCreate(strNamaFile, strData)
	# create a text file
	#
	f = open(strNamaFile, "w")
	f.writelines(str(strData))
	f.close()
	
	
	
def fileAppend(strNamaFile, strData):
  #
  # append data to output file
	try:
		f = open(strNamaFile, "a")
		f.writelines(str(strData))
		f.close()
	except:
		print "The file is being used in another process. Please close the file and retry..."
		fileAppend(strNamaFile, strData)


		
def proxyFetch(alamatURL):
	#
	# fetch web page via web proxy

	proxyURL = pickProxy()
	
	try:
		browser = Browser()
		browser.driver.maximize_window()

		browser.visit(proxyURL)
		
		time.sleep(2)

		browser.fill('u', alamatURL)
		
		divs = browser.find_by_value('Go').first.click()
		
		strHTML = browser.html

		time.sleep(8)
		
		strHTML = browser.html
		# uncomment this if you want to print HTML source to screen
		#strHTML = strHTML.encode('ascii', 'ignore').decode('ascii')
		#print strHTML
		
		browser.driver.close()
		
	except:
		print "retrying..."
		time.sleep(10)
		strHTML = proxyFetch(alamatURL)
	
	return strHTML
	
	
	
def pickProxy():

	#
	# random select proxy to use
	
	prox = {}
	prox['1'] = range(1,9)
	prox['2'] = range(1,4)
	prox['3'] = range(1,4)
	prox['4'] = range(1,4)
	prox['5'] = range(1,2)
	prox['6'] = range(1,2)
	prox['7'] = range(1,2)
	
	randKey = str(randint(1,len(prox)-1))
	
	if len(prox[randKey])>1:

		randIdx = randint(1, len(prox[randKey])-1)
		
	else:
	
		randIdx = 1
	
	proxyURL = "https://"+str(randKey)+".hidemyass.com/ip-"+ str(randIdx)
	
	return proxyURL
	
	
	
def decodeURL(strURL):
  #
  # return decoded URL encoded after proxy

	try:

		strURL = strURL.split("/")[-1]
		strURL = urllib2.unquote(strURL)
		strURL = strURL.decode('base64')
		strURL = "http" + strURL

	except:
	
		print strURL

	return strURL
	
	
def switchFetch(alamatURL):

	randKey = randint(1,2)
	
	if randKey == 1:
		
		print "try connecting directly...\n"
		print "try pressing ENTER here if not responding..."

		
		strHTML = directFetch(alamatURL)
		
	else:
		
		print "try connecting via web proxy...\n"
		print "try closing browser if browser not responding..."
		
		strHTML = proxyFetch(alamatURL)
		
	return strHTML
	
	
def correctURL(strURL):
  #
  # add main domain if necessary
  # decode only the encoded URL

	if ("http" not in strURL) and ("https" not in strURL):
	
		strURL = "http://rumahdijual.com/" + AREA + "/"+ strURL
		
	if "rumahdijual.com" not in strURL:
		
		strURL = decodeURL(strURL)
		
	return strURL

	
# below are the main lines of this script
if len(sys.argv) > 0:

	try:
	
		AREA = sys.argv[1]
		
	except IndexError:
	
		AREA = "depok"
	
	alamatURL= alamatURL + AREA + "/"

	msgBody = switchFetch(alamatURL)
	
	lastpage = getLastPage(msgBody)
	
	getDatafromPage(msgBody)
	
	for i in range(2, lastpage+1):
	
		cursorURL = alamatURL + "index" + str(i) + ".html"
		
		if os.name == "posix":
		
			os.system("clear")
			
		else:
		
			os.system("cls")
		
		print "fetching data from: ", cursorURL, "... "+str(i)+" from " +str(lastpage) +"\n"
	
		msgBody = switchFetch(cursorURL)
		
		getDatafromPage(msgBody)	
