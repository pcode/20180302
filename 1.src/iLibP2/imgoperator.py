#coding=utf-8
import base64
import datetime,time
import os

from web import storage

from config import TP_PATH

__author__ = 'jy@cjlu.edu.cn'
"""
created by jy 2015-08-26
使用tornado方式上传图片文件
"""
def gcPath():
    """
    创建上传目录，按月度处理上传的文件内容。避免一个目录的文件太多难以管理
    如果以后使用分布式来做，可以改造这个函数来处理
    :return:目录名
    """
    now_month = datetime.datetime.now().strftime("%Y%m")
    tpath=TP_PATH+"/static/uploads/"+now_month
    if not os.path.exists(tpath):
        os.mkdir(tpath)
    return tpath
class ImgOperator:
    """

    """
    def uploadBase64File(self,base64str,filename):
        """

        :param base64str:
        :param filename:
        :return:
        """
        result = storage({
            "result":"NOOK",
            "nfilename":"",
            "pfilename":"",
            "ofilename":filename,
        })
        try:
            filetype, filecontent = base64str.split('base64,')
            file_path = gcPath()
            fileext = filename.split(".")[-1]
            new_file_name = file_path + "/" + time.strftime("%Y%m%d%H%M%S") + "."+fileext
            fc = base64.decodestring(filecontent)
            fout = open(new_file_name, 'wb')
            fout.write(fc)
            fout.close()
            result.result    = "OK"
            result.nfilename = new_file_name.replace(TP_PATH, '')
            result.pfilename = new_file_name
            result.ofilename = filename
        except:
            print "Uploading file error!"
            pass
        return result

    def uploadBase64StrFile(self,base64str):
        """
        使用js api 的FileReader对象的readAsDataURL函数来读取数据，把数据变成一个base64编码的字符串，再来上传
        added by jy 2016-07-05
        :param base64str:
         data:image/png;base64,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
        :return:
        """
        filetype,filecontent=base64str.split('base64,')
        file_path=gcPath()
        if 'png' in filetype:
            fileext = ".png"
        if 'jpeg' in filetype:
            fileext = ".jpg"
        if 'text' in filetype:
            fileext = ".txt"
        new_file_name=file_path +"/"+ time.strftime("%Y%m%d%H%M%S")+fileext

        fc=base64.decodestring(filecontent)
        fout = open(new_file_name,'wb')
        fout.write(fc)
        fout.close()
        return new_file_name.replace(TP_PATH,'')

    def uploadFile(self,i):
        """
        上传文件，输入参数是i，将给定的文件上传到目标目录；
        在指定目录按月度设置目录，如果目录存在就使用，如果不存在就建立一个；
        格式类似/201508/ 代表2015年8月上传的
        :param i: 页面传入参数
        :return:保存到文件后的重名名的文件名
        """
        try:
            file_path=gcPath()
            if "files" in i:
                #只处理一个图片上传的内容这个组件必须被命名为image_upload
                f = i['files']
                file_ext_name = os.path.splitext(f.filename)[1][1:].lower()
                if file_ext_name in ["jpg","png","gif"]:
                    new_file_name = file_path +"/"+ time.strftime("%Y%m%d%H%M%S")+"."+file_ext_name
                    fout = open(new_file_name,'wb')
                    fout.write(f.file.read())
                    fout.close()
                    return new_file_name.replace(TP_PATH,'')
                else:
                    raise Exception, "filetype error,allow filetype jpg,png,gif."
        except:
            raise Exception, "Upload file error,please check filefield image_upload."

if __name__ == "__main__":
    #path="asdfasdf.png"
    #print os.path.splitext(path)[1][1:]
    #now = datetime.datetime.now().strftime("%Y%m")
    #print now
    # stra="data:image/png;base64,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"
    # opt = ImgOperator()
    # fn = opt.uploadBase64StrFile(stra)
    # print fn

    filename ="1.1src.asdfasdf.py"
    ns = filename.split(".")
    print ns[-1]