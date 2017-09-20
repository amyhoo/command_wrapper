'''
Created on 18 Aug 2016
@author: xuyamin(yamin_xu@163.com)
this module use as ssh client to execute command or open file on server
'''
import paramiko
import subprocess
import sys
class CommandClient:
    def __init__(self,server=None,port=0,user=None,pwd=None):
        '''
        if server==None, then it is local machine
        '''
        self.server=server
        self.port=port
        self.user=user
        self.pwd=pwd
        self.client=None
        self.session=None

    def __enter__(self):
        if self.server and self.port and self.user and self.pwd:
            try:
                self.client=paramiko.SSHClient()
                self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.client.connect(self.server, self.port, self.user, self.pwd)
                self.session=self.client.open_sftp()
            except Exception as e:
                self.__exit__(*sys.exc_info())
                raise
        return self
    
    def __exit__(self,exc_type,exc_val,exc_tb):
        if self.server:
            if self.session:self.session.close()
            if self.client:self.client.close()
                
    def exec_command(self,*args,**kwargs):
        '''
        if self.server is remote ,then use ssh client
        else use subprocess.Popen to execute command
        :param args:
        :param kwargs:
        :return:
        '''
        if self.server:
            stdin, stdout, stderr = self.client.exec_command(*args,**kwargs)
            stdout=stdout.read() if stdout else ''
            stderr=stderr.read() if stderr else ''
        else:
            pipe=subprocess.Popen(*args,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,**kwargs)                
            stdout, stderr = pipe.communicate()
        return (stdout,stderr)
    
    def __getattr__(self,attr):
        '''
        if have remote server then use session to do things
        else use locale command file operate function pen
        :param attr:
        :return:
        '''
        if self.server:
            if attr=='file':
                return getattr(self.session,attr)
            return getattr(self.client, attr)
        else:
            if attr=='file':
                return open
            else:#no other function
                return None
            
class  OpenFile:
    
    def __init__(self,filename,mode='r',client=None):
        '''
        :param filename:
        :param mode:
        :param client: command client
        '''
        self.client=client       
        self.filename=filename
        self.mode=mode   
        self.file=None

    def __enter__(self):
        try:
            self.file=self.client.file(self.filename,self.mode)
        except Exception as e:
                raise
        return self.file
    
    def __exit__(self,exc_type,exc_val,exc_tb):
        if self.file:self.file.close()
