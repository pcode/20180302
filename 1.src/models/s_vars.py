#coding=utf-8
from web.utils import storage
from iLibP2.dalbase import DalBase
__author__ = 'jy@cjlu.edu.cn'

class s_vars(DalBase):
    """
    用于处理与数据表s_vars进行持久化操作的相关功能
    调用iLibp的基础函数
    """
    fields = {
        'id':u'序号',
        'varname':u'变量名称',
        'varcnname':u'变量中文名称',
        'varvalue':u'变量值',
        'varclass':u'变量类别',
        'varmemo':u'备注',
        'lastmodifytime':u'最后更新时间',
        'lastmodifyuser':u'最后更新者'
    }
    def __init__(self):
        DalBase.__init__(self,"s_vars","id",self.fields)
    def SaveVarValue(self,varname,varvalue,varclass):
        """
        保存变量值，如果变量已经存在则更新，否则返回错误
        """
        try:
            varobj=self.GetRowByDbWhere(where="varname=$v and varclass=$c",vars={'v':varname,'c':varclass})
            if varobj:
                varobj.varvalue=varvalue
                self.Save(varobj)
            else:
                varobj          = storage()
                varobj.id       = 0
                varobj.varname  = varname
                varobj.varclass = varclass
                varobj.varvalue = varvalue
                self.Save(varobj)
            return True
        except :
            return False
    def GetVarsByClass(self,varclass):
        return self.GetRowsByDbWhere(where="varclass=$v",vars={"v":varclass})
    def GetVarByVarName(self,varname,varclass,defaultvalue):
        row = self.GetRowByDbWhere(where="varname=$v and varclass=$c",vars={"v":varname,"c":varclass})
        if row:
            return row
        else:
            return {'varname':varname,'varclass':varclass,'varvalue':defaultvalue}

S_vars=s_vars()
if __name__=="__main__":
    obj=s_vars()
    print obj.GetFieldDefs()
    # recs=obj.GetRowsByDbWhere()
    # for r in recs:
    #     print r.id
    #
    # print obj.GetVarByVarName('2016_GY', 's', 0.4989)
