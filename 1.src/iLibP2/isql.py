#coding=utf-8
from evn import TP_PATH
__author__ = 'pcode@qq.com'
"""
iSQL组件，把数据库的配置参数和sql语句模板的操作做了一些封装
从ibatis那里得到了一些启发，在sqlmapcongif.xml中可以定义更多的sql模板定义，方便起见可以分别定义到多个xml文件中去
2017-11-20 updated by pcode@qq.com 去掉了一些没用的设定
2017-10-07 created by pcode@qq.com
用于youliaoo.com团队内使用
目支持oracle mysql
"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import traceback,web
from xml.etree import ElementTree as ET
from mako.template import Template
from loger import LogError, LogInfo


class iSQL:
    #数据源，默认用一个，需要其他数据源的时候再定义其他的配置文件
    def __init__(self,sqlmapconfig="isqlconfig.xml"):
        """
        初始化 默认读取sqlmapconfig.xml文件来获取数据库参数
        :param sqlmapconfig:
        :return:
        """
        try:
            self.db         = {}
            self.sqlmaper   = {}
            #读取xml解析的根目录
            self.__root     = ET.parse(TP_PATH+"/"+sqlmapconfig)
            #读取数据源配置
            self.__getDbConn()
            #读取配置文件中定义的语句模板
            self.__getSQLs()

        except Exception,ex:
            msg=u"iSQL初始化出错,[具体信息]:"+str(traceback.format_exc())+u",[数据]:\n"+str(ex)
            LogError(msg)
            raise Exception,msg
        #读取sql语句配置
    def __getDbConn(self):
        """
        获取数据库连接信息
        :return:
        """
        try:
            dsd = self.__root.findall('dataSource')
            for ds in dsd:
                dbargs = {}
                for c in ds.getchildren():
                    if c.attrib['name']=='port':
                        dbargs[c.attrib['name']]=int(c.attrib['value'])
                    else:
                        dbargs[c.attrib['name']]=c.attrib['value']
                #如果已经实例化过了就不在实例化了
                self.db[ds.attrib['name']] =  web.database(**dbargs)
        except Exception,ex:
            msg=u"iSQL执行__getDbConn函数出错,[具体信息]:"+str(traceback.format_exc())+u",[数据]:\n"+str(ex)
            LogError(msg)
            raise Exception,msg

    def __getSQLs(self):
        """
        获取语句
        :return:
        """
        try:
            for mp in self.__root.iter('mapper'):
                mpfile = mp.attrib['resource']
                mp_root = ET.parse(TP_PATH+"/"+mpfile)
                mp_root_obj = mp_root.getroot()
                for query in mp_root.iter("query"):
                    self.sqlmaper[mp_root_obj.attrib['namespace']+"."+query.attrib['id']]=query.text
        except Exception,ex:
            msg=u"iSQL执行__getSQLs函数出错,[具体信息]:"+str(traceback.format_exc())+u",[数据]:\n"+str(ex)
            LogError(msg)
            raise Exception,msg

    def renderSQL(self,sqlmapid="",**kwargs):
        """
        render一个sql
        :param sqlmapid:
        :param kwargs:
        :return:
        """
        try:
            sqlstr =""
            sql_t = self.sqlmaper.get(sqlmapid,"")
            if sql_t!="":
                t = Template(sql_t, output_encoding="utf-8", input_encoding="utf-8")
                sqlstr = t.render(**kwargs)
            return sqlstr.strip()
        except Exception,ex:
            msg=u"iSQL执行renderSQL函数出错,[具体信息]:"+str(traceback.format_exc())+u",[数据]:\n"+str(ex)
            LogError(msg)
            raise Exception,msg

    def doQuery(self,conn_name="",sqlmapid="",**kwargs):
        """
        :param conn_name:配置多个连接的时候需要制定具体的连接id，参数从dataSource name="mysql_conn"中配置，配置mysql_conn，那么这
        里就执行mysql_conn
        :param sqlmapid:namespace.id，命名空间+sqlmap的id作为执行参数
        :param kwargs:输入的参数
        :return:
        """
        try:
            sqlstr = self.renderSQL(sqlmapid,**kwargs)
            sqlmsg =  "SQL>%s"%sqlstr
            #记录日志
            LogInfo(sqlmsg)
            if sqlstr!="" and self.db.has_key(conn_name):
                return self.db[conn_name].query(sqlstr)
        except Exception,ex:
            msg=u"iSQL执行renderTemplate函数出错,[具体信息]:"+str(traceback.format_exc())+u",[数据]:\n"+str(ex)
            LogError(msg)
            raise Exception,msg

if __name__=="__main__":

    recs = iSQL()
    recsss = recs.db['mysql_conn']("select id from s_sessions;select id from s_users")
    print recsss
    import MySQLDB

