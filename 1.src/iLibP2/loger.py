#coding=utf-8
__author__ = 'jy@cjlu.edu.cn'
import logging,os
import logging.handlers
def _initlog(logname,filename):
    """
    生成日志对象
    @param logname:日志名称
    @type logname:字符串
    @param filename:文件名称
    @type filename:字符串
    @return:日志对象
    """
    LOG_PATH = os.getcwd()+"/log/"
    if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)
    logger = logging.getLogger(logname)
    #使用最低的级别
    logger.setLevel(logging.DEBUG)
    #使用按天备份日志的方式
    hdlr = logging.handlers.TimedRotatingFileHandler(LOG_PATH+filename,when="D",interval=1, backupCount=0, encoding=None, delay=False, utc=False)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    return logger
#系统日志对象

_loger=_initlog("sys","syslog.txt")
#操作日志对象
_optloger=_initlog("opt","opt.txt")

def LogOpt(msg):
    """
    记录操作记录
    @param msg:需要记录的内容
    @type msg:字符串

    """
    _optloger.info(msg)
    
def LogError(msg):
    """
    记录系统错误
    @param msg:需要记录的内容
    @type msg:字符串
    """
    _loger.error(msg)

def LogInfo(msg):
    """
    记录系统信息
    @param msg:需要记录的内容
    @type msg:字符串
    """
    _loger.info(msg)

def LogWarning(msg):
    """
    记录系统警告
    @param msg:需要记录的内容
    @type msg:字符串
    """
    _loger.warn(msg)
    
def LogDebug(msg):
    """
    记录系统调试信息
    @param msg:需要记录的内容
    @type msg:字符串
    """
    _loger.debug(msg)
