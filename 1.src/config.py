#coding=utf-8
from mako.lookup import TemplateLookup
from evn import TP_PATH
from iLibP2.isql import iSQL
"""
此文件定义基础性组件
"""
#定义变量和数据库环境
GLOBAL_DB = iSQL()
MYSQL_CONN = "mysql_conn"
#定义模板引擎参数
GLOBAL_LOOKUP = TemplateLookup(TP_PATH, output_encoding="utf-8", input_encoding="utf-8",default_filters=['decode.utf8'],encoding_errors='replace')
#以全局变量方式在服务开启时计算所有用户的权限。可提高功能访问速度
UserPowers = {}
#全局变量方式定义系统全部功能
Funs = []