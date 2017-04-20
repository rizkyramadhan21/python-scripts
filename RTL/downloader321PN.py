#-*- coding: utf-8 -*-
#!/usr/bin/python
#---------------------------------------
# portaldwh.py
# Automated Downloader
# (c) Rizky Ramadhan
# 20 April 2017 
#---------------------------------------
# usage:
# python tugasdariPinwil.py
#---------------------------------------


from urllib import urlopen
from BeautifulSoup import BeautifulSoup
from splinter import Browser
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import os, sys, math, time, xlrd
from os import listdir
from os.path import isfile, join

#--------------------------------
scriptRoot = os.path.dirname(os.path.abspath(__file__)) + os.sep
downloadPath = '/path/To/Downloads/'
downDir = '/Path/To/Save/Dir/'
#--------------------------------

if os.name == 'posix':
	os.system('clear')
else:
	os.system('cls')



def downloadReport(downDir):
	#--------------------------------
	browser = Browser('chrome')
	#--------------------------------
	browser.driver.maximize_window()

	browser.visit('http://url yg akan dituju')

	# Click Cabang yang Bersangkutan
	selector = '#ReportViewerControl_ctl00_ctl05_ddValue > option:nth-child(9)'
	browser.find_by_css(selector).click()
	mainBranch=browser.find_by_css(selector).text.strip()
	print "running loop KANCA UTAMA: ", mainBranch
	time.sleep(3)

	# Click to Activate Uker Binaan
	selector = '#ReportViewerControl_ctl00_ctl07'
	browser.find_by_css(selector).click()
	time.sleep(2)

	# Click to Activate selector Uker Binaan
	selector = '#ReportViewerControl_ctl00_ctl07_divDropDown > table > tbody > tr:nth-child(1)'

	# Click Select All Uker Binaan Kanca
	selector = '#ReportViewerControl_ctl00_ctl07_divDropDown > table > tbody > tr:nth-child(1) > td > span > label'
	browser.find_by_css(selector).click()

	# Click Periode -> CHILD 2 = 2 yaitu Rows dibawah select Periode
	selector = '#ReportViewerControl_ctl00_ctl09_ddValue > option:nth-child(2)'
	browser.find_by_css(selector).click()

	# View Report
	selector = '#ReportViewerControl_ctl00_ctl00'
	browser.find_by_css(selector).click()

	# Select Format Excel
	selector = '#ReportViewerControl_ctl01_ctl05_ctl00 > option:nth-child(7)'
	browser.find_by_css(selector).click()

	# Click EXPORT
	selector = '#ReportViewerControl_ctl01_ctl05_ctl01'
	browser.find_by_css(selector).click()
	time.sleep(30)
			
		
# start Downloads !
downloadReport(downDir)
