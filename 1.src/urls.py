#coding=utf8
__author__ = 'jy@cjlu.edu.cn'
Handlers = (
    "/","index.Index",
    "/login","index.Login",
    "/logout","index.Logout",
    "/index","index.Index",
    "/webmain","index.WebMain",
    "/F0011/list",      "F00.F0011.List",               #借用数据的列表
    "/F0011/ajax",      "F00.F0011.Ajax",               #
    "/F0012/list",      "F00.F0012.List",               #前台借用使用
    "/F0012/ajax",      "F00.F0012.Ajax",		        #
    "/F0013/list",      "F00.F0013.List",               #后台编辑借用数据
    "/F0013/ajax",      "F00.F0013.Ajax",		        #

)
