<%text>#coding=utf-8
__author__ = 'pcode@qq.com'
from iLibP2.utils import doexport
import web
from iLibP2.utils import toJson, JsonResult, CopyData_INC
from iLibP2.baseView import BaseView
from models.</%text>${tablename} import ${tablename}
<%text>from web.utils import storage
########################################################################################################################
#</%text>${functionmemo}<%text>
#功能编号：</%text>${fn}<%text>
########################################################################################################################
#全局操作实例
</%text>
opt_obj=${tablename}()
def Filter(i):
    """
    过滤数据使用
    :param i:
    :return:
    """
    wherestr = " 1=1 "
    %for rec in recs:
    #查询字段${rec.colname}-${rec.colcomment}
    if i.get('${rec.colname}','')!='':
        wherestr += " and ${rec.colname}<%text> = $</%text>${rec.colname}"
    %endfor
    #补充其他条件
    i.pageindex = int(i.get("pageindex", 1))
    i.pagesize = int(i.get("pagesize", 50))
    rows, i.total, i.pagecount = opt_obj.GetPagedRowsByDbWhere(pageindex=i.pageindex-1,pagesize=i.pagesize,where=wherestr ,order="id desc",vars = i)
    i.rows=rows.list()
    return i
class Ajax(BaseView):
    def POST(self):
        """
        ajax交互
        """
        web.header("Content-Type", "application/json; charset=UTF-8")
        i = web.input(cmd="ajax")
        if i.cmd=="ajax":
            result = storage()
            i = Filter(i)
            result=CopyData_INC(result,i,['total','rows'])
            return toJson(result)
        if i.cmd =="add":
            newobj = storage()
            newobj.id = 0
            newobj=CopyData_INC(newobj,i,${colnames})
            opt_obj.Save(newobj)
            return JsonResult("OK")
        if i.cmd=="edit":
            old_obj = opt_obj.GetRowById(i.the_id)
            old_obj = CopyData_INC(old_obj,i,${colnames})
            opt_obj.Save(old_obj)
            return JsonResult("OK")
        if i.cmd=="del":
            opt_obj.DelRowsByDbWhere(where="id=$id",vars={'id':i.id})
            return JsonResult("OK")
        if i.cmd=="export":
            web.header("Content-Type", "application/json; charset=UTF-8")
            i=web.input(pagesize=999999)
            i= Filter(i)
            return doexport(opt_obj.cnfields,opt_obj.fields,i.recs)

class List(BaseView):
    def GET(self):
        """
        显示数据列表
        :return:
        """
        web.header("Content-Type", "text/html; charset=UTF-8")
        i = web.input()
        return self.display("${mn}/T/${fn}_0.html",i=i)
class Import(BaseView):
    def POST(self):
        """
        导入
        :return:
        """
        t = opt_obj.Transaction()
        try:
            # 这里需要增加清理数据的操作
            opt_obj.DelRowsByDbWhere()
            from iLibP2.ixls import iXls
            opt_xls = iXls()
            nfilename = opt_xls.uploadFile()
            result = opt_xls.parseXls(opt_obj.fielddefs,nfilename)
            for row in result.rows:
                row.id = 0
                opt_obj.Save(row)
            opt_obj.Commit(t)
            web.seeother("/${fn}/list")
        except:
            opt_obj.RollBack(t)
            web.seeother("/${fn}/list")
        pass

if __name__ == '__main__':
    pass
