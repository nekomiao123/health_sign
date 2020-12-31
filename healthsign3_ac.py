import requests
import time
import urllib3
import json
import gzip
import os
import datetime
import yaml

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


class HealthSign(object):
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
        # 每个URL后面都应该加上当时的时间戳
        self.loginUrl = "https://xsc-health.wh.sdu.edu.cn/mobile/rpc?p=/v2/login/login&t="
        self.idUrl = "https://xsc-health.wh.sdu.edu.cn/mobile/rpc?p=/v2/fight/ncp/health/report/getId&t="
        self.oldTimeUrl = "https://xsc-health.wh.sdu.edu.cn/mobile/rpc?p=/v2/cmdb/ci/getById&t="
        self.getDataUrl = "https://xsc-health.wh.sdu.edu.cn/mobile/rpc?p=/v2/workorder/formRule/execute&t="
        self.signUrl = "https://xsc-health.wh.sdu.edu.cn/mobile/rpc?p=/v2/workorder/action/createWithValidate&t="

        self.signSession = requests.Session()
        self.signHeader = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36',
            "content-type": "application/json"
            }
        self.loginCookie = None
        self.loginId = None
        self.userBasicInfo = None
        self.userAllInfo = None
        self.length = 0

    # 创建13位时间戳
    def getTimeStamp(self):
        now = time.time()
        now = (int(now * 1000))
        strnow = str(now)
        return strnow

    # 登录函数
    def healthLogin(self):
        loginTime = self.getTimeStamp()
        realLoginUrl = self.loginUrl + loginTime
        loginData = {
            "jsonrpc": "2.0",
            "method": "/v2/login/login",
            "id": 1,
            "params": [self.username, self.password, "false"]
        }
        try:
            r = self.signSession.post(realLoginUrl, json=loginData, verify=False)
            str1 = str(r.cookies)
            self.loginCookie = str1[27:67]
            print("登录成功")
        except:
            print("登录失败，请检查账号密码是否正确")
        
        return self.signSession

    # 获取id
    def getId(self):
        idTime = self.getTimeStamp()
        realIdUrl = self.idUrl + idTime
        idData = {
            "jsonrpc": "2.0",
            "method": "/v2/fight/ncp/health/report/getId",
            "id": 1,
            "params": []
        }
        try:
            idRequest = self.signSession.post(realIdUrl, json=idData, headers = self.signHeader)
            idRJson = idRequest.json()
            self.loginId = idRJson['result']
            print("获取id成功")
            # print("realID is ")
            # print(self.loginId)
        except:
            print("id获取失败")
    
    # 获取基础用户信息
    def getOldUserInfo(self):
        oldTimeT = self.getTimeStamp()
        realOldTimeUrl = self.oldTimeUrl + oldTimeT
        # params的第一个参数是最后的type，并不知道是什么，但是测试了好几次，这个type是不变的
        oldTimeData = {
            "jsonrpc": "2.0",
            "method": "/v2/cmdb/ci/getById",
            "id": 1,
            "params": ["40bca208-5184-11ea-887d-cb65bdaac481", self.loginId]
        }
        try:
            oldTimeRequests = self.signSession.post(realOldTimeUrl, json=oldTimeData, headers=self.signHeader)
            # print("oldTImeRequest")
            # print(oldTimeRequests.headers)
            oldHeaderJson = oldTimeRequests.headers
            # 虽然很无奈 但是好像只能用这个length来判断打过卡没
            self.length = oldHeaderJson['Content-Length']
            self.length = int(self.length)
            # print("Content-Length is")
            print(self.length)
            oldTRJson = oldTimeRequests.json()

            # 针对返回情况的优化
            shifouquedingfanhuishijian = ""
            fanhuishijian = ""
            if "shifouquedingfanhuishijian" in oldTRJson['result']:
                shifouquedingfanhuishijian = oldTRJson['result']['shifouquedingfanhuishijian']['name']
            if "fanhuishijian" in oldTRJson['result']:
                fanhuishijian = oldTRJson['result']['fanhuishijian']
            
            self.userBasicInfo = {
                "apply_user": oldTRJson['result']['apply_user']['id'],
                "xm": oldTRJson['result']['xm'],
                "xh": oldTRJson['result']['xh'],
                "xb": oldTRJson['result']['xb']['name'],
                "lxdh": oldTRJson['result']['lxdh'],
                "fanhuishijian": fanhuishijian,
                "id": self.loginId,
                "type": "40bca208-5184-11ea-887d-cb65bdaac481",
                "source": "mobile"
            }
            #这里可以输出用户名字
            # print(self.userBasicInfo['xm'])
            
            if self.length > 1000:
                self.userAllInfo = {
                    "xllb": oldTRJson['result']['xllb']['name'],              
                    "szyx": oldTRJson['result']['szyx']['id'],    
                    "tiwen": oldTRJson['result']['tiwen'],   
                    "dw": oldTRJson['result']['dw'],
                    "shifouzaixiao": oldTRJson['result']['shifouzaixiao']['name'],                                  
                    "shifouyifanhuihuocongweilikaixuexiao": oldTRJson['result']['shifouyifanhuihuocongweilikaixuexiao']['name'],      
                    "muqiansuozaichengshi": oldTRJson['result']['muqiansuozaichengshi']['name'],                
                    "sheng": oldTRJson['result']['sheng']['id'],         
                    "shi": oldTRJson['result']['shi']['id'],           
                    "qu": oldTRJson['result']['qu']['id'],            
                    "xxdz": oldTRJson['result']['xxdz'],     
                    "shifouquedingfanhuishijian": shifouquedingfanhuishijian,                     
                    "fanhuishijian": fanhuishijian,    
                }
                print("该用户已经打过卡，获取数据成功")

            # print("用户基础数据")
            # print(self.userBasicInfo)
        except:
            print("获取用户基础数据失败")


    # 获取用户所有信息
    def getAllInfo(self):
        allTime = self.getTimeStamp()
        realAllUrl = self.getDataUrl + allTime
        allData = {
            "jsonrpc": "2.0",
            "method": "/v2/workorder/formRule/execute",
            "id": 1,
            "params": ["8a525ad7-5187-11ea-a13f-53bf2079bf35", {
                "type": "init",
                "param": True
            }, {
                "data": {
                    "apply_user": self.userBasicInfo["apply_user"],
                    "xm": self.userBasicInfo['xm'],
                    "xh": self.userBasicInfo['xh'],
                    "xb": self.userBasicInfo['xb'],
                    "lxdh": self.userBasicInfo['lxdh'],
                    "fanhuishijian": self.userBasicInfo['fanhuishijian'],
                    "id": self.userBasicInfo['id'],
                    "type": self.userBasicInfo['type'],
                    "source": self.userBasicInfo['source']
                },
                "params": {}
            }]
        }

        try:
            getAllRequests = self.signSession.post(realAllUrl, json=allData, headers=self.signHeader)
            getAllJson = getAllRequests.json()
            # print(getAllRequests.headers)
            # 输出这个文件能看到详细的用户数据
            # fJson = json.dumps(getAllJson, sort_keys=True, indent=4, ensure_ascii=False)
            # with open('Allinfo.json', 'w') as f:
            #     f.write(fJson)
            # 只有length<1000的时候logs里面才有正确的值
            if self.length < 1000:
                logs = getAllJson["result"]["logs"]
                self.userAllInfo = logs['日志格式错误，请修改脚本']['page']['data'][0]
                print("该用户尚未打卡，获取用户所有数据成功")
                # print(type(self.userAllInfo))
                # print(self.userAllInfo)

        except:
            print("无法获取用户全部数据")

    # 打卡函数
    def signAll(self):
        signTime = self.getTimeStamp()
        realSignUrl = self.signUrl + signTime

        # 针对返回情况的优化
        shifouquedingfanhuishijian = ""
        fanhuishijian = ""
        if "shifouquedingfanhuishijian" in self.userAllInfo:
            shifouquedingfanhuishijian = self.userAllInfo['shifouquedingfanhuishijian']
        if "fanhuishijian" in self.userAllInfo:
            fanhuishijian = self.userAllInfo['fanhuishijian']

        # 这个data特别多 
        signData = {
        "jsonrpc": "2.0",
        "method": "/v2/workorder/action/createWithValidate",
        "id": 1,
        "params": [
            [
                {
                    "id": self.loginId, 
                    "type": self.userBasicInfo['type'],
                    "source": self.userBasicInfo['source'], 
                    "apply_user": self.userBasicInfo['apply_user'],    
                    "xllb": self.userAllInfo['xllb'],              
                    "szyx": self.userAllInfo['szyx'],          
                    "xm": self.userBasicInfo['xm'],
                    "xh": self.userBasicInfo['xh'],
                    "xb": self.userBasicInfo['xb'],    
                    "lxdh": self.userBasicInfo['lxdh'],             
                    "jkzt": "健康",                             
                    "shifoufare": "否",                                       
                    "tiwen": self.userAllInfo['tiwen'],                                           
                    "shifoujiuzhenzhuyuan": "",                              
                    "yiyuanmingcheng": "",                                   
                    "shifougeli": "fou",                                     
                    "gelifangshi": "",                                       
                    "gelidizhi": "",                                         
                    "dw": self.userAllInfo['dw'],       
                    "cunjieqijianshifouzaixiao": "fou",                      
                    "shifouzaixiao": self.userAllInfo['shifouzaixiao'],                                  
                    "shifouyifanhuihuocongweilikaixuexiao": self.userAllInfo['shifouyifanhuihuocongweilikaixuexiao'],      
                    "muqiansuozaichengshi": self.userAllInfo['muqiansuozaichengshi'],                
                    "sheng": self.userAllInfo['sheng'],         
                    "shi": self.userAllInfo['shi'],           
                    "qu": self.userAllInfo['qu'],            
                    "xxdz": self.userAllInfo['xxdz'],                                       
                    "guowaidizhi": "",                                       
                    "shifouquedingfanhuishijian": shifouquedingfanhuishijian,                     
                    "fanhuishijian": fanhuishijian,                          
                    "jinyigeyueshifouquguohubei": "fou",                     
                    "jinyigeyueshifoujiechuguoquezhenbingli": "fou",         
                    "jinyigeyueshifoujiechuguoyisibingli": "fou",            
                    "miqiejiechuguanxi": "",                                 
                    "ganranzhe": "否",                                       
                    "jiechuzhe": "否",                                       
                    "juzhu": "否",                                           
                    "fare": "否",                                            
                    "hubeijingwai": "否"    
                    }
                    ],
                    [
                        "8a525ad7-5187-11ea-a13f-53bf2079bf35"
                    ]
                ]
            }
        # # 这里能输出最后打卡的数据
        # json_str = json.dumps(signData, sort_keys=True, indent=4, ensure_ascii=False)
        # filename = 'finalSend_' + str(username) + '.json'
        # with open(filename, 'w') as f:
        #     f.write(json_str)
        # print("输出待提交的打卡数据成功")
        try:
            signRequest = self.signSession.post(realSignUrl, json=signData, headers=self.signHeader)
            # print("signRequest: ")
            # print(signRequest.text)

            end = "<Response [200]>"
            if end == str(signRequest):
                print("打卡成功")
            else:
                print("打卡失败")
        except:
            print("提交打卡数据失败")


def main(username, password):
    print("\n[Time] %s" %datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("🚌 打卡任务启动")
    daka = HealthSign(username, password)

    daka.healthLogin()
    
    daka.getId()

    daka.getOldUserInfo()

    daka.getAllInfo()

    daka.signAll()
    print("打卡任务结束")


def read():
    if 'CONFIG' in os.environ:
        config_current = yaml.load(os.environ['CONFIG'], Loader=yaml.FullLoader)
        studentIDs = config_current['jobs']['studentID']
        return studentIDs
    else:
        print("获取学号出错，请检查yaml文件")


if __name__ == "__main__":
    # 忽略TLS Warnings警告
    urllib3.disable_warnings()
    usernames = read()
    for username in usernames:
        password = "whsdu@" + username
        main(username, password)




