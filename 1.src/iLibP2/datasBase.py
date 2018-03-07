# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json

import config
from iLibP2.utils import ToJson
import os
FP = os.getcwd()
FP = "D:/projecting/yl_ad2/1.2SRC"
class DatasBase():
    __the_key = ""
    __the_data = []
    @property
    def Datas(self):
        return self.__the_data
    def getValue(self,the_key):
        return config.db.get(the_key)
    def setValue(self,the_key,the_value):
        return config.db.set(the_key,the_value)
    def __init__(self,the_key="",the_data = []):
        self.__the_key = the_key
        if len(the_data)>0:
            self.__the_data = the_data
        else:
            self.__the_data = self.Load()
    def Save(self,data=[]):
        """
        保存数据
        :param data:
        :return:
        """
        if len(data)>0:
            self.setValue(self.__the_key,ToJson(data))
            self.__the_data= data
        else:
            self.setValue(self.__the_key,ToJson(self.__the_data))
    def Load(self):
        """
        加载数据
        :return:
        """
        jsonstr = self.getValue(self.__the_key)
        if jsonstr:
            self.__the_data = json.loads(jsonstr)
            return self.__the_data
        else:
            self.__the_data =[]
            return self.__the_data

    def LoadFile(self,fn=""):
        """
        从文件加载
        :param fn:文件名不指定的话从默认地址加载
        :return:
        """
        if fn !="":
            f = open(FP + fn, "r")
        else:
            f = open(FP + "/" + self.__the_key + ".json", "r")
        jsonstr = f.read()
        self.__the_data = json.loads(jsonstr)
        return self.__the_data
    def Save2File(self,the_data=[],fn=""):
        """
        保存到文件去,如果指定数据则写指定的数据否则写内部数据，如果指定文件名则写指定的文件名，否则按key.json来写数据
        :param the_data:
        :param fn:
        :return:
        """
        if fn=="":
            f = open(FP + "/"+self.__the_key+".json", "w")
        else:
            f=open(FP+fn,"w")
        if len(the_data)>0:
            self.__the_data = the_data
        f.write(ToJson(self.__the_data, ifIndent=True))
        f.close()
        return self.__the_data