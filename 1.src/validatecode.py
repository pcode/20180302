#coding=utf-8
__author__ = 'jy@cjlu.edu.cn'
#=======================================================================================================================
#编号:[F0013]
#名称:[用来显示验证码]
#功能:[主要用于编辑和修改系统内置的参数信息]
#=======================================================================================================================
import web
from SysCommon.vCode import create_validate_code

class List:
    def __init__(self):
        pass
    def GET(self):
        web.header('Content-Type', 'image/jpeg; charset=utf-8')
        img = create_validate_code()
        web.setcookie("vcode",img[1],8*3600)
        return img[0]