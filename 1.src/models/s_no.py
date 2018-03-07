#coding=utf-8
import thread
import threading
import time
from web import storage

__author__ = "jy@cjlu.edu.cn"
from iLibP2.dalbase import DalBase

class s_no(DalBase):
    """
    用于处理与数据表s_no进行持久化操作的相关功能
    调用iLibp的基础函数
    """
    fields = {'id':u'序号','type':u'类别','no':u'序号值','date':u'日期'}
    def __init__(self):
        DalBase.__init__(self,"s_no","id",self.fields)

mutex = thread.allocate_lock()
obj = s_no()

def GC_COUNT(header,count_len,renew):
    """
    创建顺序号
    @param header:头
    @param count_len:长度
    @param renew: 是否需要每日重置
    @return:count_len长度的顺序号
    """
    global mutex
    if mutex.acquire():
        try:
            datestr = time.strftime('%Y%m%d', time.localtime(time.time()))
            i = obj.GetRowByDbWhere(where=" type =$header",vars={'header':header})
            counter="".zfill(count_len)
            if i==None:
                if renew:
                    i=storage({"id":0,"type":header,"no":0,"date":datestr})
                else:
                    i=storage({"id":0,"type":header,"no":0})
                obj.Save(i)
                i = obj.GetRowByDbWhere(where=" type =$header",vars={'header':header})
            if i<>None:
                if renew:#如果需要每天重置
                    if i.date == datestr:
                        counter = int(i.no)+1
                    else:
                        counter = 1
                else:#如果不需要每天重置
                    counter = int(i.no)+1
                i.no=counter
                obj.Save(i)
            sn=header+str(counter).zfill(count_len)
            return sn
        except Exception,ex:
            msg="创建序列号失败，具体信息:"+str(ex)
            raise Exception(msg)
        finally:
            mutex.release()

def GC_SN(header):
    """
    线程安全的符合编号生成规则的函数。
    created by jxf 2013-06-07
    @param header:编号头字符
    @return:符合 头2位+日期8位+4位序号规则的编号字符串
    """
    #获取全局锁
    global mutex
    #定义顺序号的长度
    COUNT_LEN=4
    #申请锁
    if mutex.acquire():
        datestr = time.strftime('%Y%m%d', time.localtime(time.time()))
        sn=""
        try:
            i = obj.GetRowByDbWhere(where=" type = $header",vars={'header':header})
            if i==None:
                #added by jy 2013-08-08 在无法取到字头的情况下，直接补充字头的信息
                i=storage({"id":0,"type":header,"no":0,"date":datestr})
                obj.Save(i)
                i = obj.GetRowByDbWhere(where=" type = $header",vars={'header':header})
            if i <> None:
                if i.date == datestr:
                    counter = int(i.no)+1
                else:
                    counter = 1
                i.no = counter
                i.date = datestr
                obj.Save(i)
                sn= header+datestr+str(counter).zfill(COUNT_LEN)
            #释放锁
            mutex.release()
            return sn

        except  Exception,ex:
            msg="创建编号失败:"+str(ex)
            mutex.release()
            raise Exception(msg)
if __name__=="__main__":
    print s_no().GetFieldDefs()
    def GETsn():
       #print GC_SN("YHJK1")
        print GC_COUNT("BANK",4,True)
    for i in xrange(100):
        thread1 = threading.Thread(target=GETsn)
        thread1.start()