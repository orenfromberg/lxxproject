# this script will download all the books of the lxxmorph
# from http://ccat.sas.upenn.edu/gopher/text/religion/biblical/lxxmorph/
# as specified in TOC.html
# uses Python 3.4.3

from html.parser import HTMLParser
import urllib.request
import re

lxxuri = "http://ccat.sas.upenn.edu/gopher/text/religion/biblical/lxxmorph/"

urllib.request.urlretrieve(lxxuri, "files/ccat-lxx-index.html")

class MyHTMLParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		if (tag == "a"):
			if (re.match("[0-9][0-9]", attrs[0][1])):
				uri = lxxuri + attrs[0][1]
				filename = "files/" + attrs[0][1]
				print(" | Fetching " + filename)
				urllib.request.urlretrieve(uri, filename)

with open ("files/ccat-lxx-index.html", "r") as myfile:
	data = myfile.read()

print ("Storing files in 'files/'")
parser = MyHTMLParser()
parser.feed(data)
print (" - done")
