#coding=utf-8
 
import urllib
import re

turl = "http://data.eastmoney.com/report/20150807/APPGNmSYLuLbASearchReport.html"
 
def downloadPage(url):
	h = urllib.urlopen(url)
	return h.read()
	
def downloadImg(content):
	pattern = r'src="(.+?\.jpg)" pic_ext'
	m = re.compile(pattern)
	urls = re.findall(m, content)
	
	for i, url in enumerate(urls):
		print("Saving %s.jpg ...... from %s" % (i,url) + '\n')
		urllib.urlretrieve(url, "%s.jpg" % (i, ))
		
content = downloadPage(turl)
f = open('test.txt','a')
for line in content:
    f.write(line)
f.close();
