#coding=utf-8
import datetime
from web import storage

__author__ = 'pcode@qq.com'

import os
from evn import TP_PATH
class s_log():
    syslogs = []
    optlogs = []
    def __init__(self):
        self.syslogs=[]
        self.optlogs=[]
        self.getLogs()

    def readlog(self,file_name):
        rr = None
        for r in self.syslogs:
            if r.file_name==file_name:
                rr=r
        for r in self.optlogs:
            if r.file_name==file_name:
                rr=r
        file_object = open(rr.file_path)
        try:
             all_the_text = file_object.read( )
        finally:
             file_object.close( )
        return all_the_text

    def getLogs(self):
        """
        获取系统日志
        :return:
        """
        log_path = TP_PATH+"/log"
        files = os.listdir(log_path)
        tmp     = []
        for file in files:
            log_file_info = storage()
            log_file_info.file_name = file
            log_file_info.file_path = log_path+"/"+file
            log_file_info.file_createtime = os.path.getctime(log_file_info.file_path)
            log_file_info.file_createtime = datetime.datetime.fromtimestamp(log_file_info.file_createtime)
            #字节大小
            bitssize    = os.path.getsize(log_file_info.file_path)
            bits_size   = ""
            if bitssize<1024:
                bits_size = "%s 字节"%bitssize
            if 1024 <= bitssize < 1024*10224:
                bits_size = "%s K"%round(float(bitssize)/1024,2)
            if bitssize>=1024*1024:
                bits_size = "%s M"%round(float(bitssize)/(1000*1000),2)
            log_file_info.file_size = bits_size
            tmp.append(log_file_info)
        for r in tmp:
            fn = str(r.file_name)
            if fn.startswith('syslog'):
                self.syslogs.append(r)
            if fn.startswith('opt'):
                self.optlogs.append(r)

if __name__ == '__main__':
    opt_log = s_log()
    print opt_log.readlog('opt.txt')
