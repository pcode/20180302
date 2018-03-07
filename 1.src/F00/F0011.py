#coding=utf-8
import web
from iLibP2.utils import doexport
from models.d_room import opt_room
from iLibP2.utils import toJson, JsonResult, CopyData_INC
from iLibP2.baseView import BaseView
from web.utils import storage
opt_obj=opt_room
__author__ = 'pcode@qq.com'
########################################################################################################################
#系统功能管理
#功能编号：F0011
########################################################################################################################
def Filter(i):
    wherestr = " 1=1 "
    if i.get('roomno', '') != '':
        i.roomno += "%"
        wherestr += " and roomno like $roomno"
    # 补充其他条件
    i.pageindex = int(i.get("pageindex", 1))
    i.pagesize = int(i.get("pagesize", 50))
    rows, i.total, i.pagecount = opt_obj.GetPagedRowsByDbWhere(pageindex=i.pageindex - 1,
                                                               pagesize=i.pagesize,
                                                               where=wherestr,
                                                               order="id desc",
                                                               vars=i)
    rows = rows.list()
    #返回数据条目数量
    i.recordsTotal =i.total
    #总计条目数量
    i.recordsFiltered=len(rows)
    i.data =rows
    return i

def Filter1(i):
    """
    过滤数据使用
    :param i:
    :return:
    """
    wherestr = " 1=1 "
    if i.get('roomno','')!='':
        i.funno +="%"
        wherestr += " and roomno like $funno"
    #补充其他条件
    i.pageindex = int(i.get("pageindex", 1))
    i.pagesize = int(i.get("pagesize", 50))
    rows, i.total, i.pagecount = opt_obj.GetPagedRowsByDbWhere(pageindex=i.pageindex-1,pagesize=i.pagesize,where=wherestr ,order="id desc",vars = i)
    i.rows=rows.list()
    return i
class Ajax(BaseView):
    def GET(self):
        return self.POST()
    def POST(self):
        """
        ajax交互
        """
        web.header("Content-Type", "application/json; charset=UTF-8")
        i = web.input(cmd="ajax")
        if i.cmd=="ajax":
            i = Filter(i)
            return toJson(i)

        if i.cmd=="del":
            opt_obj.DelRowsByDbWhere(where="id=$id",vars={'id':i.id})
            return JsonResult("OK")
class List(BaseView):
    def GET(self):
        """
        显示数据列表
        :return:
        """
        web.header("Content-Type", "text/html; charset=UTF-8")
        i = web.input()
        return self.display("F00/T/F0011.html",i=i)