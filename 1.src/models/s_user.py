#coding=utf-8
from iLibP2.utils import GETMD5

__author__ = 'jy@cjlu.edu.cn'
import traceback
from iLibP2.dalbase import DalBase
from iLibP2.loger import LogInfo, LogError, LogOpt

class s_user(DalBase):
    """
    用于处理s_user表数据
    s_user是系统权限管理的核心表之一
    用于存放系统用户
    """
    fields ={
        'id':u'序号',
        'username':u'用户名',
        'userpwd':u'密码',
        'truename':u'姓名',
        'userstatus':u'状态',
        'userpower':u'权限级别',
        'usertype':u'用户类型',
        'lastlogintime':u'最后登录时间'
    }
    def __init__(self):
        DalBase.__init__(self,"s_user","id",self.fields)

    def GetUserByUserName(self,un):
        """
        根据用户名获取用户对象
        """
        return self.GetRowByDbWhere(where="username=$un",vars={'un':un})
    def GetUsersByStatus(self,status):
        """
        根据用户的状态来获取用户数据
        :param status: 1,0分别代表启用和停用用户
        :return:用户列表的头
        """
        return self.GetRowsByDbWhere(where='userstatus=$s',vars={'s':status})

    def GetUserById(self,user_id):
        """
        根据用户id获取用户对象
        """
        return self.GetRowByDbWhere(where="id=$id",vars={'id':user_id})
    def trylogin(self,username,userpwd):
        """
        尝试登陆
        """
        rec=self.GetRowByDbWhere(where="username=$un",vars={"un":username})
        if rec:
            if rec.userpwd==GETMD5(userpwd):
                return rec
    def dostop(self,id):
        """
        停用用户
        @param id:
        @return:
        """
        rec=self.GetRowById(id)
        try:
            if rec:
                self.UpdateValues(where="id=$id",vars={'id':id},userstatus='off')
                LogInfo("系统用户ID%s被成功停用"%id)
                return True
        except Exception,ex:
            print ex
            return False
    def dostart(self,id):
        """
        启用用户
        @param id:
        @return:
        """
        rec=self.GetRowById(id)
        try:
            if rec:
                self.UpdateValues(where="id=$id",vars={'id':id},userstatus='on')
                LogInfo("系统用户ID%s被成功启用"%id)
                return True
        except:
            return False
    def GetAllAdminNo(self):
        r = []
        list = self.GetRowsByDbWhere(where=" usertype = '管理员'")
        for u in list:
            r.append(u.id)
        return r
opt_s_user = s_user()
if __name__=="__main__":
    opt_obj =s_user()
    recs = opt_obj.GetRowsByDbWhere()
    for rec in recs:
        print rec
    print GETMD5('123456')
    # recs = opt_obj.GetAllAdminNo()
    # opt_obj.dostop(85)
    # opt_obj.dostart(85)
    # for rec in recs:
    #     print rec