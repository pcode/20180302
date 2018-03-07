#coding=utf-8
__author__ = 'jy@cjlu.edu.cn'
from iLibP2.dalbase import DalBase
"""
用于处理v_ufs表数据
v_ufs是系统权限管理的核心表之一
用于联合各表显示用户权限
"""
class dal_v_ufs(DalBase):
    def __init__(self):
        DalBase.__init__(self,"v_ufs","id",[])
        
class bll_v_ufs(dal_v_ufs):
    def __init__(self):
        dal_v_ufs.__init__(self)