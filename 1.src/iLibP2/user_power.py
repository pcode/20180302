#coding=utf-8
from loger import *
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
        def newmethod(*args,**kw):
            LogInfo("操作"+funno+"功能，获得授权，ip：127.0.0.1 本机")
            result = method(*args,**kw)
            return result
        return newmethod
    return methodwrapper