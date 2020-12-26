import requests
import time
import urllib3
import json
import gzip
import os

''' 
    每日打卡3.0版
    采用requests库进行发包和接收包,方便快捷
    用类的思想重写整个代码，增加可读性和可扩展性

    过程
    1.先发送登陆包，然后服务器会返回一个维持会话的cookie；
    2.之后再发一个包获得当天的打卡id；
    3.最后发打卡包。
    使用python的requests库进行发包
    1.将账号密码设为字典，之后发第一个登录包，用字符串操作获得cookie，
    2.置入下一个获得id的包中，发包，用json格式化获得id
    3.根据这个id和一个不知道是什么的type id获得老数据
    4.将老数据置入打卡包，加入新修改的地址数据
    5.发打卡包，接受返回信息，如果是200，即成功。

'''





