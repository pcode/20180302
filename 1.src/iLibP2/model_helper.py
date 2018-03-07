#coding=utf-8
"""
在youliaoo团队内使用的模版代码生成程序
created by jy
2017-10-07 updated by jy
"""
__author__="pcode@qq.com"
from web import storage
from config import GLOBAL_DB as dbs
from config import MYSQL_CONN
from config import GLOBAL_LOOKUP as T
import os

class MHelper:
    """
    创建模板用的代码
    """
    def __init__(self):
        """
        按数据库名称初始化
        """
        #数据库
        self.db         = dbs.db[MYSQL_CONN]
        #从配置文件中读取数据配置的数据库名称
        self.dbname     = "yl_jk"
        #从配置文件中读取环境配置的临时路径的位置
        self.temp_dir   = "C:/iLibP2"
        
    def getColsComments(self,tablename):
        """
        读取数据表的字段和注释信息
        """
        sqlt='select column_name colname,column_comment colcomment from INFORMATION_SCHEMA.Columns where table_name=$tablename and table_schema=$dbname'
        recs=self.db.query(sqlt,vars={'tablename':tablename,'dbname':self.dbname})
        return recs.list()
    def saveRenderResult(self,subdir,filename,renderResult):
        """
        保存render的结果到文件
        """
        if not os.path.exists(self.temp_dir):
            os.mkdir(self.temp_dir)
        filepath = self.temp_dir+"/"+subdir+"/"
        if not os.path.exists(filepath):
            os.mkdir(filepath)
        fpath = filepath+filename
        ofile = open(fpath,"wb")
        ofile.write(renderResult)
        ofile.close()
        print u"文件保存至%s"%fpath
    def gc_model(self,**kwargs):
        t0                  = T.get_template("iLibP2/T/model.mako")
        modelresult         = t0.render(**kwargs)
        mhobj.saveRenderResult("models",kwargs['tablename']+".py",modelresult)
    def gc_0(self,**kwargs):
        """
        创建list文件
        :param kwargs:
        :return:
        """
        t0                  = T.get_template("iLibP2/T/list_0.mako")
        modelresult         = t0.render(**kwargs)
        mhobj.saveRenderResult(kwargs['mn']+"/T",kwargs['fn']+"_0.html",modelresult)
    def gc_fun(self,**kwargs):
        """
        创建fun文件
        :param kwargs:
        :return:
        """
        t0                  = T.get_template("iLibP2/T/fun.mako")
        modelresult         = t0.render(**kwargs)
        mhobj.saveRenderResult(kwargs['mn'],kwargs['fn']+".py",modelresult)
    def gc_1(self,**kwargs):
        """
        创建list文件
        :param kwargs:
        :return:
        """
        t0                  = T.get_template("iLibP2/T/list_1.mako")
        modelresult         = t0.render(**kwargs)
        mhobj.saveRenderResult(kwargs['mn']+"/T",kwargs['fn']+"_1.html",modelresult)
    def gc_2(self,**kwargs):
        """
        创建list文件
        :param kwargs:
        :return:
        """
        t0                  = T.get_template("iLibP2/T/list_2.mako")
        modelresult         = t0.render(**kwargs)
        mhobj.saveRenderResult(kwargs['mn']+"/T",kwargs['fn']+"_2.html",modelresult)
    def gc_3(self,**kwargs):
        """
        创建list文件
        :param kwargs:
        :return:
        """
        t0                  = T.get_template("iLibP2/T/list_3.mako")
        modelresult         = t0.render(**kwargs)
        mhobj.saveRenderResult(kwargs['mn']+"/T",kwargs['fn']+"_3.html",modelresult)
    def GC_OneTable(self,tablename="",mn="",fn="",fm=""):
        """
        用于创建一个表的操作
        :param tablename: 表格
        :param mn: 模块名称
        :param fn: 功能编号
        :param fm: 功能备注
        :return:
        """
        args                = storage()
        args.mn             = mn
        args.fn             = fn
        args.tablename      = tablename
        args.functionmemo   = fm
        cols                = self.getColsComments(args.tablename)
        args.colnames       = [rec.colname for rec in cols]
        args.colcomments    = [rec.colcomment for rec in cols]
        args.recs           = cols
        self.gc_model(**args)
        self.gc_fun(**args)
        self.gc_0(**args)
        self.gc_1(**args)
        self.gc_2(**args)
        self.gc_3(**args)
        print u'"/%s/list",      "%s.%s.List",                  #%s 显示数据用'%(fn,mn,fn,fm)
        print u'"/%s/update",    "%s.%s.Update",		        #%s 修订数据用'%(fn,mn,fn,fm)
        print u'"/%s/import",    "%s.%s.Import",		        #%s 导入数据'%(fn,mn,fn,fm)
        print u'"/%s/export",    "%s.%s.Export",		        #%s 导出数据'%(fn,mn,fn,fm)

if __name__=="__main__":
    mhobj               = MHelper()
    #构建参数
    args                = storage()
    args.mn             = "F20"
    args.fn             = "F2013"
    args.tablename      = "d_xk"
    args.fm             = "消息日志"
    mhobj.GC_OneTable(**args)
