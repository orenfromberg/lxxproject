# this script will download all the books of the lxxmorph
# from http://ccat.sas.upenn.edu/gopher/text/religion/biblical/lxxmorph/
# as specified in TOC. html

from html.parser import HTMLParser
import urllib.request
import re

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if (tag == "a"):
            if (re.match("[0-9][0-9]", attrs[0][1])):
                uri = "http://ccat.sas.upenn.edu/gopher/text/religion/biblical/lxxmorph/" + attrs[0][1]
                filename = "files/" + attrs[0][1]
                urllib.request.urlretrieve(uri, filename)

with open ("TOC.html", "r") as myfile:
	data = myfile.read()
	
parser = MyHTMLParser()
parser.feed(data)
