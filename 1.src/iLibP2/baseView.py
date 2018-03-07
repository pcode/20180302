#coding=utf-8
from evn import TP_PATH
from iLibP2.ixls import iXls
from utils import TimeStr, toJson
import copy
__author__ = 'pcode@qq.com'
from config import GLOBAL_LOOKUP as T
class BaseView:
    def __init__(self):
        pass

    def display(self,templatefile,**kwargs):
        """
        显示模板
        :param templatefile:
        :param kwargs:
        :return:
        """
        t = T.get_template(templatefile)
        return t.render(**kwargs)
    def export(self,i,opt_obj,filterfun):
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
        fields = copy.deepcopy(opt_obj.fields)
        fields.remove('id')
        cnfields = copy.deepcopy(opt_obj.cnfields)
        cnfields.remove(u'序号')
        for f in  cnfields:
            ws.write(row,col,f)
            col+=1
        row +=1
        #更改页面大小防止分页影响
        i.pagesize=999999
        datas=filterfun(i)
        for d in datas.recs:
            col = 0

            for f in fields:
                ws.write(row,col,d[f])
                col +=1
            row+=1
            #3.输出excel

        nfilename = gcPath()+"/"+TimeStr()+".xls"
        wb.save(TP_PATH+nfilename)
        return toJson({'result':"OK","filename":nfilename})


if __name__ == '__main__':
    fields =['id','hahha','tett']
    fields.remove('tett')
    print fields