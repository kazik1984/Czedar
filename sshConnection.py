'''
Created on 18 paz 2016

@author: PI345811
'''
import paramiko
import os
import sys

class SshConnection():
    '''
    classdocs
    '''

    def __init__(self,host,user,pkpath):
        self.host=host
        self.user=user
        self.pkpath=pkpath
        
        
   
    def sendCDRToBSCS(self,cdr_path,remote_cdr_path,fileName):
        try:
           
            cdrLocation=cdr_path+fileName
            remoteLocation=remote_cdr_path+fileName
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            privatekeyfile = os.path.expanduser(self.pkpath)
            mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
            ssh.connect(self.host, username=self.user, pkey=mykey)
            sftp = ssh.open_sftp()
            sftp.put(cdrLocation,remoteLocation)
            
            ssh.close()
        except IOError:
            print('Cannot send CDR to remote location. Try do this by yourself.')
            raise
        
        
       
        
        
           
    def runCommandOnShell(self,command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        privatekeyfile = os.path.expanduser(self.pkpath)
        mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
        ssh.connect(self.host, username=self.user, pkey=mykey)
        stdin, stdout, stderr = ssh.exec_command(command)
        stout=stdout.readlines()
        sterr=stderr.readlines()
        ssh.close()
        
        return stout, sterr
        
    def printOutput(self,stout):
        list_len=len(stout)
        for i in range(0,list_len):
            print(stout[i])
       
    
