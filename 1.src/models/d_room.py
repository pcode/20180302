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
opt_room = d_room()