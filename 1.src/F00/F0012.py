#coding=utf-8
import datetime
import web
from iLibP2.utils import doexport
from models.d_room import opt_room
from iLibP2.utils import toJson, JsonResult, CopyData_INC
from iLibP2.baseView import BaseView
from web.utils import storage
opt_obj=opt_room
__author__ = 'pcode@qq.com'
########################################################################################################################
#会议室预约
#功能编号：F0012
########################################################################################################################
class Ajax:
    def POST(self):
        """
        ajax交互
        """
        web.header("Content-Type", "application/json; charset=UTF-8")
        i = web.input(cmd="ajax")
        if i.cmd == "add":
            i.time1 = i.starthour+":"+i.startmin
            i.time2 = i.endhour +":"+i.endmin
            i.applytime = datetime.datetime.now()
            opt_obj.Save(i)
        return JsonResult("OK")
class List(BaseView):
    def GET(self):
        """
        显示数据列表
        :return:
        """
        web.header("Content-Type", "text/html; charset=UTF-8")
        i = web.input(id="")
        if len(i.id)>0:
            row = opt_obj.GetRowById(i.id)
            i=row
            i.cmd           = "edit"
            i.starthour     = i.time1.split(":")[0]
            i.startmin      = i.time1.split(":")[1]
            i.endhour       = i.time2.split(":")[0]
            i.endmin        = i.time2.split(":")[1]
        return self.display("F00/T/F0012.html",i=i)