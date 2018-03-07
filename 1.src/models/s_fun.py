#coding=utf-8
__author__ = "pcode@qq.com"
import config
from iLibP2.dalbase import DalBase
class s_fun(DalBase):
    """
    用于处理与数据表s_fun进行持久化操作的相关功能
    调用iLibp的基础函数
    """
    fields = {
        'id'            : u'序号',
        'funno'         : u'功能编号',
        'funname'       : u'功能名称',
        'funcatalog'    : u'功能分类',
        'funclass'      : u'功能类别'
    }
    def __init__(self):
        DalBase.__init__(self,"s_fun","id",self.fields)

    def GetFunsByFunHead(self,funnohead):
        """
        根据功能编号的头部来获取功能列表
        """
        return self.GetRowsByDbWhere(where="funno like '$funnohead%' order by funno asc",vars={'funnohead':funnohead})

    def GetFunByFunno(self,funno):
        """
        根据功能编号获取功能
        """
        return self.GetRowByDbWhere(where="funno=$f",vars={"f":funno})


obj=s_fun()

if __name__=="__main__":
    print obj.GetRowsByDbWhere().list()
    # print obj.GetFieldDefs()
    # recs=obj.GetRowsByDbWhere()
    # for r in recs:
    #     print r.id

