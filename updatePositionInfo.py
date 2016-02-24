# -*- coding: utf-8 -*-
#!/usr/bin/python
#---------------------------------------
# updatePositionInfo.py
# (c) Jansen A. Simanullang, 16:40
# 14.01.2016 13:34 AM
# to be used with telegram-bot plugin
#---------------------------------------
# usage: !updatePositionInfo [location]
#---------------------------------------


from urllib import urlopen
from BeautifulSoup import BeautifulSoup
import os, sys, time

numArgs =  len(sys.argv)

if numArgs == 1:

	print "Anda belum meng-input keterangan"

if numArgs > 1:
	
	if sys.argv[3]:
	# msg.from
		lokasi_userid = sys.argv[1]
		# terminal ID
		lokasi_nama = sys.argv[2]
		# create date
		lokasi_datetime = time.strftime("%Y-%m-%d %H:%M:%S")
		lokasi_credt = lokasi_datetime
		lokasi_creausr = "TELEGRAM"
		# description
		lokasi_keterangan = " ".join(sys.argv[3:numArgs])

		strQuery = "INSERT INTO m_lokasi_karyawan (lokasi_userid, lokasi_nama, lokasi_keterangan, lokasi_datetime, lokasi_credt, lokasi_creausr) VALUES ('"+lokasi_userid+"','"+ lokasi_nama+"','"+lokasi_keterangan+"','"+ lokasi_datetime+"','"+ lokasi_datetime+"','"+ lokasi_creausr+"');"

		#strQuery = "INSERT INTO m_atm_problem_keterangan (atmproblem_tid, atmproblem_keterangan, atmproblem_creadt, atmproblem_creausr) VALUES ('"+atmproblem_tid+"','"+atmproblem_keterangan+"', '"+atmproblem_creadt+"', '"+atmproblem_creausr+"');"
		
		strCmd = 'mysql -h 1.132.218.71 --user sa --password=P@ssw0rd -D kanwiljak3 -e "' + strQuery + '"'

		#print strCmd

		os.system(strCmd)

		print "Terima kasih telah meng-update data lokasi Anda sebagai berikut:\n\nPelapor:\n" + lokasi_nama + "\n\nWaktu laporan:\n" + lokasi_credt + "\n\nLokasi:\n" + lokasi_keterangan

	else:

		print "Anda belum menginput keterangan"



