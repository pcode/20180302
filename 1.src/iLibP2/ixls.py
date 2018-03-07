#encoding=utf-8
#额外函数请自行定义
#encoding=utf-8
#额外函数请自行定义
from evn import TP_PATH
from iLibP2.loger import *
from web.utils import storage,dictreverse
import datetime,traceback,time,os,web,xlrd
class iXls:
    def uploadFile(self):
        """
        :param school_no:
        :return:上传成功后的文件名
        """
        try:
            now_month = datetime.datetime.now().strftime("%Y%m")
            tpath = TP_PATH + "/static/uploads/" + now_month
            if not os.path.exists(tpath):
                os.makedirs(tpath)
            # 使用跟图片一致的路径
            strBaseLocation = tpath
            # 需要在这里增加一个excel={}否则上传的文件名及大小等信息不会被保留
            x = web.input(excel={})
            nfilename = strBaseLocation + "/u_" + time.strftime("%Y%m%d%H%M%S") + ".xls"
            # excel需要使用二进制写入打开参数需要wb
            fout = open(nfilename, 'wb')
            fout.write(x["excel"].file.read())
            fout.close()
            return nfilename
        except Exception,ex:
                msg = u"excelParser执行uploadFile函数出错,[具体信息]:"+str(traceback.format_exc())+u"\n[数据]:\n"+str(ex)
                LogError(msg)
                raise Exception,msg
    def parseXls(self,fieldrelation,excelfilepath):
        """
        解析xls，如果解析到字段的中文英文定义，则按对照来做，否则按列的名称来尝试，给定的字段名一定是中：英这样。
        :param fieldrelation:
        字段对照关系，中文对照数据字段
        类似
        {
                        u'来源表id':'src_id',
                        u'姓名':'truename',
                        u'出生日期':'birthday',
                        u'电话号码':'phoneno',
                        u'机构名称':'orgname',
                        u'绘画作品小样':'thumbpaintfile',
                        u'绘画作品':'paintfile',
        }
        :param excelfilepath: excel文件是已经上传到系统的文件绝对路径
        :return:
        """
        try:
        #结果对象
            result = storage()
            #数据集合
            rows = []
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
            fr1 = dictreverse(the_fields_relation)
            fr2 = the_fields_relation
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
                rows.append(row_data)

            #封装返回结果
            result.fields       = cols_infos
            result.rows         = rows
            result.row_count    = nrows - 1
            result.col_count    = ncols
            return result
        except :
           raise Exception, "install xlrd first,pypm install xlrd"


    def openExistExcel(self,excelfilename):
        """
        返回一个可以写入数据工作簿
        """
        try:
            from xlrd import open_workbook
            from xlutils.copy import copy
            #打开EXCEL并保留格式信息
            rb = open_workbook(excelfilename,formatting_info=True)
            wb=copy(rb)
            ws=wb.get_sheet(0)
            return wb,ws
        except :
            print "pypm install xlrd;pypm install xlwt;pypm install xlutils.then try again"
            return None