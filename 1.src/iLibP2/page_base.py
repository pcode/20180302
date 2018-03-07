#coding=utf-8
import traceback
from iLibP2.loger import LogError

__author__ = 'pcode@qq.com'
from config import GLOBAL_LOOKUP as T
import json
from web.utils import storage
from evn import TP_PATH
class PageBase:

    def display(self,templatefile,**kwargs):
        t = T.get_template(templatefile)
        return t.render(**kwargs)
    def Loads(self,filepath):
        """
        读取文本文件并加载到json中作为数据源
        :param filepath:
        :return:
        """
        try:
            f = open(TP_PATH+"/"+filepath)
            strcontent = f.read()
            f.close()
            result = json.loads(strcontent)
            return result
        except Exception,ex:
            msg=u"page_base执行Loads函数出错,[具体信息]:"+str(traceback.format_exc())+u",\n[参数]:\n"+filepath+u"\n[数据]:\n"+str(ex)
            LogError(msg)
            return {}