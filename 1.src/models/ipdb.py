#coding=utf-8
__author__ = "jy@cjlu.edu.cn"
from iLibP2.dalbase import DalBase
class ipdb(DalBase):
    """
    用于处理与数据表ipdb进行持久化操作的相关功能
    调用iLibp的基础函数
    """
    fielddefs = {
        'id'        : u'序号',
        'IPSTART'   : u'起始值',
        'IPEND'     : u'截止值',
        'REGION1'   : u'地区1',
        'REGION2'   : u'地区2',
        'IPSTART1'  : u'IP起始值',
        'IPEND1'    : u'IP截止值'
    }
    def __init__(self):
        DalBase.__init__(self,"ipdb","id",self.fielddefs)

if __name__=="__main__":
    obj=ipdb()
    print obj.GetFieldDefs()
    # recs=obj.GetRowsByDbWhere(limit=10)
    # for r in recs:
    #     print r.id