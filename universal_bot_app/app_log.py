# coding: utf8 

import datetime

def appendLog(log_string):
    print ('[' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] ' + log_string)
