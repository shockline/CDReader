import cPickle as p

#myList=['a','b','c']
#myList2=['a','b','c','d']
#myFile =file('data.data','a')
#p.dump(myList,myFile)
#p.dump(myList2,myFile)
#myFile.close()

if __name__ =='__main__':
    rFile =file('data.data','r')
    try:
        while True:
            myList=p.load(rFile)
            print myList
    except EOFError:
            print 'end...'