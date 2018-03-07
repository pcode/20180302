#coding=utf-8
from iLibP2.utils import GETMD5

__author__ = 'pcode@qq.com'
from config import GLOBAL_DB as db
from config import MYSQL_CONN
from iLibP2.dalbase import DalBase
class s_users(DalBase):
    fields = {
                    u'应用名':'appname',
                    u'用户名':'username',
                    u'密码':'pw',
                    u'最后登录时间':'lastlogintime',
                }
    def __init__(self):
        DalBase.__init__(self,'s_users','id',self.fields)

    #额外函数请自行定义
    def DataFilter(self,i):
        """
        用于过滤数据，给出最终的数据列表，每个元素都是一个storage
        返回的数据放置在i的recs里
        """
        #补充其他查询条件

        i.id  = i.get('id','')
        i.appname  = i.get('appname','')
        i.username  = i.get('username','')
        i.pw  = i.get('pw','')
        i.lastlogintime  = i.get('lastlogintime','')
        #初始化结果
        i.recs      = []
        strwhere    = " id>0 "
        #序号查询
        if i.get('id',None):
            strwhere+=" and id like '%"+i.id+"%'"
        #用户名查询
        if i.get('username',None):
            strwhere+=" and username like '%"+i.username+"%'"

        i.pageindex = int(i.get("pageindex", 1))
        i.pagesize  = int(i.get("pagesize", 15))
        recs, i.recordercount, i.pagecount = self.GetPagedRowsByDbWhere(pageindex=i.pageindex-1,pagesize=i.pagesize,where=strwhere ,order=" id asc")
        i.recs      = recs.list()
        return i
    def getInfo(self,appname,username):
        """
        根据用户的参数来获取用户信息
        :return:
        """
        return self.GetRowByDbWhere(where ="appname=appname and username=username" ,vars={'appname':appname,'username':username})
    def check_login(self,appname,username,pw):
        """
        检测接口应用的登陆权限。
        目前还没有限制接口权限的范围
        未来将增加针对appname和username的接口权限的限制
        :param appname:
        :param username:
        :param pw:
        :return:
        """
        user_obj = self.getInfo(appname,username)
        if user_obj and user_obj.pw ==pw:  #为什么需要再GETMD5?user_obj.pw ==GETMD5(pw),应该直接user_obj.pw ==pw
            return True,user_obj
        else:
            return False,None
    def getCurrentUser(self):
        """
        通过session获取当前登录的用户，这个函数是给web调用时候使用的。
        :return:
        """
        pass
opt_user = s_users()
if __name__ == '__main__':
    recs = opt_user.GetRowsByDbWhere()
    for r in recs:
        print r