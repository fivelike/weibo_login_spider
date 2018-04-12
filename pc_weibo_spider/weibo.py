# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 21:13:51 2018
pc_weibo模拟登陆
@author: fivelike
"""

import requests
import base64
import rsa
import urllib.request
import re
import json
import binascii

"""
weibo登陆类
    args：
        username : string
        password : string
"""
class Launcher:
    session = requests.Session()
    
    def __init__(self,username,password):
        self.username = username
        self.password = password

    #返回加密后的string username
    def get_encrypted_username(self):
        username_urllike = urllib.request.quote(self.username)
        username_encrypted = base64.b64encode(bytes(username_urllike,encoding="utf-8"))
        return username_encrypted.decode("utf-8")
    
    #模拟预登录，获取服务器返回的nonce，servertime，pub_key等信息，用字典返回
    def get_prelogin_args(self):
        json_pattern = re.compile("\{(.*)\}")
        url = "https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su="+self.get_encrypted_username()+"&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)"
        try:
            res = self.session.get(url)
#            res = requests.get(url)
#            print(res.text)
            json_data = json_pattern.search(res.text).group()
#            print(json_data)
            data = json.loads(json_data)
            
            return data
        except:
            print("预登录失败")
            return None

    #利用预登录信息生成rsa加密过的密码，需要的密码信息用data传入,返回加密后的密码
    def get_encrypted_password(self,data):
        rsa_e = 65537 #0x10001 65537
        pw_string = str(str(data["servertime"])+"\t"+str(data["nonce"])+"\n"+self.password)
#        pw_string = "1521191709" + "\t" + "OMQ782" + "\n" + self.password

        key = rsa.PublicKey(int(data["pubkey"],16),rsa_e)
        pw_encrypted = rsa.encrypt(pw_string.encode("utf-8"),key)
        passwd = binascii.hexlify(pw_encrypted)
#        print(pw_encrypted)
#        return str(passwd,encoding="utf-8")
        return passwd.decode("utf-8")

    #构造POST登陆请求的data字典，raw字典来自get_prelogin_args返回的字典
    def build_post_data(self,raw):
        post_data = {
            "entry":"weibo",
            "gateway":"1",
            "from":"",
            "savestate":"7",
            "qrcode_flag": "false",
            "useticket":"1",
            "pagerefer":"https://passport.weibo.com/visitor/visitor?entry=miniblog&a=enter&url=https%3A%2F%2Fweibo.com%2F&domain=.weibo.com&sudaref=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DxsROu3DQg5nzb9GgJkpgTl7-6Y01N3XlnZLKH-YSlS_%26wd%3D%26eqid%3Df3520b9100017833000000035aab7d27&ua=php-sso_sdk_client-0.6.23",
            "vsnf":"1",
            "su":self.get_encrypted_username(),
            "service":"miniblog",
            "servertime":raw['servertime'],
            "nonce":raw['nonce'],
            "pwencode":"rsa2",
            "rsakv":raw['rsakv'],
            "sp":self.get_encrypted_password(raw),
            "sr":"1440*900",
            "encoding":"UTF-8",
            "prelt":"42",
            "url":"https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            "returntype":"META"
        }
#        print(post_data)
        return post_data
    
    def login(self):
        url = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)"
        args = self.get_prelogin_args()
        post_data = self.build_post_data(args)
        
        headers =  {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://weibo.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36",
            "Host": "login.sina.com.cn",
            "Origin": "https://weibo.com",               
        }
        try:
            res = self.session.post(url,data=post_data,headers=headers)
#            print(res.apparent_encoding)  #识别返回编码
            res.encoding = "GBK"
#            print(res.text)
#            print(res.status_code)
        except:
            print("1重定向登陆失败")
            
        p = re.compile('location\.replace\(\"(.*)\"\)')
        p2 = re.compile('location\.replace\(\'(.*)\'\)')
        p3 = re.compile(r'"userdomain":"(.*?)"')

        try:
            #重定向1
            login_url = p.search(res.text).group(1)
#            print(login_url)
            page = self.session.get(login_url)
            page.encoding ="GBK"
#            print(page.text)

            #重定向2
            replace_url = p2.search(page.text).group(1)
#            print(replace_url)
            page2 = self.session.get(replace_url)
            page2.encoding = "GBK"
#            print(page2.text)

            #重定向3 final_res 为已登陆response对象
            final_url = "https://weibo.com" + p3.search(page2.text).group(1)
#            print(final_url)
            final_res = self.session.get(final_url)
            print("Login success!")
            return final_res
            
        except:
            print("Login error!")
            return 0
        
    def get(self,url):
        try:
            logined_res = self.session.get(url)
            return logined_res
        except:
            print("获取页面失败！")



