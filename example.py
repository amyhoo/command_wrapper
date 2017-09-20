# -*- coding: utf-8 -*-
'''
author:Amy Hoo
email:xuyamin@gmail.com
created at:2017/9/20
'''
from .commandClient import *

def trackFiles(filename,*args,**params):
    with CommandClient(*args,**params) as client:
        stdout, stderr = client.exec_command('ls ' + filename)
        if stderr:
            error_msg = stderr
            print(error_msg)
        else:
            info = {}
            with  OpenFile(filename, client=client) as remote_file:
                for line in remote_file.readline():
                    print(line)