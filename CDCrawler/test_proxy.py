import urllib2
from multiprocessing import Pool
import time
cnt = 0;
def test_proxy(ip,port):
	print ip,port,'miao'
	try:
		time1= time.time();
		url = 'http://www.baidu.com';
		proxy_handler = urllib2.ProxyHandler({"http" : '%s:%s'%(ip,port)});
		opener = urllib2.build_opener(proxy_handler);
		urllib2.install_opener(opener);
		request = urllib2.Request('http://www.baidu.com/');  
		request.add_header('User-Agent', 'fake-client');  
		response = urllib2.urlopen(request,timeout=3);  
		text = response.read(); 
		if len(text)>10:
			time2 = time.time();
			if time2 - time1 < 3:
				fobj = open('proxy_inuse.txt','a');
				fobj.write('%s:%s\n'%(ip,port));
				fobj.close();
				print ip,port;
		else:
			raise 'error';
	except Exception,ex:
		print ex;
		

		

lines = [line.strip().split('@')[0] for line in file('new.txt')];

for l in lines:
	tmp = l.split(':');
	ip = tmp[0];
	port = tmp[1];
	test_proxy(ip,port);




	
