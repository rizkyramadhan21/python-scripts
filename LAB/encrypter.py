#-*- coding: utf-8 -*-
#!/usr/bin/python
#---------------------------------------
# encrypter.py
# (c) Jansen A. Simanullang, 
# 01.03.2016 17:11
# to be used to encrypt string
# and store the encrypted string in a hidden file
# similar to htpasswd
# usage: encrypter "this is a string"
# script name followed by a string
#---------------------------------------
from Crypto.Cipher import AES
import sys


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

	print remainder, quotient
	if remainder:
		message = strInput.ljust(16*(quotient+1))



	encryptedText = obj.encrypt(message)

	return encryptedText

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

key1 = 'ἀλήθεια,καὶἡζωή'
key2 = 'Ἰησοῦς88'

if len(sys.argv) > 0:

	strInput = sys.argv[1]

encryptedText = encrypt(strInput, key1, key2)

print "Encrypted text =\n"+ encryptedText

decryptedText = decrypt(encryptedText, key1, key2)
print "\nDecrypted text =\n", decryptedText

#-------------------------------------

fileCreate(".pass",encryptedText)
strText = readTextFile(".pass")

print strText

decryptedText = decrypt(strText, key1, key2)
print "\nDecrypted from text file =\n", decryptedText.strip()
