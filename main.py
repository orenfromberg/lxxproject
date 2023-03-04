from os import listdir, mkdir
from os.path import isfile, join, exists
import betacode as betacode
import sqlite3
import re

mypath = "files"
count = 0

if not exists(mypath):
	mkdir(mypath)

# Check if we already have the lxx files downloaded
lxx_file_count = len(listdir(mypath))
if lxx_file_count == 65:
		print("LXX files found, skipping download step.\n")
else:
	# If not, run that script...
	if lxx_file_count == 0:
		print("LXX files not found, downloading...\n")
	elif lxx_file_count < 65:
		print("LXX files found, but not all of them are available so to be safe, we're going to start downloading them from scratch.\n")
	elif lxx_file_count > 65:
		print("It doesn't make any sense that you would have extra files in there... I don't know what you're trying to do but you're doing it wrong.\n")
		exit()
	import get_lxx



def parse_lxx():
	dbconn = sqlite3.connect("lxx.db")
	dbconn.execute('''drop table if exists content''')
	dbconn.commit()
	dbconn.execute('''CREATE TABLE `content` (
			`id`			INTEGER PRIMARY KEY AUTOINCREMENT,
			`book_name`		TEXT NOT NULL,
			`chapter_nr`	INTEGER NOT NULL,
			`verse_nr`		INTEGER NOT NULL,
			`word_nr`		INTEGER NOT NULL,
			`word`			TEXT NOT NULL,
			`word_root`		TEXT NOT NULL,
			`morphology`	TEXT NOT NULL
		);''')
	dbconn.close()

	lxxfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) and f[-4:] == "mlxx" ]

	for lxxfile in lxxfiles:
		print (" | Processing " + lxxfile)
		parse_file(lxxfile)

def get_unicode_word(wordInBetacode):
	encoded_word = str.encode(betacode.transliterate(wordInBetacode))
	return encoded_word.decode('utf-8')

commitCounter = 0
def commit_values(db, valuesToInsert):
	sqlcode = "INSERT INTO content VALUES " + ",".join(valuesToInsert)
	db.execute(sqlcode)
	db.commit()
	global commitCounter
	commitCounter += 1
	if commitCounter % 10 == 0:
		print(" | {} rows completed".format(commitCounter * 500))

def parse_file(filename):
	lines = [line.rstrip('\n') for line in open('files/' + filename)]

	book_name = ""
	chapter_nr = ""
	verse_nr = ""
	word_nr = 0
	word = ""
	global count

	dbconn = sqlite3.connect("lxx.db")

	valuesToInsert = []
	chunkCounter = 0
	for line in lines:
		if (re.match(".+ .+:.+", line)):
			# e.g. Ruth 1:1
			a = re.split("[\s|:]", line)
			book_name = a[0]
			chapter_nr = a[1]
			verse_nr = a[2]
			word_nr = 0
		elif (re.match(".+ [1-9]+", line)):
			# e.g. Obad 1 (books with 1 chapter)
			a = re.split("[\s]", line)
			book_name = a[0]
			chapter_nr = 1
			verse_nr = a[1]
			word_nr = 0
		elif (re.match(".+", line)):
			# must be word data
			word_nr = word_nr + 1
			count = count + 1
			word = get_unicode_word(line[0:25].strip())
			root_word = get_unicode_word(re.sub(r'\s+', ' ', line[36:]))
			morphology = re.sub(r'\s+', ' ', line[25:36].strip())
			valuesToInsert.append("(\'" + str(count) + "\', \'" + book_name + "\', \'" + str(chapter_nr) + "\', \'" + str(verse_nr) + "\', \'" +  str(word_nr) + "\', \'" + word + "\', \'" + root_word + "\', \'" + morphology + "\')")
			chunkCounter += 1

		if (chunkCounter == 500):
			commit_values(dbconn, valuesToInsert)
			valuesToInsert = []
			chunkCounter = 0

	if (chunkCounter > 0):
		commit_values(dbconn, valuesToInsert)

	dbconn.close()

print("Beginning lxx file -> sqlite3 conversion:")
parse_lxx()
print(" - 100% Complete")
