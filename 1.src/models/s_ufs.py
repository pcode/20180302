#coding=utf-8
import traceback
from iLibP2.loger import LogError

__author__ = 'jy@cjlu.edu.cn'
from iLibP2.dalbase import DalBase
from s_user import s_user
from s_fun import s_fun
from web.utils import storage
"""
用于处理s_ufs表数据
s_ufs是系统权限管理的核心表之一
用于存放用户权限数据
"""
class s_ufs(DalBase):
    fields = {
            'id'        : u'序号',
            'username'  : u'用户名',
            'funno'     : u'功能编号'
        }
    def __init__(self):
        DalBase.__init__(self,"s_ufs",self.fields)

    #获取某用户的功能权限，如果用户的级别是９级则返回全部功能
    def GetUserFunnos(self,username):
        """
        获取用户的所有授权功能
        如果用户权级是9级，则返回所有功能
        否则按用户ID号进行查询授权
        """
        result = []
        try:
            opt_user    = s_user()
            funobj      = s_fun()
            #再次验证用户身份
            userobj  = opt_user.GetRowByDbWhere(where = 'username = $username',vars={'username':username})
            if userobj:
                #系统管理员返回全部功能可用
                if userobj.userpower>=9:
                    result = funobj.GetRowsByDbWhere(what = 'funno').list()
                #非系统管理员返回定义可用功能
                else:
                    result = self.GetRowsByDbWhere( what = 'funno',where="username=$username",vars={'username':userobj.username}).list()
            return [r.funno for r in result]
        except Exception,ex:
            msg=u"s_ufs执行GetUserFunnos函数出错,[具体信息]:%s,\n[参数]:\n %s \n[数据]:\n%s"%(str(traceback.format_exc()),str(username),str(ex))
            LogError(msg)
        return result

    #检查用户权限
    def CheckUserPower(self,userobj,fun_no):
        """
        检查用户功能授权
        仅传入用户对象，然后根据授权表进行检查
        """
        result=False
        try:
            #9级用户直接认为可以使用此功能
            if userobj.userpower>=9:
                result=True
            #其他权限级别用户需要判断
            else:
                result=self.CheckHave(where="username=$username and funno=$funno",vars={'username':userobj.username,'funno':fun_no})
        except Exception,ex:
            msg=u"s_ufs执行CheckUserPower函数出错,[具体信息]:%s,\n[参数]:\n %s \n %s \n[数据]:\n%s"%(str(traceback.format_exc()),str(userobj),fun_no,str(ex))
            LogError(msg)
        return result

    def GetUserFunsStatus(self,funs,username):
        """
        获取用户的所有功能的可用状态。
        返回一个storage，属性由F_功能编号=True或False的对象
        在使用时直接判断obj.F_功能编号==True即可判断是否具有某一权限
        """
        user_funnos     = self.GetUserFunnos(username)
        result          = storage()
        for f in funs:
            result[f] = user_funnos.__contains__(f)
        return result


    def getFunsStatus(self):
        """
        获取所有用户的权限状态
        刷新系统全局的权限信息
        全局funs是系统功能的列表
        全局UserPowers结构
        {
        "admin":{
            "F00":True,"F0011":True,"F0012":False....
            },
        "user":{
            "F00":True,"F0011":True,"F0012":False....
            }
            ...
        }
        @return:一个storage列表，其中包括所有用户的权限状态
        """
        #获取全部功能
        opt_fun     = s_fun()
        recs        = opt_fun.GetRowsByDbWhere()
        funs        = [r.funno for r in recs]
        #获取全部用户
        opt_user    = s_user()
        opt_ufs     = s_ufs()
        user_rows   = opt_user.GetRowsByDbWhere()
        #计算用户的功能可用性
        result      = storage()
        for row in user_rows:
            result[row.username] = opt_ufs.GetUserFunsStatus(funs,row.username)
        return result

if __name__=="__main__":
    obj=s_ufs()
    r = obj.getFunsStatus()
    print r