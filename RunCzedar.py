'''
Created on 18 pa 2016

@author: PI345811
'''
#import tkinter as tk
#import sshConnection as ssh
#import shellCommands as com
#import re
import dbConnection as db
import getCoInfo 
import sqlQuery as sql
import rating as r
import cdrGenerator
import os
import sys, getopt
import datetime as d
import sshConnection
import shellCommands

def Usage():
    print('The Czedar can be started with the following parameters:')
    print('========================================================')
    print('-c co_id    Contract Id - mandatory parameter')
    print('-d cdr_dir  Path where cdr will be saved. D:/CDR/ - default location')
    print('-h help')
    

if __name__ == '__main__':
    
    
    cdr_path='D:/CDR/' #default location
    coIdNotDefined=True

    try:
        argv=sys.argv[1:]
        
        if len(argv)==0:
            Usage()
            sys.exit()
        else:
            opts,args = getopt.getopt(argv,"hc:d:")
          
               
            
    except getopt.GetoptError:
        print('error')
        Usage()
        sys.exit(2)
          
    for opt, arg in opts:
        
        
        
        if opt == '-h' :
            Usage()
            sys.exit()
        elif opt == '-c':
            coIdNotDefined=False
            co_id=arg
                
        elif opt == '-d':
            cdr_path=arg+'/'  
           
     
   
    if coIdNotDefined:
        print('Contract Id is mandatory parameter.')
        sys.exit(2)
    
    if not os.path.exists(cdr_path):
        os.makedirs(cdr_path)
        
    keyPath='D:\pulpit sluzbowy\pkey.ppk'
    host='aixtestdb1.unx.t-mobile.pl'
    user='t13bscs'
    
   
        
    now = d.datetime.now()
    curDate=now.strftime("%Y%m%d")
    startTime=now.strftime("%Y%m%d%H%M%S")
   
    conInfo=getCoInfo.getCoInfo(sql.user,sql.passw,sql.host,sql.sid,sql.port,co_id)
    
    if not conInfo.coIdIsActive(curDate):
        print('CO_ID does not exists or is not active.')
        sys.exit()
    #print('RunCzedar run for co_id:',co_id)
    #print('Argument List:', sys.argv[1:])
    
    
    
    
    callDict={'OUTGOING LOCAL CALL':('T10','1','1','g'),'OUTGOING LOCAL SMS':('T20','20','1','g'),'OUTGOING LOCAL MMS':('T31','230','1','C'),
              'DATA UPLOAD':('T50','112','1','g'),'DATA DOWNLOAD':('T50','113','1','g'),'DATA UPLOAD/DOWNLOAD':('T50','111','1','g')}
    
    item=1
    tempDict={}
    for i in sorted(cdrGenerator.CdrGenerator._callDict):
        tempDict[str(item)]=i
        print(str(item)+'. '+i)
        item+=1
    
    
    
   # path='D:\pulpit sluzbowy\pkey.ppk'
    #host='aixtestdb1.unx.t-mobile.pl'
   
    chosenCall=input('Put your choice 1-{}:'.format(item-1))
    
    while chosenCall not in tempDict:   
        
        print('Incorrect Choice.Try Again or put N to close...')
        chosenCall=input('Put your choice 1-{}:'.format(item-1))
        if chosenCall=='N' or chosenCall not in tempDict:
            sys.exit()
            
        
        
    chosenCall=tempDict[chosenCall]
    print('You chose '+ chosenCall)
    
        
        
    cdrType=callDict[chosenCall][0]
    sncode=callDict[chosenCall][1]
    if not conInfo.sncodeIsActive(sncode, curDate):
        print('Cannot generate {} because sncode={} is not in active state'.format(chosenCall,sncode))
        sys.exit()
    callType=callDict[chosenCall][2]
    filePrefix=callDict[chosenCall][3]
    
    #stdout, stderr=ssh.runCommandOnShell(host, 't13bscs',path, com.readASCIIconvGsm)
    duration=60
    
    imei='355671073043250'
    conInfo=getCoInfo.getCoInfo(sql.user,sql.passw,sql.host,sql.sid,sql.port,co_id)
    tmcode=conInfo.getTmcode(curDate)
    callTech=str(0)
    spcode=conInfo.getSpcode(sncode)
    directoryNum=conInfo.getDnNumber()
    port=conInfo.getPort()
    rat=r.Rating(sql.user,sql.passw,sql.host,sql.sid,sql.port)
    svlcode=rat.getSvlcode(tmcode, spcode, sncode)
    zncode=rat.getZncodes(tmcode, spcode, sncode)
    cdrObj=cdrGenerator.CdrGenerator()
    fileName=str(filePrefix)+str(startTime)+'_co_id_'+str(co_id)+'.cdr'
    print(cdr_path+fileName)
    pattern=cdrObj.parseCdrPattern('cdr_pattern.txt', cdrType)
    params=cdrObj.cdrParameters(pattern)
    
    for i in zncode:
        digits=str(i[3])
        cgi=str(i[1])
    
    
        paramDict={'DIGITS':digits,'CALL_TYPE':callType,'DIRECTORY_NUMBER':directoryNum,'PORT':port,'START_TIME':startTime,'SVLCODE':svlcode,'CGI':cgi,'REMARK':digits,
               'CALL_TECH':callTech,'DURATION':str(duration),'IMEI':imei,'DATAVOLUME':'102400'}
  
        
        cdr=cdrObj.generateCDR(pattern, params, paramDict)
        cdrObj.saveCDRToFile(cdr_path,fileName, cdr)
    
    # Transfer created CDR file to Remote Location ($BSCS_WORK/MP/SWITCH/DIH)
    
    s=sshConnection.SshConnection(host, user, keyPath)
    bscsWork=s.runCommandOnShell(shellCommands.preCommand+'echo $BSCS_WORK')[0][1]
    cdrLocation=bscsWork.rstrip()+'/MP/SWITCH/DIH/'    
    #s.sendCDRToBSCS(cdr_path, cdrLocation,fileName)
        #print(cdr)
    
   
    