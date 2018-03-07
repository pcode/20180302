#coding=utf-8
from random import random, randint
from decimal import Decimal
from web.utils import storage, dictreverse

import os,web
import time
import datetime
import json
import xlrd
from evn import TP_PATH
from iLibP2.ixls import iXls


def doexport(cnfields,fields,recs):
    """
    cnfields
    :param i:
    :param opt_obj:
    :param filterfun:
    :return:
    """
    def gcPath():
        import datetime,os
        """
        创建上传目录，按月度处理上传的文件内容。避免一个目录的文件太多难以管理
        如果以后使用分布式来做，可以改造这个函数来处理
        :return:目录名
        """
        now_month = datetime.datetime.now().strftime("%Y%m")
        tpath="/static/uploads/"+now_month
        if not os.path.exists(TP_PATH+tpath):
            os.mkdir(TP_PATH+tpath)
        return tpath
    excelobj=iXls()
    wb,ws=excelobj.openExistExcel(TP_PATH+"/static/blank.xls")
    row = 0
    col = 0
    #写头部数据
    for f in  cnfields:
        ws.write(row,col,f)
        col+=1
    row +=1
    #更改页面大小防止分页影响
    for d in recs:
        col = 0
        for f in fields:
            ws.write(row,col,d[f])
            col +=1
        row+=1
        #3.输出excel
    nfilename = gcPath()+"/"+TimeStr()+".xls"
    wb.save(TP_PATH+nfilename)
    return toJson({'result':"OK","filename":nfilename})

def parseXls(fieldrelation,excelfilepath):
    """
    解析xls，如果解析到字段的中文英文定义，则按对照来做，否则按列的名称来尝试，给定的字段名一定是中：英这样。
    :param fieldrelation:
    字段对照关系，中文对照数据字段
    类似
    {
                    u'来源表id':'src_id',
                    u'姓名':'truename',
                    ....
    }
    :param excelfilepath: excel文件是已经上传到系统的文件绝对路径
    :return:
    """
    #结果对象
    result = storage()
    #数据集合
    data = []
    #先读取字段的对照关系，如果没有给定对照关系就默认按读取到的结果写入；
    bk = xlrd.open_workbook(excelfilepath)
    # 默认取得第一个sheet
    sh = bk.sheet_by_index(0)
    # 获取默认的字段对照关系,如果没有就去使用默认的字段对照关系
    the_fields_relation = fieldrelation
    #读取行数
    nrows = sh.nrows
    # 获取到列数
    ncols = sh.ncols
    # 列信息的采集
    cols_infos = []
    # 解析中文字段
    fr1 = the_fields_relation
    fr2 = dictreverse(the_fields_relation)
    #读取列
    for c in range(ncols):
        #从第一行第一列开始取数据
        col_title = sh.cell_value(0, c)
        field_name1 = fr1.get(col_title, "")
        field_name2 = fr2.get(col_title,"")
        # 如果能获取到字段值就进行匹配
        if field_name1 != "":
            cols_infos.append((col_title, field_name1, c))
        if field_name2 != "":
            cols_infos.append((col_title,col_title,c))
    #读取行
    for row_index in range(1, nrows):
        row_data = storage()
        for col_title, field_name, col_index in cols_infos:
            row_data[field_name] = sh.cell_value(row_index, col_index)
        data.append(row_data)

    #封装返回结果
    result.fields = cols_infos
    result.data = data
    result.row_count = nrows - 1
    result.col_count = ncols
    return result
class MyEncoder(json.JSONEncoder):
      def default(self, obj):
          # if isinstance(obj, datetime.datetime):
          #     return int(mktime(obj.timetuple()))
          if isinstance(obj, datetime):
              return obj.strftime('%Y-%m-%d %H:%M:%S')
          elif isinstance(obj, date):
              return obj.strftime('%Y-%m-%d')
          elif isinstance(obj,Decimal):
              return str(obj)
          else:
              return json.JSONEncoder.default(self, obj)
def GETMD5(src):
    """
    用于生成md5串
    """
    import hashlib
    return hashlib.md5(src).hexdigest()
def encode_zf(v):
    '''
    正方密码的加密算法
    :param v:
    :param k:
    :return:
    '''
    k = 'Encrypt01'
    newStr =''
    pos=0
    for i in range(0,len(v)):
        strChar = v[i]
        keyChar = k[pos]
        s_v = ord(strChar)
        k_v = ord(keyChar)
        if ((s_v^k_v)<32)|((s_v^k_v)>126) | (s_v<0) | (s_v>255):
            newStr = newStr+strChar
        else:
            newStr = newStr+chr(s_v^k_v)
        if pos == len(k)-1: pos=0
        else:
            pos += 1
    if len(newStr)%2==0 :
        side1 = (newStr[0:int(len(newStr)/2)])[::-1]    #左边一半
        side2 = (newStr[::-1])[0:int(len(newStr)/2)]    #右边一半
        newStr = side1+side2
    return newStr

def ToJson(dictobj):
    return json.dumps(dictobj,ensure_ascii=False,indent=2,cls=MyEncoder)

def toMD5(src):
    """
    用于生成md5串
    """
    import hashlib
    return hashlib.md5(src).hexdigest()

def webPackage(errcode,errmsg,data):
    """
    将数据打包准备发回给客户端
    :param errcode: 错误编号
    :param errmsg: 错误信息
    :param data: 数据
    :return:
    """
    try:
        r = {
            'errcode':errcode,
            'errmsg':errmsg,
            'data':data
        }
        return ToJson(r)
    except Exception,ex:
        pass
def ArrayFind(array,value):
    """
    在数组中查找值
    """
    i=0
    fl=False
    for a in array:
        i+=1
        if a==value:
            fl=True
            break
    if fl:
        return i
    else:
        return -1
def InitStorage(storage,incfields=[],defaultvalue=""):
    """
    用于初始化storage，补充属性值
    @param storage:需要初始化的storage
    @param incfields:涉及的字段
    @param defaultvalue:默认值
    @return:storage,初始化好的对象
    """
    if incfields:
        for field in incfields:
            if storage.get(field,defaultvalue)==defaultvalue or storage[field]==None:   #不污染原有值
                storage[field]=defaultvalue
    else:
        for field in storage.keys:
            if storage.get(field,defaultvalue)==defaultvalue or storage[field]==None:   #不污染原有值
                storage[field]=defaultvalue
    #初始化好的对象
    return storage
def InitStorageBlank(storage,incfields=[]):
    """
    用于初始化storage或dic,将incfields包含的字段赋值，如果有值则传，无值则初始化为""
    给定字段则按给定字段
    """
    if incfields:
        for field in incfields:
            if storage.get(field,None)==None:   #不污染原有值
                storage[field]=""
    else:
        for field in storage.keys():
            if storage.get(field,None)==None:   #不污染原有值
                storage[field]=""
    return storage
def CopyData_INC(storage1,storage2,incfields=[],default=None):
    """合并属性，将storage2由incfields指定的字段合并入storage1中。
    如属性在2中为None，则不指定
    """
    for field in incfields:
        if storage2.get(field,None) is None:
            storage1[field]=default
        else:
            storage1[field]=storage2[field]
    return storage1
def CopyData_EX(storage1,storage2,exfields=["id"]):
    """
    合并属性,如果storage1、2共有的属性按2更新1的属性值，如2有1无的，不作处理
    1有2无的也不作处理
    exfiles=["id","no"]不想受此次复制污染的字段
    """
    a=[]
    if not storage1:                    #如果给的是一个None空，则先初始化一下。
        storage1=storage()
    for k in storage2.keys():
        if ArrayFind(exfields,k)==-1:
            storage1[k]=storage2[k]
    return storage1
def CopyData(storage1,storage2):
    """
    合并属性,如果storage1、2共有的属性按2更新1的属性值，如2有1无的，增加
    1有2无的也不作处理
    """
    if not storage1:                    #如果给的是一个None空，则先初始化一下。
        storage1=storage()
    for k in storage2.keys():
        storage1[k]=storage2[k]
    return storage1
def CopyData_Match(storage1,storage2,fields1=[],fields2=[]):
    """
    按配置字段将storage2的数据赋值给storage1
    @param fields1:storage1需要赋值的字段
    @param fields2:storage2提供数据的字段
    @param storage1:需要被赋值的storage
    @param storage2:提供数据的storage
    @reaturn:storage1
    """
    if len(fields1)==len(fields2) and len(fields1)>0:
        for i in range(len(fields1)):
            storage1[fields1[i]]=storage2[fields2[i]]
        return storage1
    else:
        raise Exception,u"字段数量不对应或未配置"
def TimeStr(fmt="%Y%m%d%H%M%S"):
    return time.strftime(fmt)

def JsonResult(the_result):
    result ={"result":the_result}
    return toJson(result)

def safewhere(s):
    """
    用于过滤注入句语
    ...
    sql = "parent_id in (SELECT id FROM t_Menu WHERE module_code = '"+qn(md_code)+"')"
    ....
    """
    dirty_stuff = ["\"", "\\", "/", "*", "'", "=", "-", "#", ";", "<", ">", "+", "%"]
    for stuff in dirty_stuff:
        s = s.replace(stuff,"")
    return s


def GETMD5(src):
    """
    用于生成md5串
    """
    import hashlib
    return hashlib.md5(src).hexdigest()

class MyEncoder(json.JSONEncoder):
    """
    用来配合序列化对象
    """
    def default(self, obj):
        # if isinstance(obj, datetime.datetime):
        #     return int(mktime(obj.timetuple()))
        if isinstance(obj, datetime):
          return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
          return obj.strftime('%Y-%m-%d')
        elif isinstance(obj,Decimal):
          return str(obj)
        else:
          return json.JSONEncoder.default(self, obj)

def __default(obj):
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, datetime.date):
        return obj.strftime('%Y-%m-%d')
    elif isinstance(obj,Decimal):
        return str(obj)
    else:
        raise TypeError('%r is not JSON serializable' % obj)

def toJson(obj):
    """
    将对象转换成json串,
    一般入口请使用web.utils的storage对象
    解决日期不能dumps问题
    """
    import json
    return json.dumps(obj,default=__default,ensure_ascii=False,indent=2,cls=MyEncoder)