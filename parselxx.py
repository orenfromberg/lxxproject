from os import listdir
from os.path import isfile, join
import betacode as betacode
import sqlite3
import re

mypath = "files"
count = 0

def parse_lxx():
	dbconn = sqlite3.connect("lxx.fast.db")
	dbconn.execute('''drop table if exists content''')
	dbconn.commit()
	dbconn.execute('''CREATE TABLE `content` (
			`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
			`book_name`	TEXT NOT NULL,
			`chapter_nr`	TEXT NOT NULL,
			`verse_nr`	TEXT NOT NULL,
			`word_nr`	INTEGER NOT NULL,
			`word`	TEXT NOT NULL,
			`word_root`	TEXT NOT NULL
		);''')
	dbconn.close()

	lxxfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

	for lxxfile in lxxfiles:
		print (lxxfile)
		parse_file(lxxfile)

def get_unicode_word(wordInBetacode):
	encoded_word = str.encode(betacode.transliterate(wordInBetacode))
	return encoded_word.decode('utf-8')

def commit_values(db, valuesToInsert):
	sqlcode = "INSERT INTO content VALUES " + ",".join(valuesToInsert)
	db.execute(sqlcode)
	db.commit()

def parse_file(filename):
	lines = [line.rstrip('\n') for line in open('files/' + filename)]

	book_name = ""
	chapter_nr = ""
	verse_nr = ""
	word_nr = 0
	word = ""
	global count

	dbconn = sqlite3.connect("lxx.fast.db")

	valuesToInsert = []
	chunkCounter = 0
	for line in lines:
		if (re.match(".+ .+:.+", line)):
			a = re.split("[\s|:]", line)
			book_name = a[0]
			chapter_nr = a[1]
			verse_nr = a[2]
			word_nr = 0
		elif (re.match(".+ [1-9]+", line)):
			a = re.split("[\s]", line)
			book_name = a[0]
			chapter_nr = 1
			verse_nr = a[1]
			word_nr = 0
		elif (re.match(".+", line)):
			word_nr = word_nr + 1
			count = count + 1
			a = re.split("\s+", line)
			word = get_unicode_word(a[0])
			root_word = get_unicode_word(a[-1])
			valuesToInsert.append("(\'" + str(count) + "\', \'" + book_name + "\', \'" + str(chapter_nr) + "\', \'" + str(verse_nr) + "\', \'" +  str(word_nr) + "\', \'" + word + "\', \'" + root_word + "\')")
			chunkCounter += 1

		if (chunkCounter == 499):
			commit_values(dbconn, valuesToInsert)
			valuesToInsert = []
			chunkCounter = 0

	if (chunkCounter > 0):
		commit_values(dbconn, valuesToInsert)

	dbconn.close()

parse_lxx();
