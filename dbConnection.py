'''
Created on 21 paz 2016

@author: PI345811
'''
import cx_Oracle


class DbConnection:
    
    def __init__(self,user,pswd,host,db,port):
        '''
        Constructor
        '''
        self.__host=host
        self.__pswd=pswd
        self.__user=user
        self.__db=db
        self.__port=port
        
    
    def openConnToDb(self):
        try:
        #conString=user+'/'+pswd+'@'+host+'/'+db
            self.__conString=self.__user+'/'+self.__pswd+'@'+cx_Oracle.makedsn(self.__host, self.__port, self.__db)
            self.__connection=cx_Oracle.connect(self.__conString)
            return self.__connection
        except cx_Oracle.DatabaseError as e:
            #print(e)
            #exit(1)
            raise
            
    def fetchDataForQuery(self,query):
        try:
            self.__dbCon=self.openConnToDb()
            self.__cur = self.__dbCon.cursor()
            self.__cur.execute(query)
            self.__res = self.__cur.fetchall()
            self.__cur.close()
            self.__dbCon.close()
            
            return self.__res
        except cx_Oracle.DatabaseError as e:
            print(e)
            #self.__dbCon.close()
            #exit(1)
            raise