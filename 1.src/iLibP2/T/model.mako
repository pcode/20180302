<%text>#encoding=utf-8</%text>
__author__ = 'jy@cjlu.edu.cn'
# ${functionmemo}
from iLibP2.dalbase import DalBase
${tablename}_fields = {
%for r in recs:
    '${r.colname}':u'${r.colcomment}',
%endfor
}

class ${tablename}(DalBase):
    def __init__(self):
        DalBase.__init__(self,'${tablename}','id',${tablename}_fields)
    #额外函数请自行定义

if __name__ == '__main__':
    opt_obj = ${tablename}()
    #print opt_obj.GetFieldDefs()
    recs,r1,r2 = opt_obj.GetPagedRowsByDbWhere(0,20)
    for rec in recs:
        print rec