import sys
import logMod
import MySQLdb

l = logMod.logMod()

class MysqlMod:

    def Create(self):
        self.__db = MySQLdb.connect(host="cp01-bdl-stock-001.epc.baidu.com",user="root",db="Stock_Data",port=5200)
        self.__cursor = self.__db.cursor()

    def Destroy(self):
        self.__cursor.close()
        self.__db.close()   

    def Insert(self, table, line):
        Filed = ['"' + x + '"' for x in line.split("\t")]
        # print len(Filed),Filed
        sql = "INSERT INTO %s(Source,StockCode,StockName,CompanyCode,RateA,RateB,RateC,CompanyName,Author,Url,Title,Text,Date,Time,LabelMood,LabelRelate,Positive,Negative) VALUES (%s);" % (table, ','.join(Filed)) 
        try:
            # l.Notice("This SQL is [%s]" % str(sql))
            self.__cursor.execute(sql)
            self.__db.commit()
        except Exception, ex:
            # Rollback in case there is any error
            l.Fatal("Error: there's a Rollback %s\nSQL:%s" % (str(ex), str(sql)) )
            self.__db.rollback()
