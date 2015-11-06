from os import listdir
from os.path import isfile, join
import re

def convert_to_unicode(string):
	return "hi"

mypath = "files"

# get array of files
lxxfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

# get lines in one lxxfile
#lines = [line.rstrip('\n') for line in open('files/01.Gen.1.mlxx')]
lines = [line.rstrip('\n') for line in open('files/14.1Kings.mlxx')]

book_name = ""
chapter_nr = ""
verse_nr = ""
word_nr = 0
word = ""
prefix = ""

for line in lines:
	if (re.match(".+ .+:.+", line)):
		a = re.split("[\s|:]", line)
		book_name = a[0]
		chapter_nr = a[1]
		verse_nr = a[2]
		prefix = book_name + ", " + chapter_nr + ", " + verse_nr + ", "
		word_nr = 0
		#print (book_name + " " + chapter_nr + " " + verse_nr)
	elif (re.match(".+", line)):
		word_nr = word_nr + 1
		#print (str(word_nr) + " = " + line)
		a = re.split("\s+", line)
		word = a[0]
		unicode_word = convert_to_unicode(word)
		print(prefix + str(word_nr) +": \"" + word + "  \"" + unicode_word + "\"")
