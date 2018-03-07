#coding=utf-8
__author__ = 'pcode@qq.com'
from evn import TP_PATH
from iLibP2.ixls import iXls
from utils.tools import TimeStr, toJson

def doexport(cnfields,fields,recs):
    """
    cnfields
    :param i:
    :param opt_obj:
    :param filterfun:
    :return:
    """
    def gcPath():
        import datetime,os
        """
        创建上传目录，按月度处理上传的文件内容。避免一个目录的文件太多难以管理
        如果以后使用分布式来做，可以改造这个函数来处理
        :return:目录名
        """
        now_month = datetime.datetime.now().strftime("%Y%m")
        tpath="/static/uploads/"+now_month
        if not os.path.exists(TP_PATH+tpath):
            os.mkdir(TP_PATH+tpath)
        return tpath
    excelobj=iXls()
    wb,ws=excelobj.openExistExcel(TP_PATH+"/static/blank.xls")
    row = 0
    col = 0
    #写头部数据
    for f in  cnfields:
        ws.write(row,col,f)
        col+=1
    row +=1
    #更改页面大小防止分页影响
    for d in recs:
        col = 0
        for f in fields:
            ws.write(row,col,d[f])
            col +=1
        row+=1
        #3.输出excel
    nfilename = gcPath()+"/"+TimeStr()+".xls"
    wb.save(TP_PATH+nfilename)
    return toJson({'result':"OK","filename":nfilename})