'''
Created on 24 paz 2016

@author: PI345811
'''

from dbConnection import DbConnection


class getCoInfo(DbConnection):
    '''
    classdocs
    '''
    __customerQuery='select customer_id from contract_all where co_id={}'
    __tmcodeQuery='select utils.get_tmcode({},sysdate) from dual'
    __sncodeQuery='''SELECT status FROM   pr_serv_status_hist pr WHERE    sncode = {} AND  co_id = {}
     AND  histno=(select max(histno) from pr_serv_status_hist where co_id=pr.co_id and sncode=pr.sncode and trunc(valid_from_date)<=sysdate)
    '''
    __spcodeQuery='''SELECT spcode FROM   pr_serv_spcode_hist pr WHERE co_id = {} and sncode = {} 
    and histno=(Select max(histno) from pr_serv_spcode_hist where co_id=pr.co_id and sncode=pr.sncode)
    '''
    __dnNumberQuery='''select dn.dn_num from directory_number dn, contr_services_cap cp where dn.dn_id=cp.dn_id and cp.co_id={} 
    and dn_status='a' 
    '''
    __portQuery='''select p.port_num from port p , contr_services_cap cp,contr_devices cd where cp.co_id={} and cd.co_id=cp.co_id
and p.port_id=cd.port_id and p.port_status='a' and cp.cs_Deactiv_Date is null
'''
    __activeCoIdQuery='select utils.get_co_status({},sysdate) from dual'
    
    __parameterQuery='''select pv.prm_value_number from parameter_value pv where pv.co_id={} and pv.sncode={} and pv.parameter_id={} 
and pv.prm_seqno=(select max(prm_seqno) from parameter_value where co_id=pv.co_id and sncode=pv.sncode and parameter_id=pv.parameter_id and prm_valid_From is not null)
'''
    def __init__(self,user, pswd, host, db, port,co_id):
        '''
        Constructor
        '''
        self.__co_id=co_id
        DbConnection.__init__(self, user, pswd, host, db, port)
        
        
        '''
        getTmcode
        The method retrieves tmcode for given contract for particular date
        Date should be in format: YYYYMMDD
        '''
    def getTmcode(self): 
        return super().fetchDataForQuery(self.__tmcodeQuery.format(self.__co_id))[0][0]
    def getCustomer(self): 
        return super().fetchDataForQuery(self.__customerQuery.format(self.__co_id))[0][0]
    
    '''
        sncodeIsActive
        The method checks if service for given co_id is active in particular time.
        Date should be in format: YYYYMMDD
        '''
    def coIdIsActive(self):
        try:
            status=super().fetchDataForQuery(self.__activeCoIdQuery.format(self.__co_id))[0][0]
            
            #print(status)
            if status=='a':
                return True
            else:
                return False
        except IndexError :
            return False     
    def sncodeIsActive(self,sncode):
        try:
            sncodeQuery=self.__sncodeQuery.format(sncode,self.__co_id)
            #print(sncodeQuery)
            if super().fetchDataForQuery(sncodeQuery)[0][0]=='A':
                return True
            else:
                return False
        except IndexError :
            return False     
        
    def getDnNumber(self):
        return super().fetchDataForQuery(self.__dnNumberQuery.format(self.__co_id))[0][0]
    def getPort(self):
        return super().fetchDataForQuery(self.__portQuery.format(self.__co_id))[0][0]
    
    def getSpcode(self,sncode):
        return super().fetchDataForQuery(self.__spcodeQuery.format(self.__co_id,sncode))[0][0]
    
    def getParametrValue(self,sncode,paramId):
        try:
            
            return super().fetchDataForQuery(self.__parameterQuery.format(self.__co_id,sncode,paramId))[0][0]
        except IndexError:
            raise
            