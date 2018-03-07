#coding=utf-8
"""
iLibP是iLib库的Python迁移版本
代码量大量下降
@author:姜源
@license:
2017-10-24 删减了不少利用率很低的函数
2017-10-07 改进细节
2017-10-03 将dabase与isql整合，用模板来定义语句提高开发效率
同时将数据库配置迁移到xml文件
1.注意此库用于jy团队的商业项目开发

2.团队内人员可随意使用,严禁对外发布源码

3.团队内人员离开团队后使用此库开发其他商业项目须事先征得jy允许

@contact: jy@cjlu.edu.cn
@version:2.0
"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import traceback,json
from web.utils import storage
from config import GLOBAL_DB,MYSQL_CONN
from loger import *



class DalBase(object):
    def __init__(self, table_name="", key_field="id", fields=None):
        """
        @rtype : object
        @param table_name: 数据表名称
        @type table_name: 字符类型
        @param key_field: 关键字段 一般为id
        @type key_field: 字符类型
        @param fields: 数据表字段
        @type fields: 字符数组
        """
        if fields is None:
            fields = {}
        #获取mysql连接
        self.db         = GLOBAL_DB.db[MYSQL_CONN]     #数据库连接
        self.table_name = table_name                #表名
        self.fields     = fields.keys()             #字段名
        self.fielddefs  = fields                    #字段定义
        self.cnfields   = fields.values()           #中文字段名
        self.key_field  = key_field                 #主键名

    def GetRowById(self,id):
        """
        根据id来获取一行
        @note:如果获得的结果是多行，则默认取第一行返回
        @param id: 主键
        @type id: int
        @return:一条记录，类型为storage
        """
        try:
            recs=self.db.select(self.table_name,where=self.key_field+'=$id',vars={'id':id},limit=1)
            return recs[0]
        except Exception,ex:
            msg=u"iLib执行GetRowById函数出错,[具体信息]:"+str(traceback.format_exc())+u",\n[参数]:\n"+str(id)+u"\n[数据]:\n"+str(ex)
            LogError(msg)
            return None

    def CheckHave(self,**dbwhere_args):
        """
        检查是否存在记录
        :return:
        """
        dbwhere_args['what'] =self.key_field
        row = self.GetRowByDbWhere(**dbwhere_args)
        if row:
            return True
        else:
            return False
    def GetRowByDbWhere(self,**where_args):
        """根据DBWhere条件来获取一行
        @note:如果获得的结果是多行，则默认取第一行返回
        @param where_args: where条件 如：where="id=$i",vars={"i":id}
        @type where_args: 字典
        @return:一条记录，类型为storage
        """
        try:
            recs=self.db.select(self.table_name,**where_args)
            if recs:
                return recs[0]
        except Exception,ex:
            msg=u"GetRowByDbWhere,[具体信息]:"+str(traceback.format_exc())+u",\n[参数]:\n"+str(where_args)+u"\n[数据]:\n"+str(ex)
            LogError(msg)
            #return None
            raise Exception,msg
    def GetRowsByDbWhere(self,**where_args):
        """根据DBWhere条件来获取记录集
        @param where_args: where条件 如：where="id=$i",vars={"i":id}
        @type where_args: 字典
        @return:单向只读迭代器，每次迭代的单次值为storage
        """
        try:
            recs=self.db.select(self.table_name,**where_args)
            return recs
        except Exception,ex:
            msg=u"iLib执行GetRowsByDbWhere函数出错,[具体信息]:"+str(traceback.format_exc())+u",\n[参数]:\n"+str(where_args)+u"\n[数据]:\n"+str(ex)
            LogError(msg)
            raise Exception,msg
    def DelRowsByDbWhere(self,**whereargs):
        """根据DBWhere条件来删除记录集
        @param whereargs: where条件 如：where="id=$i",vars={"i":id}
        @type whereargs: 字典
        @return:删除结果
        """
        try:
            i=self.db.delete(self.table_name,**whereargs)
            return i
        except Exception,ex:
            msg=u"iLib执行DelRowsByDbWhere函数出错,[具体信息]:"+str(traceback.format_exc())+u",\n[参数]:\n"+str(ex)
            LogError(msg)
            raise Exception,msg
    def SaveEx(self,obj,fields=["id"]):
        """
        可指定保存或更新某些字段的保存函数
        @note:fields中一定要包括id
        @param obj: 需要保存的对象
        @type obj: storage
        @param fields: 需要保存的属性
        @type fields: 字符串数组
        """
        try:
            nobj=storage()
            for k in fields:
                nobj[k]=obj.get(k,None)
            self.Save(nobj)
        except Exception,ex:
            msg=u"iLib执行SaveEx函数出错,[具体信息]:"+str(traceback.format_exc())+u",\n[参数]:\n"+str(obj)+u"\n[数据]:\n"+str(ex)
            LogError(msg)
            raise Exception,msg
    def Save(self,obj):
        """
        保存函数，可将storage对象保存到指定的数据表
        @note:fields中一定要包括id
        @param obj: 需要保存的对象
        @type obj: storage
        """
        try:
           #过滤掉传入对象中与数据无关的属性,再用于操作数据
            objn=storage()
            for key in self.fields:
                #如果没有的属性则不写入，避免污染原有属性的值 updated by jy 2011-10-08
                #updated by jy 2012-07-11强制None判断
                if obj.get(key,None)!=None:
                    objn[key]=obj.get(key,None)
            if objn.get(self.key_field,None) is None:                    #要求传入参数中必须包括主键信息
                raise Exception,u"传入数据需要包括数据表的主键属性值"
            else:
                row = self.GetRowById(objn[self.key_field])
                if row:
                    #更新时不写入主键信息
                    self.db.update(self.table_name,where=self.key_field+"=$id",vars={"id":objn[self.key_field]},**objn)
                else:
                    self.db.insert(self.table_name,**objn)
        except Exception,ex:
            msg=u"iLib执行Save函数出错,[具体信息]:"+str(traceback.format_exc())+u",\n[参数]:\n"+str(obj)+u"\n[数据]:\n"+str(ex)
            LogError(msg)
            raise Exception,msg
    def UpdateValues(self,where,vars,**kwargs):
        """
        根据条件更新数据表列值 where="id=$id",vars={'id':id},userstatus='on',后面可以继续补充需要更新的字段
        :return:
        """
        self.db.update(self.table_name,where,vars,**kwargs)
    def UpdateColValueByStrWhere(self,strwhere,col,value):
        """
        更新某列数据值，不论给定值是何值，直接更新
        @param strwhere:where参数
        @param col:列名
        @param value:需要更新的值
        """
        try:
            #通过语句来完成项目值修订
            self.db.query("update "+self.table_name+" set "+col+"=$v where "+self.Conn.safewhere(strwhere),vars={"v":value})
            return value
        except Exception,ex:
            #编码参数
            args=json.dumps((self.table_name,id,col,value))
            msg=u"iLib执行UpdateColValue函数出错,[具体信息]:"+str(traceback.format_exc())+u",\n[参数]:\nid:"+args+u",\n[数据]:\n"+str(ex)
            LogError(msg)
            return None
    def GetCount(self,**dbwhere):
        """
        获取指定查询条件下得记录数量
        @param dbwhere: 查询条件 如：where="id>$i",vars={"i":id}
        @type dbwhere: 字典
        """
        try:
            dbwhere["what"]="count(id) as rc"
            del dbwhere['order']
            r=self.db.select(self.table_name,**dbwhere)
            return r[0].rc
        except Exception,ex:
            msg=u"iLib执行GetCount函数出错,[具体信息]:"+str(traceback.format_exc())
            LogError(msg)
            raise Exception,msg
    def GetPagedRowsByDbWhere(self,pageindex,pagesize,**dbwhere):
        """
        获取某查询条件下的指定页号数据集
        @note:
        特别注意这里的pageindex从0开始计算，如果计算第一页则需要传入0
        @param pageindex:页号
        @type pageindex:int
        @param pagesize:每页记录数
        @type pagesize:int
        @param dbwhere: 查询条件 如：where="id>$i",vars={"i":id}
        @type dbwhere: 字典
        @return: 记录集,总记录数,总页数
        """
        pageindex=int(pageindex)
        pagesize=int(pagesize)
        #总记录数
        recordercount=self.GetCount(**dbwhere)
        #总页数
        pagecount = recordercount/pagesize
        if recordercount%pagesize != 0:
            pagecount += 1
        #分页结果
        offset= pageindex *pagesize
        dbwhere["offset"]=offset
        dbwhere["limit"]=pagesize
        result=self.db.select(self.table_name,**dbwhere)
        return result,recordercount,pagecount
    def Transaction(self):
        """
        开始数据库事务
        @return:事务 如:t=obj.Transaction()
        """
        return self.db.transaction()
    def RollBack(self,t):
        """
        回滚数据库事务
        如:t.rollback()
        """
        t.rollback()
    def Commit(self,t):
        t.commit()
    def GetFieldDefs(self):
        '''
        创建自己用的fields的定义
        :return:
        '''
        sqlstr ="""
                SELECT column_name colname,column_comment colcomment
                FROM INFORMATION_SCHEMA.Columns
                WHERE table_name='%s' AND table_schema='%s'
                """%(self.table_name,GLOBAL_DB.dbargs['db'])
        recs = self.db.query(sqlstr)
        result = []
        for rec in recs:
            result.append("'%s':u'%s'"%(rec.colname,rec.colcomment))
        return "{%s}"%",".join(result)
