#coding=utf-8
__author__ = 'pcode@qq.com'
from urls import Handlers
import web
if __name__ == "__main__":
    app = web.application(Handlers, globals())
    app.run()