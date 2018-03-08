#coding=utf-8
from iLibP2.utils import GETMD5
__author__ = 'jy@cjlu.edu.cn'
import traceback
from iLibP2.dalbase import DalBase
from iLibP2.loger import LogInfo, LogError, LogOpt

class d_room(DalBase):
    """
    用于处理会议室借用数据表
    """
    fields ={
        'id'        : u'序号',
        'roomno'    : u'用户名',
        'the_date'  : u'日期',
        'time1'     : u'开始时间',
        'time2'     : u'结束时间',
        'applyuser' : u'申请人',
        'phoneno'   : u'电话号码',
        'the_memo'  : u'用途描述',
        'applytime' : u'申请时间'
    }
    def __init__(self):
        DalBase.__init__(self,"d_room","id",self.fields)
    def getInfos(self,roomno,days):
        """
        获取未来几天的借用情况
        :param roomno:
        :param days:
        :return:
        """
        result=[]
        try:
            result = self.GetRowsByDbWhere(
                                            where= " the_date BETWEEN CURDATE() and ADDDATE(CURDATE(),INTERVAL $days DAY) and roomno=$roomno",
                                            vars={"days":days,"roomno":roomno}
                                           )
            result=result.list()
        except:
            pass
        return result

    def getPassedInfos(self,roomno,days):
        """
        获取近几天的借用情况
        :param roomno:
        :param days:
        :return:
        """
        pass
opt_room = d_room()
if __name__ == '__main__':
    recs = opt_room.getInfos('T400',3)
    print recs