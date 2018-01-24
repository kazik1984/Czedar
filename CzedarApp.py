'''
Created on 28 gru 2016

@author: PI345811
'''

import tkinter as tk

import tkinter.ttk
import cx_Oracle

import queue

#import sys
import datetime as d
from os.path import isfile

from tkinter.filedialog import askdirectory,askopenfilename
from tkinter.messagebox import showerror,showinfo
import os
import time 
#from tkinter.constants import BOTTOM, LEFT, RIGHT
from cdrGenerator import CdrGenerator
import rating as r
import sshConnection
import shellCommands
import getCoInfo
import paramiko


class CzedarApp(tk.Tk):
    '''
    classdocs
   
    '''

    def enterCoId(self,event):
        
        #print(self.generateCDRButton.winfo_exists())
        
        self.generateCDRButton.grid_remove()
        #self.getRatConf.grid()
        self.zncodeDesList=['ALL']
        self.chosenDirectionList=['ALL']
        self.chk_button_overwrite.deselect()
        self.chk_button_overwrite.config(state="disabled")
        
        #self.comboChosenCall['values']=self.chosenCallList[1:]
        self.comboChosenCall.current(0)
        self.chosenCall=''
        try:
       
            self.comboDirection['values']=self.chosenDirectionList
            self.comboDirection.current(0)
       
            self.comboZncodes['values']=self.zncodeDesList
            self.comboZncodes.current(0)
        #self.comboDirection.current(0)
        #self.comboChosenCall
        #self.comboZncodes.current(0)
        except AttributeError:
            pass
                
    def setBscsFlag(self):
            self.flagBSCS=self.var.get()   
            #print(self.flagBSCS)
    
    def refreshConfig(self,event):
        try:
            
            self.comboChosenCall.current(0)
            
            for i,j in enumerate(self.envList):
                if self.envList[i][0]==self.chosenEnv.get():
                    database=j[1]
                    self.user=database.split('/')[0]
                    self.pswd=database.split('/')[1].split('@')[0]
                    self.db=database.split('/')[1].split('@')[1]
                    self.host=j[2]
                    self.portdb=j[3]
                    self.AixUser=j[4]
                    self.AixHost=j[5]
            
            if self.comboZncodes is not None:
                self.comboZncodes['values']=['']
                self.comboZncodes.current(0)
                self.comboDirection['values']=['']
                self.comboDirection.current(0)
                self.generateCDRButton.grid_remove()
                self.chosenCall=''
        except AttributeError:
            print('e')
            pass
        
        
    def readNewConfig(self):
        try:
            #print('lista')
            separator='|'
            with open('config.txt') as f:
                lines = f.readlines()
                
                self.envList=[]
                env=[]
                for line in lines:
                    
                    if len(line.split(separator))>1:
                        conf=line.split(separator)[0].strip()
                        var=line.split(separator)[1].strip()
                        
                        if conf=='Env':
                        
                            env.append(var)
                    
                        if conf=='Database':
                            
                            env.append(var) 
                        elif conf=='DB Host':
                            
                            env.append(var)
                        elif conf=='DB Port':
                            
                            env.append(var)
                        elif conf=='AIX User':
                            
                            env.append(var)
                        elif conf=='Path to PK':
                            if os.path.isfile(var):
                                self.entryPkPath.insert(0, var)
                        elif conf=='CDR Path':
                            if os.path.isdir(var):
                                self.entryCdrPath.insert(0, var)
                                
                            
                                
                        elif conf=='AIX Host':
                            
                            env.append(var)
                    else:
                        self.envList.append(env)
                        env=[]
                   
                    
                    
                time.sleep(1)    
                if self.entryPkPath.get()=='':
                        showinfo("Incorrect Path.","Private key not found. Browse the file manually.")   
                envList=[]
                for i,j in enumerate(self.envList):
                    #print(self.envList[i][0])
                    envList.append(self.envList[i][0])
                self.envCombo['values']=envList  
                self.envCombo.current(0)
                
                
                database=self.envList[0][1]
                self.user=database.split('/')[0]
                self.pswd=database.split('/')[1].split('@')[0]
                self.db=database.split('/')[1].split('@')[1]
                self.host=self.envList[0][2]
                self.portdb=self.envList[0][3]
                self.AixUser=self.envList[0][4]
                self.AixHost=self.envList[0][5]
                
                
        except FileNotFoundError:
            showinfo("Config file not found.","Please put configuration manually.")
        
            
    
    def readConfig(self):
        try:
            separator='|'
            with open('config.txt') as f:
                lines = f.readlines()
                
                for line in lines:
                    if len(line.split(separator))>1:
                        conf=line.split(separator)[0].strip()
                        var=line.split(separator)[1].strip()
                    
                    if conf=='Database':
                        
                        self.entryDatabase.insert(0, var) 
                    elif conf=='DB Host':
                        
                        self.entryDatabaseHost.insert(0, var)
                    elif conf=='DB Port':
                        
                        self.entryDatabasePort.insert(0, var)
                    elif conf=='AIX User':
                        
                        self.entryAixUser.insert(0, var)
                    elif conf=='Path to PK':
                        if os.path.isfile(var):
                            self.entryPkPath.insert(0, var)
                    elif conf=='CDR Path':
                        if os.path.isdir(var):
                            self.entryCdrPath.insert(0, var)
                            
                        
                            
                    elif conf=='AIX Host':
                        
                        self.entryAixHost.insert(0, var)
                time.sleep(1)    
                if self.entryPkPath.get()=='':
                        showinfo("Incorrect Path.","Private key not found. Browse the file manually.")     
        except FileNotFoundError:
            showinfo("Config file not found.","Please put configuration manually.")
        
    def browseDirectoryButton(self,entry): 
        directory=askdirectory(title='Please select a CDR path.')
        if directory: 
            try: 
                entry.delete(0,len(entry.get()))
                entry.insert(0, directory)
            except: 
                showerror("Open Source Directory", "Failed to open directory \n'%s'"%directory)  
                
    def browseFileButton(self,entry): 
        file=askopenfilename(title='Please select a CDR path.')
        if file: 
            try: 
                entry.delete(0,len(entry.get()))
                entry.insert(0, file)
            except: 
                showerror("Open Source File", "Failed to open file \n'%s'"%file)
                
    def patch_crypto_be_discovery(self):

        """
        Monkey patches cryptography's backend detection.
        Objective: support pyinstaller freezing.
        """
    
        from cryptography.hazmat import backends
    
        try:
            from cryptography.hazmat.backends.commoncrypto.backend import backend as be_cc
        except ImportError:
            be_cc = None
    
        try:
            from cryptography.hazmat.backends.openssl.backend import backend as be_ossl
        except ImportError:
            be_ossl = None
    
        backends._available_backends_list = [
            be for be in (be_cc, be_ossl) if be is not None
        ] 
    
    def busy(self,event):
        self.config(cursor="wait")

    def notbusy(self,event):
        self.config(cursor="")
    
    def filtrComboBox(self,event):
        try:
            
            print(self.comboDirection.get())
            chosenDirectionListTmp=[]
            for i in self.chosenDirectionList:
                if  (self.comboDirection.get().lower()) in i.lower():
                    
                    chosenDirectionListTmp.append(i)
                
            #print(chosenDirectionListTmp)
            self.comboDirection['values']=chosenDirectionListTmp
            
            #self.comboDirection.event_generate('<Down>')
            #self.comboDirection.position()
            
            #print(len(chosenDirectionListTmp))
            if len(chosenDirectionListTmp)==1 and  event.keysym != "BackSpace":#and len(var.get())>0
                #lenString=len(var.get())
                #self.comboDirection.delete(0,tkinter.END)
                #
                #self.comboDirection.selection_range(lenString,tkinter.END)        
                self.comboDirection.current(0)
                self.comboDirection.icursor(tkinter.END)
                #self.comboDirection.selection_range(lenString,tkinter.END)
                
               
            '''
            for i in self.chosenDirectionList:
                for i in self.zncode:
                    if i[0]==self.var2.get():
                        self.chosenDirectionList.append(str(i[5])+'-'+str(i[4]))
                #self.zncode=self.zncodeDesDict[self.var2.get()]
                #print(self.zncode)
                #self.chosenDirection=['1','2','3']
                self.comboDirection['values']=self.chosenDirectionList
                self.comboDirection.current(0)
            else:
                self.chosenDirectionList=['ALL']
                
                self.comboDirection['values']=self.chosenDirectionList.sort
                self.comboDirection.current(0)
           ''' 
        except AttributeError as e:
            print(e)  
        
         
    def getCoRatingConfiguration(self,event):
        
        
        try:
            print(self.chosenCall)
            print(self.var1.get())
            self.now = d.datetime.now()
            self.curDate=self.now.strftime("%Y%m%d")
            #print(self.curDate)
            #print(self.user)
            #print(self.db)
            self.startTime=self.now.strftime("%Y%m%d%H%M%S")
            self.co_id=self.entryContractId.get()
            
            
            if self.chosenCall!=self.var1.get():
                self.chosenCall=self.var1.get()
                #self.comboChosenCall['values']=self.chosenCallList
                #self.comboChosenCall.current(0)
                
                    
                
            
            
                if self.co_id!='':
                 
                    self.coInfo=getCoInfo.getCoInfo(self.user, self.pswd, self.host, self.db, self.portdb,self.co_id)
                    rat=r.Rating(self.user, self.pswd, self.host, self.db, self.portdb)
                    
                    self.cdrType=CdrGenerator._callDict[self.chosenCall][0]
                    self.sncode=CdrGenerator._callDict[self.chosenCall][1]
         
                    
                    #print(self.coInfo.sncodeIsActive(self.sncode, self.curDate))
                    if self.coInfo.coIdIsActive() :
                        self.customerId=self.coInfo.getCustomer()
                        if self.cdrType[-1]=='R': 
                            
                            try:
                                
                                if  self.coInfo.sncodeIsActive(911) and self.sncode in CdrGenerator._roaming554SncodesParams.keys():
                                    
                                    self.rateplan='554'
                                    
                                    self.parameterValue=str(int(self.coInfo.getParametrValue('911', CdrGenerator._roaming554SncodesParams[self.sncode])))
                                    self.Tzone=str(int(self.coInfo.getParametrValue('911',227)))
                                    print(self.Tzone)
                                    self.spcode=rat.getSpcode(self.rateplan,self.parameterValue,self.Tzone)
                                    
                                elif self.coInfo.sncodeIsActive(911) and self.sncode in CdrGenerator._roaming553SncodesParams.keys():
                                    self.rateplan='553'
                                    
                                    self.parameterValue=str(int(self.coInfo.getParametrValue('911', CdrGenerator._roaming553SncodesParams[self.sncode])))
                                    self.Tzone=str(int(self.coInfo.getParametrValue('911',227)))
                                    print(self.Tzone)
                                    self.spcode=rat.getSpcode(self.rateplan,self.parameterValue,self.Tzone)
                                   
                                    print(self.spcode)
                                    
                                else:
                                    raise
                            except KeyError as e:
                            
                                self.generateCDRButton.grid_remove()
                                showinfo("Error","Cannot find spcode for given parameter.")
                            
                            
                                
                                
                        
                        
                        else:
                               
                            self.rateplan=self.coInfo.getTmcode()
                       
                        self.callType=CdrGenerator._callDict[self.chosenCall][2]
                        self.filePrefix=CdrGenerator._callDict[self.chosenCall][3]
                           
                                
                                 
                        #print(self.coInfo.sncodeIsActive(self.sncode))        
                        if   self.coInfo.sncodeIsActive(self.sncode) or self.sncode=='102':
                            
                            if self.cdrType[-1]!='R':
                                self.spcode=self.coInfo.getSpcode(self.sncode)
                                
                        
                            self.svlcode=rat.getSvlcode(self.rateplan, self.spcode, self.sncode)
                            self.zncode=rat.getZncodes(self.rateplan, self.spcode, self.sncode)
                            
                            self.uniqueZncodes=rat.getUniqueZncodes(self.zncode)
                            
                            self.zncodeDesDict=rat.getZncodesDes(tuple(self.uniqueZncodes))
                            #print(self.zncode)
                            
                            
                            
                            '''
                            drop down menu with zncodes
                                '''
                            self.labelZncodes=tk.Label(self.frameCdrGenerator,text="Choose zncode: ").grid(row=2,column=0,sticky='W')
                            self.var2 = tk.StringVar()
                            self.zncodeDesList=['ALL']
                            self.zncode.sort(key=lambda x: x[1])
                            for i in self.zncode:
                                    if (str(i[1])+'-'+str(i[0])) not in self.zncodeDesList:
                                        self.zncodeDesList.append(str(i[1])+'-'+str(i[0]))
                            
                            self.comboZncodes =tkinter.ttk.Combobox(self.frameCdrGenerator, textvariable=self.var2,width=57,values=self.zncodeDesList, state='readonly')
                            self.comboZncodes.current(0)
                            self.comboZncodes.grid(row=2,column=1,sticky='W')
                            self.comboZncodes.bind("<<ComboboxSelected>>", self.getDirection)
                            
                            '''
                            drop down menu with direction
                           '''
                            self.labelDirection=tk.Label(self.frameCdrGenerator,text="Choose direction: ").grid(row=3,column=0,sticky='W')
                            self.var3 = tk.StringVar()
                            self.chosenDirectionList=['ALL']
                            
                            
                            
                             
                            
                            self.comboDirection =tkinter.ttk.Combobox(self.frameCdrGenerator, textvariable=self.var3,width=57,value=self.chosenDirectionList)
                            
                            self.comboDirection.current(0)
                            #self.comboDirection.select_range(0,tk.END)
                            self.comboDirection.grid(row=3,column=1,sticky='W')
                            #self.var3.trace("w",lambda name, index, mode, sv=self.var3: self.filtrComboBox(self.var3))
                            self.comboDirection.bind('<KeyRelease>',self.filtrComboBox)
                             
                           
                            
                            '''
                            quantity
                            '''
                            self.labelQuantity=tk.Label(self.frameCdrGenerator,text="Quantity of CDRs:").grid(row=5,column=0,sticky='W')
                            self.entryQuantity=tk.Entry(self.frameCdrGenerator,width=60)
                            
                            self.entryQuantity.grid(row=5,column=1,sticky='W')
                            
                            self.entryQuantity.delete(0,len(self.entryQuantity.get()))
                            self.entryQuantity.configure(state='disabled')
      
                            if 'T10' in self.cdrType:
                                self.labelDuration.grid()
                                self.entryDuration.grid()
                                self.entryDuration.config(state='normal')
                                self.labelDuration.config(text="Duration [sec]:")
                                self.entryDuration.delete(0,len(self.entryDuration.get()))
                                self.entryDuration.insert(0,"60")
                            elif 'T20' in self.cdrType or 'T31' in self.cdrType or 'T40L' in self.cdrType:
                                self.labelDuration.grid()
                                self.entryDuration.grid()
                                self.entryDuration.delete(0,len(self.entryDuration.get()))
                                self.labelDuration.config(text="Messages number [Items]:")
                                self.entryDuration.insert(0,"1")
                                self.entryDuration.config(state='disabled')
                                
                            elif 'T50' in self.cdrType or 'T40R' in self.cdrType:
                                self.labelDuration.grid()
                                self.entryDuration.grid()
                                self.entryDuration.config(state='normal')
                                self.labelDuration.config(text="Data Volume [Bytes]:")
                                self.entryDuration.delete(0,len(self.entryDuration.get()))
                                self.entryDuration.insert(0,"1048576")
                                
                            
                            
                            
                            
                            '''
                            destroy rating configuration button
                            '''
                            #self.getRatConf.grid_remove()
                            self.generateCDRButton.grid()
                            self.generateCDR
                            
                            
                            
                            
                        else:
                            if self.comboZncodes is not None:
                                self.comboDirection['values']=['']
                                self.comboZncodes['values']=['']
                                self.comboZncodes.current(0)
                                self.comboDirection.current(0)
                                self.chk_button_overwrite.deselect()
                                self.chk_button_overwrite.config(state="disabled")
                                
                            
                            self.message='Service '+self.sncode+' is not in active state. Cannot generate CDR.'
                            showinfo("Service is not in active state. ", self.message)
                            self.generateCDRButton.grid_remove()
                            self.comboChosenCall.current(0)
                            
                
                    else:
                        showerror("Incorrect Contract ID", "Contract does not exists or is not in active state.")
                    
                else:
                    showinfo("Missing Contract ID", "Contract Id is mandatory.")
                    self.chosenCall=''
           
                    
        except ValueError as e :
                showinfo('ERROR',e)
        except KeyError as e:
                        print(str(e))
                        self.generateCDRButton.grid_remove()
                        showinfo("Error","Please select call type.")
        except cx_Oracle.DatabaseError as e:
                        self.generateCDRButton.grid_remove()
                        self.comboChosenCall.current(0)
                        showinfo("Database Error",e)
        except TypeError as e:
                        self.generateCDRButton.grid_remove()
                        showerror("Error","Cannot find spcode for given parameter.")
        
        except AssertionError: 
            self.message='Roaming for the contract is not activated. Cannot generate CDR.'
            showinfo("Check service  911 or service "+self.sncode+" if are in active state. ", self.message)           
        except IndexError as e:
            self.message='Roaming for the contract is not activated. Cannot generate CDR.'
            showinfo("Check  parameters for service  911.", self.message)
        
        
        
       
    def getDirection(self,event):
        
        try:
            if self.var2.get()!='ALL':
                self.chk_button_overwrite.config(state="normal")
                self.entryQuantity.configure(state='normal')
                self.entryQuantity.delete(0, len(self.entryQuantity.get()))
                self.entryQuantity.insert(0, "1")
                self.chosenDirectionList=[]
                self.zncode.sort(key=lambda x: x[6])
                for i in self.zncode:
                   
                    if str(i[1])==self.var2.get().split('-')[0]:
                        
                        self.chosenDirectionList.append(str(i[6])+'-'+str(i[5])+'-'+str(i[4]))
                #self.zncode=self.zncodeDesDict[self.var2.get()]
                #print(self.zncode)
                #self.chosenDirection=['1','2','3']
                self.chosenDirectionList.sort()
                self.comboDirection['values']=self.chosenDirectionList
                self.comboDirection.set('')
                #self.comboDirection.select_range(0,tkinter.END)
            else:
                self.chk_button_overwrite.deselect()
                self.chk_button_overwrite.config(state="disabled")
                
                self.chosenDirectionList=['ALL']
                self.entryQuantity.delete(0,len(self.entryQuantity.get()))
                self.entryQuantity.configure(state='disabled')
                self.comboDirection['values']=self.chosenDirectionList
                self.comboDirection.current(0)
            
        except AttributeError as e:
            print(e)  
    
    
    


    '''
    def progressBar(self,progress,progressmax):
        top=tk.Toplevel()
        top.title("CDRs are generated. Please Wait.")
                
        self.progressbar=tkinter.ttk.Progressbar(top,orient="horizontal", length=200, mode='determinate',maximum=progressmax)
        self.progressbar["value"]=progress 
              
                
        print("progress")
     '''           
       
    def generateCDR(self,event):
       
        self.now = d.datetime.now()
        self.curDate=self.now.strftime("%Y%m%d")
        self.startTime=self.now.strftime("%Y%m%d%H%M%S")
        self.cnt=0
        self.offset='3600'
        '''
        database=self.entryDatabase.get()
        user=database.split('/')[0]
        pswd=database.split('/')[1].split('@')[0]
        db=database.split('/')[1].split('@')[1]
        host=self.entryDatabaseHost.get()
        port=self.entryDatabasePort.get()
        co_id=self.entryContractId.get()
        
        self.chosenCall=self.var1.get()
        '''
        self.duration=self.entryDuration.get()
        self.imei='355671073043250'
        self.callTech=str(0)
        self.quantity=self.entryQuantity.get()
        self.chosenZncode=self.comboZncodes.get()
        self.chosenDirection=self.comboDirection.get()
    
        
        while True:
            try:
                '''
                if co_id=='':
                
                    showinfo("Missing Contract ID", "Contract Id is mandatory.")
                
                    break
           
                
                coInfo=getCoInfo.getCoInfo(user, pswd, host, db, port,co_id)
                
                if not coInfo.coIdIsActive(self.curDate):
                    showerror("Incorrect Contract ID", "Contract does not exists or is not in active state.")
                    break
                
                '''
                if self.comboDirection.get() not in self.chosenDirectionList:
                    showinfo("Error", "Incorrect Direction. Please choose only available on the direction list.")
                    self.comboDirection.selection_range(0, 5)
                    break
                self.dnNumber=self.coInfo.getDnNumber()
                    #self.entryDirectoryNumber.insert(0, dnNumber)
                self.port=self.coInfo.getPort()
                    #self.entryPort.insert(0, port)
                self.rateplan=self.coInfo.getTmcode()
                    #self.entryRateplan.insert(0,rateplan)
                '''
                self.cdrType=CdrGenerator._callDict[self.chosenCall][0]
                self.sncode=CdrGenerator._callDict[self.chosenCall][1]
                if not coInfo.sncodeIsActive(self.sncode, self.curDate):
                    self.message='Service '+self.sncode+' is not in active state. Cannot generate CDR.'
                    showinfo("Service is not in active state. ", self.message)
                    break 
                
                self.spcode=coInfo.getSpcode(self.sncode)
                
                self.callType=CdrGenerator._callDict[self.chosenCall][2]
                self.filePrefix=CdrGenerator._callDict[self.chosenCall][3]
                '''
                if not  self.duration.isdigit() and self.duration!='':
                    showinfo("Error. ", "Duration/Data Volume must be digits")
                    break
                #print(isdigit(self.quantity))
                if (not  self.quantity.isdigit()) and self.quantity!='':
                    showinfo("Error. ", "Quantity must be digits")
                    break
                
                '''    
                rat=r.Rating(user, pswd, host, db, port)
                self.svlcode=rat.getSvlcode(self.rateplan, self.spcode, self.sncode)
                self.uniqueZncodes=rat.getUniqueZncodes(self.rateplan, self.spcode, self.sncode)
                self.zncode=rat.getZncodes(self.rateplan, self.spcode, self.sncode)
                #print(self.uniqueZncodes)
                
                '''
                cdrObj=CdrGenerator()
                
                pattern=cdrObj.parseCdrPattern('cdr_pattern.txt', self.cdrType)
                params=cdrObj.cdrParameters(pattern)
                self.cdrPath=self.entryCdrPath.get()+'/'
                cdr=''
                if self.ovw.get()==1:
                    fileName=str(self.filePrefix)+'_co_id_'+str(self.co_id)+'_set.cdr' 
                else:
                            
                    fileName=str(self.filePrefix)+str(self.startTime)+'_co_id_'+str(self.co_id)+'.cdr' 
                fileNameList=[] 
             
            # read more bytes after 100 ms
                
                if self.chosenZncode=='ALL':
                    
                    if self.ovw.get()==1:
                        fileName=str(self.filePrefix)+'_co_id_'+str(self.co_id)+'_set.cdr' 
                    else:
                            
                        fileName=str(self.filePrefix)+str(self.startTime)+'_co_id_'+str(self.co_id)+'.cdr'
                    
                    
                    logName=str(self.co_id)+'_'+str(self.rateplan)+'_'+str(self.spcode)+'_'+str(self.sncode)+'.log'
                    query='''select * from udr_lt where cust_info_customer_id={} and cust_info_contract_id={} 
                and tariff_info_sncode={} and start_Time_timestamp=to_date('{}','yymmddhh24miss')-{}/3600/24;'''.format(self.customerId,self.co_id,self.sncode,self.startTime,self.offset)
                    for i in self.zncode:
                        self.digits=str(i[4])
                        self.cgi=str(i[2])
    
                        paramDict={'DIGITS':self.digits,'CALL_TYPE':self.callType,'DIRECTORY_NUMBER':self.dnNumber,'PORT':self.port,'START_TIME':self.startTime,'SVLCODE':self.svlcode,'CGI':self.cgi,'REMARK':(str(i[5].replace(',',''))+'-'+str(i[1])+'-'+str(i[6])),
                                    'CALL_TECH':self.callTech,'DURATION':str(self.duration),'IMEI':self.imei,'DATAVOLUME':str(self.duration),'OFFSET':self.offset}
                        
                        
                        cdr+=cdrObj.generateCDR(pattern, params, paramDict)
                        self.cnt+=1
                        
                        
                    cdrObj.saveToFile(self.cdrPath,fileName, cdr)
                    fileNameList.append(fileName)
                    
                else:
                    
                   
                    for i in self.zncode:
                        
                        if self.chosenZncode==(str(i[1])+'-'+str(i[0])) and self.chosenDirection==(str(i[6])+'-'+str(i[5])+'-'+str(i[4])):
                            logName=str(self.co_id)+'_'+str(self.rateplan)+'_'+str(self.spcode)+'_'+str(self.sncode)+'_'+str(i[1])+'_'+str(i[6])+'.log'
                            query='''select * from udr_lt where cust_info_customer_id={} and cust_info_contract_id={} 
                and tariff_info_sncode={} and tariff_info_zncode={} and tariff_info_zpcode={} and start_Time_timestamp=to_date('{}','yymmddhh24miss')-{}/3600/24;'''.format(self.customerId,self.co_id,self.sncode,i[1],i[6],self.startTime,self.offset) 
                            self.digits=str(i[4])
                            self.cgi=str(i[2])
                            
                            paramDict={'DIGITS':self.digits,'CALL_TYPE':self.callType,'DIRECTORY_NUMBER':self.dnNumber,'PORT':self.port,'START_TIME':self.startTime,'SVLCODE':self.svlcode,'CGI':self.cgi,'REMARK':(str(i[5]).replace(',','')+'-'+str(i[1])+'-'+str(i[6])),
                                    'CALL_TECH':self.callTech,'DURATION':str(self.duration),'IMEI':self.imei,'DATAVOLUME':str(self.duration),'OFFSET':self.offset}
                            
                            fileNum=1
                            if self.ovw.get()==1:
                                fileName=str(self.filePrefix)+'_co_id_'+str(self.co_id)+'_set.cdr' 
                            else:
                            
                                fileName=str(self.filePrefix)+str(self.startTime)+'_co_id_'+str(self.co_id)+'_'+str(i[1])+'_'+str(i[6])+'.cdr'
                      
                            
                            
           
                             
                            for i in range(int(self.quantity)):
                                self.max=self.quantity
                                
                                #self.progressBar(cnt, self.max)
                                
                                cdr+=cdrObj.generateCDR(pattern, params, paramDict)
                                
                                self.cnt+=1
                                
                                #print(cnt)
                                #print(int(self.quantity))
                                left=int(self.quantity)-self.cnt
                                if (self.cnt%10000==0 or left==0) and int(self.quantity)>10000:
                                    filenameTmp=fileName.split('.')[0]+'_'+str(fileNum)+'.cdr'
                                    fileNameList.append(filenameTmp)
                                    cdrObj.saveToFile(self.cdrPath,filenameTmp, cdr)
                                    
                                    cdr=''
                                    
                              
                                    fileNum+=1
                                    
                                   
                                    
                                elif int(self.quantity)<=10000 and self.cnt==int(self.quantity):
                                    print('tutaj')
                                    cdrObj.saveToFile(self.cdrPath,fileName, cdr)
                                    fileNameList.append(fileName)
                #print(cdr)        
                               
                             
                   
                    
                # log dla CDR-a katalog LOG w sciezce dla CDR-ow
                logPath=self.cdrPath+'/LOG/'
                if not os.path.isdir(logPath):
                    os.makedirs(logPath)
                #print(logPath)
                #print(str(cnt))
                noCDR='No of sent CDRs: '+str(self.cnt)+' start date: '+self.startTime+'\n'
                cdrObj.saveToFile(logPath,logName,noCDR)
                cdrObj.saveToFile(logPath,logName,query+'\n')
                   
                self.bscsFlag=self.var.get()  
                try:
                    if self.bscsFlag==1:
                    
                            if not isfile(self.entryPkPath.get()):
                                showinfo("INFO", "Cannot find private key.CDR not sent to BSCS.")
                                break
                            
                            self.patch_crypto_be_discovery()
                        
                            s=sshConnection.SshConnection(self.AixHost, self.AixUser, self.entryPkPath.get())
                            bscsWork=s.runCommandOnShell(shellCommands.preCommand+'echo $BSCS_WORK')[0][1]
                            cdrLocation=bscsWork.rstrip()+'/MP/SWITCH/DIH/'
                            for i in fileNameList:
                                print(i)    
                                s.sendCDRToBSCS(self.cdrPath, cdrLocation,i)
                            
                            showinfo("INFO", str(self.cnt)+" CDRs successfully generated and sent to BSCS.")
                            break
                
                    else:
                        showinfo("INFO",str(self.cnt)+" CDRs successfully generated.")
                        break
                
                except ValueError as e :
                    showinfo('ERROR',e)
                    break
                except IOError as e :
                    showinfo('ERROR','Cannot send CDR to remote location. Try do this by yourself.')
                    print(str(e))
                    break
                except paramiko.ssh_exception.SSHException as e:
                    showinfo('ERROR','Something wrong with private key or AIX user.')
                    print(str(e))
                    break
                       
                        
            except cx_Oracle.DatabaseError as e:
                showinfo("Something wrong with database. ", e)
                break
            except FileNotFoundError as e:
                showinfo('File with CDR patterns not found.',e)
                break
            
        
            except UnboundLocalError as e:
                showinfo('CDR pattern not found.',e)
                break
   
   
    def setConf(self,sv):
        print(sv.get())
    def __init__(self):
        
        tk.Tk.__init__(self)
        '''
        data parameters mandatory to generate CDR
        '''
        
        self.title("CzeDaR - CDR Generator")
        
        '''
        Configuration frame containing following labels and entries:
        - Database connection in format user/pass@database
        - Host for database
        - AIX user
        - path to Private Key for AIX user
        - AIX Host
        
        '''
        
        self.queue = queue.Queue()
        tk.Tk.resizable(self,width=False, height=False)
        self.frameConf=tk.LabelFrame(self,text="Environment:")
        self.frameConf.grid(row=0,padx=0,pady=10,columnspan=5, ipady=20,ipadx=5,sticky='WE')
      
        '''
        Database
        
        self.database=tk.StringVar()
        
        #self.database.trace("w",lambda name, index, mode, sv=self.database: self.setConf(self.database))
        self.labelDatabase=tk.Label(self.frameConf,text="Database")
        self.labelDatabase.grid(row=0,column=0,padx=0,sticky='W')
        self.entryDatabase=tk.Entry(self.frameConf,width=30,textvariable=self.database)
        self.entryDatabase.grid(row=0,column=1,sticky='W')
        self.entryDatabase.bind('<Key>', self.enterCoId)
        #self.database.trace("w", print(self.database))
        
        
        
        Host for Database
        
        
        self.labelDatabaseHost=tk.Label(self.frameConf,text="DB Host").grid(row=1,column=0,sticky='W')
        self.entryDatabaseHost=tk.Entry(self.frameConf,width=30)
        self.entryDatabaseHost.grid(row=1,column=1,sticky='W')
        self.entryDatabaseHost.bind('<Key>', self.enterCoId)
        
       
        Port for Database
       
        
        self.labelDatabasePort=tk.Label(self.frameConf,text="DB Port").grid(row=2,column=0,sticky='W')
        self.entryDatabasePort=tk.Entry(self.frameConf,width=30)
        self.entryDatabasePort.grid(row=2,column=1,sticky='W')
        self.entryDatabasePort.bind('<Key>', self.enterCoId)
        
        AIX user
      
        
        self.labelAixUser=tk.Label(self.frameConf,text="AIX User").grid(row=3,column=0,sticky='W')
        self.entryAixUser=tk.Entry(self.frameConf,width=30)
        self.entryAixUser.grid(row=3,column=1,sticky='W')
         
        '''
        '''
        Private Key Path
        '''
        
        self.labelPkPath=tk.Label(self.frameConf,text="Path to Private Key").grid(row=5,column=0,sticky='W')
        self.entryPkPath=tk.Entry(self.frameConf,width=60)
        self.entryPkPath.grid(row=5,column=1,sticky='W')
        self.browsePkPath = tk.Button(self.frameConf, text="Browse",command=lambda: self.browseFileButton(self.entryPkPath)).grid(row=5,column=2,padx=10,ipadx=25,sticky='W')
        
        '''
        AIX Host
       
        
        self.labelAixHost=tk.Label(self.frameConf,text="AIX Host").grid(row=5,column=0,sticky='W')
        self.entryAixHost=tk.Entry(self.frameConf,width=30)
        self.entryAixHost.grid(row=5,column=1,sticky='W')
        
        '''
        '''
        Environment combo box
        '''
        self.envList=[]
        
        self.chosenEnv = tk.StringVar()
        self.labelenvCombo=tk.Label(self.frameConf,text="Choose environment:").grid(row=4,column=0,sticky='W')
        self.envCombo=tkinter.ttk.Combobox(self.frameConf,width=57,textvariable=self.chosenEnv,values=self.envList, state='readonly')
        self.envCombo.grid(row=4,column=1,sticky='W')
        
        self.envCombo.bind("<<ComboboxSelected>>",self.refreshConfig)
        
        
        
        '''
        Contract Info frame containing following labels and entries:
        - Contract Id
        - Directory number
        - Port
        - Tmcode
       
        
        
        
        self.frameCoInfo=tk.LabelFrame(self,text="Contract Info:")
        self.frameCoInfo.grid(row=0,column=1,padx=0, pady=5, ipady=20,ipadx=5,rowspan=50,sticky='WN')
        
        
        contract Id
       
        self.labelContractId=tk.Label(self.frameCoInfo,text="Contract Id").grid(row=0,column=0,sticky='W')
        self.entryContractId=tk.Entry(self.frameCoInfo,width=30)
        self.entryContractId.grid(row=0,column=1,sticky='W')
        
       
        Tmcode
        
        self.labelRateplan=tk.Label(self.frameCoInfo,text="Rateplan").grid(row=1,column=0,sticky='W')
        self.entryRateplan=tk.Entry(self.frameCoInfo,width=30)
        self.entryRateplan.grid(row=1,column=1,sticky='W')
        
        
        directory number
       
        self.labelDirectoryNumber=tk.Label(self.frameCoInfo,text="Directory Number").grid(row=2,column=0,sticky='W')
        self.entryDirectoryNumber=tk.Entry(self.frameCoInfo,width=30)
        self.entryDirectoryNumber.grid(row=2,column=1,sticky='W')
        
        port
        
        self.labelPort=tk.Label(self.frameCoInfo,text="Port").grid(row=3,column=0,sticky='W')
        self.entryPort=tk.Entry(self.frameCoInfo,width=30)
        self.entryPort.grid(row=3,column=1,sticky='W')
        
        '''
        '''
        CDR generator frame containing following labels and entries:
        - Contract Id
        option menus:
        - zones
        
        
        check boxes:
        - send to BSCS flag
        
        buttons:
        - generate CDR 
       
        
        '''
        self.frameCdrGenerator=tk.LabelFrame(self,text="CDR Generator:")
        self.frameCdrGenerator.grid(row=1,padx=0,pady=10,columnspan=5, ipady=20,ipadx=5,sticky='WE')
        self.listbox = tk.Listbox(self.frameCdrGenerator, width=20, height=5)
        '''
         contract Id
           '''
        #self.coId=''  
        
        self.labelContractId=tk.Label(self.frameCdrGenerator,text="Contract Id").grid(row=0,column=0,sticky='W')
       
        self.entryContractId=tk.Entry(self.frameCdrGenerator,width=60)
        self.entryContractId.bind('<Key>', self.enterCoId)
        
        #self.coId.set('123')
        self.entryContractId.grid(row=0,column=1,sticky='W')
        
        
        '''
        drop down menu with type of call
        '''
        self.labelChosenCall=tk.Label(self.frameCdrGenerator,text="Get Configuration: ").grid(row=1,column=0,sticky='W')
        self.var1 = tk.StringVar()
        self.chosenCall=''
        self.chosenCallList=['']
        
        for key in CdrGenerator._callDict:
            self.chosenCallList.append(key)
        
         
        self.chosenCallList.sort(reverse=False)
        
        self.comboChosenCall =tkinter.ttk.Combobox(self.frameCdrGenerator, textvariable=self.var1,width=57,values=self.chosenCallList, state='readonly')
        
        self.comboChosenCall.current(0)
        self.comboChosenCall.grid(row=1,column=1,sticky='W')
        
        self.comboChosenCall.bind("<<ComboboxSelected>>",self.getCoRatingConfiguration)
        
        self.comboZncodes=None
       
        '''
        duration/data volume
        '''
        self.labelDuration=tk.Label(self.frameCdrGenerator,text="Duration/Data Volume:")
        self.labelDuration.grid(row=4,column=0,sticky='W')
        self.entryDuration=tk.Entry(self.frameCdrGenerator,width=60)
        self.entryDuration.insert(0, "")
        self.entryDuration.grid(row=4,column=1,sticky='W')
        self.labelDuration.grid_remove()
        self.entryDuration.grid_remove()
        
        '''
        CDR Path
        '''
        self.frameCdrGenerator.columnconfigure(1, weight=1)
        
        self.labelCdrPath=tk.Label(self.frameCdrGenerator,text="Save CDR to: ").grid(row=6,column=0,sticky='W')
        self.entryCdrPath=tk.Entry(self.frameCdrGenerator,width=60)
        self.entryCdrPath.grid(row=6,column=1,sticky='W')
        self.browseCdrPath = tk.Button(self.frameCdrGenerator, text="Browse",command=lambda: self.browseDirectoryButton(self.entryCdrPath)).grid(row=6,column=2,padx=10,ipadx=25,sticky='W')
        
       
       
        '''
        overwrite CDR flag
        '''
       
        self.ovw=tk.IntVar()
        self.chk_button_overwrite=tk.Checkbutton(self.frameCdrGenerator,text="Overwrite CDR file"
                                              ,variable=self.ovw,anchor='se',indicatoron=True
                                              )
        self.chk_button_overwrite.grid(row=7,column=0)
        self.chk_button_overwrite.config(state="disabled")
        
                
        '''
        send to BSCS flag
        '''
       
        self.var=tk.IntVar()
        self.chkButtonBscsFlag=tk.Checkbutton(self.frameCdrGenerator,text="Send CDR to BSCS"
                                              ,variable=self.var,anchor='se',indicatoron=True
                                              ).grid(row=8,column=0)
        
        
        
        
    
        '''
        Generate CDR Button
        '''
        
        self.generateCDRButton = tk.Button(self.frameCdrGenerator, text="Generate CDR")
        self.generateCDRButton.grid(row=9,column=1,sticky='WE')
        self.generateCDRButton.bind("<ButtonRelease-1>",self.generateCDR)
        self.generateCDRButton.grid_remove()
        

        
        '''
        self.getRatConf = tk.Button(self.frameCdrGenerator, text="Get Rating Configuration for Contract")
        self.getRatConf.grid(row=8,column=1,sticky='W')
        self.getRatConf.bind("<ButtonRelease-1>",self.getCoRatingConfiguration)
        self.getRatConf.grid_remove()
        '''
        '''
                
        self.var = tk.StringVar()
        self.var.set("one") # initial value

        option = tk.OptionMenu(self, self.var, "one", "two", "three", "four")
        option.grid(row=0,column=3)



        '''
        
        time.sleep(1)
        #self.readConfig()
        self.readNewConfig()
        self.mainloop()
        
    
            

    
      
w = CzedarApp()

