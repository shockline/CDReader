import sys
import sql.Mysql as Mysql


Mysqldb = Mysql.Mysql()

def GetLine():
    Mysqldb.Create()
    for line in sys.stdin:
        line = line.rstrip()
        if line == "" :
            continue
        Mysqldb.Insert("Stock_Test", line)
    Mysqldb.Destroy()

GetLine()
