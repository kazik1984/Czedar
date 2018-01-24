'''
Created on 20 gru 2016

@author: PI345811
'''


from dbConnection import  DbConnection
class Rating(DbConnection):
    '''
    classdocs
    '''
    __svlcodeQuery='select svlcode from mpulktmm where tmcode={} and spcode={} and sncode={}'
    __zncodesQuery='''select /*+ paralell(20) */ mp.des,m.zncode,replace(cgi,'*','*'),trim(zodes),replace(replace(digits,'*','*'),'+'),trim(zpdes),zpcode from
                        MPULKGVM m, mpuzntab mp where mp.zncode=m.zncode and vscode={}
                        and m.gvcode in ({}) order by zncode'''
    
    __ricodeQuery='''select ricode from mpulktmm mm where tmcode ={} and spcode={} and sncode ={} order by vscode desc'''
                       
    
    __gvcodeQuery='''select unique(gvcode) from mpulkrim where ricode in ({})'''
    __vscodeQuery='''select max(vscode) from MPULKGVM where gvcode={}'''
    
    __uniqueZncodesQuery='''select unique zncode from
                        MPULKGVM m where vscode=(select max(vscode) from MPULKGVM where gvcode=m.gvcode)
                        and m.gvcode in (select unique(gvcode) from mpulkrim where ricode in
                        (select ricode from mpulktmm mm where tmcode = {} and spcode={} and sncode = {}
                        and vscode=(select max(vscode) from mpulktmm where tmcode=mm.tmcode and sncode=mm.sncode and spcode=mm.spcode))) order by zncode'''
    
    __zncodeDescQuery='''select des,zncode from mpuzntab where zncode in {}''' 
    
    __zncodeQuery='''select zncode,replace(cgi,'*','*'),zodes,replace(replace(digits,'*','*'),'+'),zpdes from
                        MPULKGVM m where vscode=(select max(vscode) from MPULKGVM where gvcode=m.gvcode)
                        and m.gvcode in (select unique(gvcode) from mpulkrim where ricode in
                        (select ricode from mpulktmm mm where tmcode = {} and spcode={} and sncode = {}
                        and vscode=(select max(vscode) from mpulktmm where tmcode=mm.tmcode and sncode=mm.sncode and spcode=mm.spcode))) and zncode={} order by zncode'''
    
    
    __roamingQueryTzoneOn='''select 
    unique bsi.scenario_spcode
from 
    business_scenario_item bsi, 
    system_scenario_element sse, 
    udc_chain uc, 
    udc_simple_cond usc, 
    udc_reference_value urv
where
    bsi.business_scenario_id = sse.business_scenario_id
and sse.version = 
(select max(version) from system_scenario_version where system_scenario_id = 5)
and sse.system_scenario_id = 5
and bsi.business_scenario_vscode = 
(select max(business_scenario_vscode) from business_scenario_version where business_scenario_id = bsi.business_scenario_id)
and bsi.rateplan_type = 2
and sse.complex_cond_id = uc.complex_cond_id
and uc.version in (1,2)
and uc.chain_id = usc.chain_id
and usc.uds_element_code in (20050, 20051, 20066, 20067, 20068)
and usc.simple_cond_id = urv.simple_cond_id
and usc.operator_id = 1
and uc.short_des like '%TZ'
and bsi.scenario_tmcode={}
and ref_integer={}
'''
    __roamingQueryTzoneOff='''select 
    unique bsi.scenario_spcode
from 
    business_scenario_item bsi, 
    system_scenario_element sse, 
    udc_chain uc, 
    udc_simple_cond usc, 
    udc_reference_value urv
where
    bsi.business_scenario_id = sse.business_scenario_id
and sse.version = 
(select max(version) from system_scenario_version where system_scenario_id = 5)
and sse.system_scenario_id = 5
and bsi.business_scenario_vscode = 
(select max(business_scenario_vscode) from business_scenario_version where business_scenario_id = bsi.business_scenario_id)
and bsi.rateplan_type = 2
and sse.complex_cond_id = uc.complex_cond_id
and uc.version in (1,2)
and uc.chain_id = usc.chain_id
and usc.uds_element_code in (20050, 20051, 20066, 20067, 20068)
and usc.simple_cond_id = urv.simple_cond_id
and usc.operator_id = 1
and uc.short_des not like '%TZ'
and bsi.scenario_tmcode={}
and ref_integer={}
'''

    def __init__(self,user, pswd, host, db, port):
        '''
        Constructor
        '''
        
        DbConnection.__init__(self, user, pswd, host, db, port)
        
    
    def getSpcode(self,tmcode,param_value,tzone_flag):
        if tzone_flag==1:
            spcode=super().fetchDataForQuery(self.__roamingQueryTzoneOn.format(tmcode,param_value))[0][0]
        else:
            spcode=super().fetchDataForQuery(self.__roamingQueryTzoneOff.format(tmcode,param_value))[0][0]
        return spcode
    
    def getZncodes(self,tmcode,spcode,sncode):
        ricode=super().fetchDataForQuery(self.__ricodeQuery.format(tmcode,spcode,sncode))[0][0]
        
        gvcode=super().fetchDataForQuery(self.__gvcodeQuery.format(ricode))[0][0]
        vscode=super().fetchDataForQuery(self.__vscodeQuery.format(gvcode))[0][0]
        zncodes=super().fetchDataForQuery(self.__zncodesQuery.format(vscode,gvcode))
        return zncodes
    
    
         
    def getSvlcode(self,tmcode,spcode,sncode):
        svlcode=super().fetchDataForQuery(self.__svlcodeQuery.format(tmcode,spcode,sncode))[0][0]
        return svlcode
    '''
    def getZncodes(self,tmcode,spcode,sncode):
        zncodes=super().fetchDataForQuery(self.__zncodesQuery.format(tmcode,spcode,sncode))
        return zncodes
        '''
    
    def getZncode(self,tmcode,spcode,sncode,zncode):
        zncode=super().fetchDataForQuery(self.__zncodeQuery.format(tmcode,spcode,sncode,zncode))
        return zncode
    
    def getUniqueZncodes(self,zncodes):
        uniqueZncodes=[]
        for i,j in enumerate(zncodes):
            if zncodes[i][1] not in uniqueZncodes:           
                uniqueZncodes.append(zncodes[i][1])
            
        return uniqueZncodes
    
    def getZncodesDes(self,zncodeList):
        zncodeDesc=super().fetchDataForQuery(self.__zncodeDescQuery.format(str(zncodeList)))
        zncodeDescDict={}
       
        for i in zncodeDesc:
            zncodeDescDict[i[0]]=i[1]
                
        return zncodeDescDict
        