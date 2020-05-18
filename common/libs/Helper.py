from flask import jsonify,session
import time
from hdfs import InsecureClient



def ops_renderJSON( code = 200,msg = "操作成功~~",data = {} ):
    resp = { "code":code,"msg":msg,"data":data }
    return jsonify( resp )

def ops_renderErrJSON( msg = "系统繁忙，请稍后再试~~",data = {} ):
    return ops_renderJSON( code = -1,msg = msg,data = data )


def check_login():
    try:
        session["uid"]
    except:
        return False
    else:
        return True

# 输入毫秒级的时间，转出正常格式的时间
def timeStamp(timeNum):
    timeStamp = float(timeNum/1000)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

