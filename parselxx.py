from os import listdir
from os.path import isfile, join
import betacode as betacode
import sqlite3

import re

def convert_to_unicode(string):
	return "hi"

mypath = "files"
	
# get array of files
lxxfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

# get lines in one lxxfile
lines = [line.rstrip('\n') for line in open('files/01.Gen.1.mlxx')]
#lines = [line.rstrip('\n') for line in open('files/14.1Kings.mlxx')]

book_name = ""
chapter_nr = ""
verse_nr = ""
word_nr = 0
count = 0
word = ""

# outfile = open('outfile.txt', 'wb')

dbconn = sqlite3.connect("database")

for line in lines:
	if (re.match(".+ .+:.+", line)):
		a = re.split("[\s|:]", line)
		book_name = a[0]
		chapter_nr = a[1]
		verse_nr = a[2]
		word_nr = 0
	elif (re.match(".+", line)):
		word_nr = word_nr + 1
		count = count + 1
		a = re.split("\s+", line)
		word = a[0] # word is first in array
		encoded_word = str.encode(betacode.transliterate(word))
		unicode_word = encoded_word.decode('utf-8')
		sqlcode = "INSERT INTO content VALUES (\'" + str(count) + "\', \'" + book_name + "\', \'" + str(chapter_nr) + "\', \'" + str(verse_nr) + "\', \'" +  str(word_nr) + "\', \'" + unicode_word + "\')"
		#outfile.write(unicode_word.encode('utf-8'))
		dbconn.execute(sqlcode)
		dbconn.commit()

dbconn.close()
# outfile.close()