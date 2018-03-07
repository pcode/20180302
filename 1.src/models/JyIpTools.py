#coding=utf8
from web.utils import storage

__author__ = 'Administrator'
from models.ipdb import ipdb
import web
def GetIpLong(ip):
    ip=ip.split(".")
    if len(ip)==4:
      ip = 16777216 * long(ip[0]) + 65536 * long(ip[1]) + 256 * long(ip[2]) + long(ip[3]);
      return ip
    else:
        return 0
def GetCurrentuserIP():
    return web.ctx.get("ip","0.0.0.0")
def GetIPRegion(ip):
    obj=ipdb()
    ipl=GetIpLong(ip)
    rec=obj.GetRowByDbWhere(where=" (IPSTART1<=$ipl and IPEND1>=$ipl) " ,vars ={'ipl':ipl})
    if rec:
        return "IP:"+ip+" 解析为:"+ rec.REGION1 + "," + rec.REGION2
def GetUserIPRegion():
    ip=GetCurrentuserIP()
    return GetIPRegion(ip)

if __name__=="__main__":
    import datetime
    print GetIpLong("218.108.132.106")
    a=datetime.datetime.now()
    print GetIPRegion("218.108.132.106")
    b=datetime.datetime.now()
    print b-a