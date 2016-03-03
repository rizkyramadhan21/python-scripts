#!/usr/bin/python
# -*- coding: utf-8 -*-
#------------------------------
# (c) Jansen A. Simanullang
# 03.03.2016 23:02 LT 16:02 UTC
# usage:
# $>python removeTags.py
# to remove tags from html
#------------------------------

import urllib2
from bs4 import BeautifulSoup

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
	
	print "\n\n>> HTML removed from tags: " + ' '.join(arrTags)
	
	return strHTML
	
def fetchHTML(alamatURL):
	#------------------------------
	# fungsi ini hanya untuk mengambil stream string HTML dari alamat URL yang akan dimonitor
	# Content-Type utf-8 raises an error when meets strange character
	#------------------------------
	#print "fetching HTML from URL...\n", alamatURL
	strHTML = urllib2.urlopen(urllib2.Request(alamatURL, headers={ 'User-Agent': 'Mozilla/5.0' })).read()

	strHTML = strHTML.decode("utf-8").encode('ascii', 'ignore')

	print ">> HTML fetched from URL: " + alamatURL
	
	print strHTML
	
	return strHTML

strHTML = fetchHTML('http://www.google.co.id/')


cleaned = removeTags(["script", "style", "div", "noscript", "iframe", "meta", "link", "span"], strHTML)
print (cleaned)
