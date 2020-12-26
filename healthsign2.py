import requests
import time
import urllib3
import json
import gzip
import os

''' 
    每日打卡2.0版
    采用requests库进行发包和接收包
    方便快捷，整体用时3 s

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

# 创建13位时间戳
def getTimeStamp():
    now = time.time()
    now = (int(now * 1000))
    strnow = str(now)
    return strnow


def main(username, password):
    # 登录时间
    loginTime = getTimeStamp()

    # 开始进行登录
    loginHeaders = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36'
    }
    loginUrl = 'https://xsc-health.wh.sdu.edu.cn/mobile/rpc?p=/v2/login/login&t=' + loginTime

    # print("login url " + loginUrl)
    # 请求数据
    loginData = {
        "jsonrpc": "2.0",
        "method": "/v2/login/login",
        "id": 1,
        "params": [username, password, "false"]
    }
    # 新建一个session类 以后都在session里面通信
    session = requests.Session()
    # 发送post请求
    try:
        r = session.post(loginUrl, json=loginData, headers=loginHeaders, verify=False)
        # 打印cookie
        # print("r: ")
        # print(r.headers)
        # 获取cookie，这里用的是字符串操作，感觉可能用正则好一点
        # print(r.cookies)
        str1 = str(r.cookies)
        loginCookie = str1[27:67]
        # print("realCoocie is ")
        # print(loginCookie)
    except:
        print("请求失败")

    # 获取id
    idHeaders = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36",
        "content-type": "application/json",
        "Cookie": loginCookie
    }

    idTime = getTimeStamp()
    idUrl = "https://xsc-health.wh.sdu.edu.cn/mobile/rpc?p=/v2/fight/ncp/health/report/getId&t=" + idTime
    # print("idUrl: " + idUrl)

    idData = {
        "jsonrpc": "2.0",
        "method": "/v2/fight/ncp/health/report/getId",
        "id": 1,
        "params": []
    }
    try:
        idRequest = session.post(idUrl, json=idData, headers=idHeaders)
        # print("idRequest is ")
        # print(idRequest)
        # print(idRequest.headers)
        idRJson = idRequest.json()
        # print(idRJson)
        realId = idRJson['result']
        print("realID is ")
        print(realId)
    except:
        print("id获取失败")

    # 获取之前的打卡信息
    oldTimeHeaders = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36",
        "Connection": "keep-alive",
        "Content-Length": "144",
        "Accept": "*/*",
        "X-User-Lang": "zh-CN",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://xsc-health.wh.sdu.edu.cn",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://xsc-health.wh.sdu.edu.cn/mobile/index.html",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6",
        "Accept-Encoding": "gzip, deflate, br",
        "content-type": "application/json",
        "Cookie": loginCookie
    }

    oldTimeT = getTimeStamp()
    oldTimeUrl = "https://xsc-health.wh.sdu.edu.cn/mobile/rpc?p=/v2/cmdb/ci/getById&t=" + oldTimeT
    # print("oldTimeURl: " + oldTimeUrl)

    # params的第一个参数是最后的type，并不知道是什么，但是测试了好几次，这个type是不变的
    oldTimeData = {
        "jsonrpc": "2.0",
        "method": "/v2/cmdb/ci/getById",
        "id": 1,
        "params": ["40bca208-5184-11ea-887d-cb65bdaac481", realId]
    }

    try:
        oldTimeRequests = session.post(
            oldTimeUrl, json=oldTimeData, headers=oldTimeHeaders)
        print("oldTimeRequests: ")
        # with open('info2.json', 'w') as f:
        #     f.write(oldTimeRequests.text)
        # print(oldTimeRequests)
        print(oldTimeRequests.headers)
        # print(oldTimeRequests.content.decode())
        # print(oldTimeRequests.json())
        oldTRJson = oldTimeRequests.json()
        userinfo = None
        if 'modify_user' in oldTRJson['result']:
            print(oldTRJson['result']['modify_user'])
            userinfo = oldTRJson['result']['modify_user']
        if 'apply_user' in oldTRJson['result']:
            print(oldTRJson['result']['apply_user'])
            userinfo = oldTRJson['result']['apply_user']

        # with open('all_info.txt', 'a+') as f:
        #     f.write(str(oldTimeRequests.headers) + '\n')
        #     f.write(str(userinfo) + '\n')
    except:
        print("获取打卡历史数据失败")


    # # 测试打卡代码
    # testHeaders = {
    #     "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36",
    #     "Cookie": loginCookie
    # }
    # testTime = getTimeStamp()
    # testUrl = "https://xsc-health.wh.sdu.edu.cn/mobile/rpc?p=/v2/cmdb/ci/getById&t=" + testTime
    # testData = {"jsonrpc": "2.0", "method": "/v2/cmdb/ci/getById", "id": 1, "params": [
    #     "40bca208-5184-11ea-887d-cb65bdaac481", "952016c3-46f5-11eb-bb47-83ad6615480f"]}
    # testRequests = session.post(testUrl, json=testData, headers=testHeaders)
    # print("testRequests: ")
    # print(testRequests.headers)
    # with open('info2.json', 'w') as f:
    #     f.write(testRequests.text)

    # 发送打卡包
    signHeaders = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36",
        "content-type": "application/json",
        "Cookie": loginCookie
    }

    signTime = getTimeStamp()
    signUrl = "https://xsc-health.wh.sdu.edu.cn/mobile/rpc?p=/v2/workorder/action/createWithValidate&t=" + signTime
    # print("signUrl: ")
    

    # 针对返回情况的优化
    shifouquedingfanhuishijian = ""
    fanhuishijian = ""
    if "shifouquedingfanhuishijian" in oldTRJson['result']:
        shifouquedingfanhuishijian = oldTRJson['result']['shifouquedingfanhuishijian']['name']
    if "fanhuishijian" in oldTRJson['result']:
        fanhuishijian = oldTRJson['result']['fanhuishijian']

    # 这个data特别多 
    signData = {
    "jsonrpc": "2.0",
    "method": "/v2/workorder/action/createWithValidate",
    "id": 1,
    "params": [
        [
            {
                "id": realId,            
                "type": "40bca208-5184-11ea-887d-cb65bdaac481",          
                "source": "mobile",                                      
                "apply_user": oldTRJson['result']['apply_user']['id'],    
                "xllb": oldTRJson['result']['xllb']['name'],              
                "szyx": oldTRJson['result']['szyx']['id'],          
                "xm": oldTRJson['result']['xm'],                                           
                "xh": oldTRJson['result']['xh'],                                    
                "xb": oldTRJson['result']['xb']['name'],                                            
                "lxdh": oldTRJson['result']['lxdh'],                                   
                "jkzt": oldTRJson['result']['jkzt']['name'],                                           
                "shifoufare": oldTRJson['result']['shifoufare']['name'],                                       
                "tiwen": oldTRJson['result']['tiwen'],                                           
                "shifoujiuzhenzhuyuan": "",                              
                "yiyuanmingcheng": oldTRJson['result']['yiyuanmingcheng'],                                   
                "shifougeli": oldTRJson['result']['shifougeli']['name'],                                     
                "gelifangshi": "",                                       
                "gelidizhi": oldTRJson['result']['gelidizhi'],                                         
                "dw": oldTRJson['result']['dw'],       
                "cunjieqijianshifouzaixiao": oldTRJson['result']['cunjieqijianshifouzaixiao']['name'],                      
                "shifouzaixiao": oldTRJson['result']['shifouzaixiao']['name'],                                  
                "shifouyifanhuihuocongweilikaixuexiao": oldTRJson['result']['shifouyifanhuihuocongweilikaixuexiao']['name'],      
                "muqiansuozaichengshi": oldTRJson['result']['muqiansuozaichengshi']['name'],                
                "sheng": oldTRJson['result']['sheng']['id'],         
                "shi": oldTRJson['result']['shi']['id'],           
                "qu": oldTRJson['result']['qu']['id'],            
                "xxdz": oldTRJson['result']['xxdz'],                                       
                "guowaidizhi": oldTRJson['result']['guowaidizhi'],                                       
                "shifouquedingfanhuishijian": shifouquedingfanhuishijian,                     
                "fanhuishijian": fanhuishijian,                          
                "jinyigeyueshifouquguohubei": oldTRJson['result']['jinyigeyueshifouquguohubei']['name'],                     
                "jinyigeyueshifoujiechuguoquezhenbingli": oldTRJson['result']['jinyigeyueshifoujiechuguoquezhenbingli']['name'],         
                "jinyigeyueshifoujiechuguoyisibingli": oldTRJson['result']['jinyigeyueshifoujiechuguoyisibingli']['name'],            
                "miqiejiechuguanxi": "",                                 
                "ganranzhe": oldTRJson['result']['ganranzhe']['name'],                                       
                "jiechuzhe": oldTRJson['result']['jiechuzhe']['name'],                                       
                "juzhu": oldTRJson['result']['juzhu']['name'],                                           
                "fare": oldTRJson['result']['fare']['name'],                                            
                "hubeijingwai": oldTRJson['result']['hubeijingwai']['name']    
                }
                ],
                [
                    "8a525ad7-5187-11ea-a13f-53bf2079bf35"
                ]
            ]
        }
    json_str = json.dumps(signData, sort_keys=True, indent=4, ensure_ascii=False)
    with open('duibi_info.json', 'w') as f:
        f.write(json_str)

    signRequest = session.post(signUrl, json = signData, headers = signHeaders)
    print("signRequest: ")
    print(signRequest.text)

    end = "<Response [200]>"
    if end == str(signRequest):
        print("打卡成功")
    else:
        print("打卡失败")


if __name__ == "__main__":
    # 忽略TLS Warnings警告
    urllib3.disable_warnings()

    username = "201700800609"
    password = "whsdu@" + username
    print("开始为学号 " + username + "的同学开始打卡")
    main(username, password)



