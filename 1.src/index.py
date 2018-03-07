#coding=utf-8
from iLibP2.utils import toJson

__author__ = 'pcode@qq.com'
from iLibP2.baseView import BaseView
from models.s_userpower import *
from web.utils import storage
class Index(BaseView):
    """
    入口页面
    """
    def GET(self):
        web.header("Content-Type", "text/html; charset=UTF-8")
        i = web.input()
        return self.display("T/index.html", i=i)
class Logout:
    def GET(self):
        clearLogin()
        web.seeother('/login')

class Login(BaseView):
    def GET(self):
        web.header("Content-Type", "text/html; charset=UTF-8")
        i=web.input()
        return self.display("T/login.html",i=i)
    def POST(self):
        web.header("Content-Type", "application/json; charset=UTF-8")
        i=web.input(act='list',usern='',pwd='')
        if i.act and i.usern and i.pwd :
            opt_user=s_user()
            login_result = storage()
            if i.act=="login":
                userobj=opt_user.trylogin(i.usern,i.pwd)
                if userobj:
                    setLogin(userobj)
                    LogOpt("[%s]%s请求登录,获授权;%s"%(userobj.username,userobj.truename,GetUserIPRegion()))
                    login_result.result = "OK"
                else:
                    clearLogin()
                    LogOpt("请求使用[%s]账号使用[%s]密码登录系统,被拒绝;%s"%(i.usern,i.pwd,GetUserIPRegion()))
            else:
                clearLogin()
                LogOpt("外部程序请求登录系统,被拒绝;%s"%(GetUserIPRegion()))
            return toJson(login_result)
class WebMain(BaseView):
    @s_checklogin()
    def GET(self):
        web.header("Content-Type", "text/html; charset=UTF-8")
        i=web.input()
        i.cu = get_currentuser()
        return self.display("T/main.html",i=i)
