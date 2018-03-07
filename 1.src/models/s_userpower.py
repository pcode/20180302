# coding=utf-8

from models.JyIpTools import GetUserIPRegion
from models.s_ufs import s_ufs
from models.s_user import *
from iLibP2.loger import *
import web


def setLogin(userData=None):
    """
        设置登陆信息
        :param userData:
        :return:
        """

    if userData is None:
        web.setcookie("login", False)
    else:
        web.setcookie("login", True)
        web.setcookie("userid", userData['id'])
        web.setcookie("username", userData['username'])
    return userData


def clearLogin():
    """
    #注销
    """
    web.cookies().clear()


def checkLogin():
    """
    是否已经登陆
    :return:
    """
    l=web.cookies().get("login","False")
    return  l=="True"


def get_currentuser():
    result = None
    try:
        if checkLogin():
            userid = web.cookies().get("userid")
            cuser = opt_s_user.GetUserById(userid)
            result = cuser
    except:
        result = None
    return result

def get_userpower(userobj):
    """
    根据用户获取用户权限
    :param userobj:
    :return:
    """
    if userobj:
        optobj = s_ufs()
        power_status = optobj.GetUserFunsStatus(userobj)
        return power_status
    else:
        return None

def check_userpower(funno):
    """
    检查当前登录的用是否具有使用funno的权限
    """
    user_obj = get_currentuser()
    if user_obj:
        f = False
        # 检查用户权限
        from config import UserPowers
        if UserPowers.has_key(user_obj.username) and UserPowers[user_obj.username].has_key(funno) and \
                UserPowers[user_obj.username][funno]:
            f = True
        if f:
            LogOpt("[%s]%s请求操作[%s]功能,获授权;%s" % (user_obj.username, user_obj.truename, funno, GetUserIPRegion()))
        else:
            LogOpt("[%s]%s请求操作[%s]功能,被拒绝;%s" % (user_obj.username, user_obj.truename, funno, GetUserIPRegion()))
        return f
    else:
        LogOpt("未登陆用户]请求[%s]功能，被拒绝;%s" % (funno, GetUserIPRegion()))
        return False

def s_checklogin():
    def methodwrapper(method):
        """
        封装函数，在调用前检查权限
        """
        def newmethod(*args, **kw):
            tr = checkLogin()
            if tr:
                result = method(*args, **kw)
                return result
            else:
                """
                以后改成模板显示
                """
                web.header("Content-Type", "text/html; charset=UTF-8")
                return u"请<a href='/login'>登录</a>后使用此功能"

        return newmethod

    return methodwrapper


def s_checkpower(funno):
    """
    权限检查
    调用示例:
    @checkpower("F1011")
    def GET(self):
        XXX
    """
    def methodwrapper(method):
        """
        封装函数，在调用前检查权限
        """

        def newmethod(*args, **kw):
            tr = check_userpower(funno)
            if tr:
                result = method(*args, **kw)
                return result
            else:
                return u"未获授权使用此功能"

        return newmethod

    return methodwrapper
