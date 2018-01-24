'''
Created on 21 gru 2016

@author: PI345811
'''
import re
from  sys import exit
class CdrGenerator():
    '''
    classdocs
    '''
    _callDict={'OUTGOING LOCAL CALL':('T10L','1','1','g'),'OUTGOING LOCAL SMS':('T20L','20','1','g'),'OUTGOING LOCAL MMS':('T31L','230','1','C'),
              'DATA UPLOAD':('T50L','112','1','g'),'DATA DOWNLOAD':('T50L','113','1','g'),'DATA UPLOAD/DOWNLOAD':('T50L','111','1','g'),
              'ROAMING OUTGOING  CALL':('T100R','1','1','g'),
              'ROAMING INCOMING  CALL':('T100R','102','2','g'),
              'ROAMING OUTGOING  SMS':('T200R','20','1','g'),
              'ROAMING INCOMING  MMS':('T31R','230','2','C'),
              'ROAMING OUTGOING  MMS':('T31R','230','1','C'),
              'HOTLINE':('T10L','612','1','g'),
              'ROAMING APN TOTAL VOLUME':('T40R','111','1','c'),
              'ROAMING UPLINK ZONAL':('T40R','1047','1','c'),
              'ROAMING DOWNLINK ZONAL':('T40R','1048','1','c'),
              'ROAMING TRANSFERA':('T40R','396','1','c'),
              'DATA TRANSFERA':('T50L','396','1','g'),
              'PBX OWNER PBX-OG rec.':('T10L','350','1','g'),
              'WLAN Roaming':('T40L','781','1','g'),
              'SMS Direct Access USAGE':('T20L','351','1','g'),
              'Supera USAGE':('T20L','352','1','g')
            }
    _roaming554SncodesParams={'1':'148','102':'224','20':'225','230':'226'}
    _roaming553SncodesParams={'111':'149','1047':'149','1048':'149','396':'149'}
   
    #def __init__(self):
        
        
     

    def parseCdrPattern(self,cdrPatternFile,cdrType):
        
        try:
            with open(cdrPatternFile) as f:
                lines = f.readlines()
                for i,line in enumerate(lines):
                    
                    if line.strip()==cdrType:
                        cdrPattern=lines[i+1]
                        break
                        
                    
                    
                    
                return cdrPattern.rstrip()
        except FileNotFoundError:
            print('File with CDR patterns not found.')
            raise
        
        except UnboundLocalError:
            print('CDR pattern not found.')
            raise
    
    
    
    def cdrParameters(self,cdrPattern):
        
        
        params=re.findall('\{(.*?)\}',cdrPattern.strip())
        params = [x for i,x in enumerate(params) if x not in params[i+1:]]
        return params
   

    def generateCDR(self,cdrPattern,params,paramsDict):
        try:
            cdr=cdrPattern
            for i in params:
                j='{'+i+'}'
                cdr=re.sub(j,paramsDict[i], cdr)
            
            return cdr+'\n'
        except KeyError:
            print('Not all CDR parameters available in dictionary:',i)
            exit()
              
            
    def saveToFile(self,path,filename,text):
        file=path+filename
        
        with open(file, 'a') as f:
            f.write(text) 
            
    
        
    