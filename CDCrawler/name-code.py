f = open("name-code.txt","r")
for i in xrange(0,2599) :
    t = f.readline()
    t = t[0:len(t)-1]
    print "[%s]," %t
f.close()
    
