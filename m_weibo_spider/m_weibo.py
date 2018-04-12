# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 12:45:44 2018
m_weibo模拟登陆
@author: ASUS
"""
import requests
import json

class Launcher:
    
    session = requests.Session()
    
    def __init__(self,username,password):
        self.username = username
        self.password = password
        
    def build_post_data(self):
        post_data = {
            "username": self.username,
            "password": self.password,
            "savestate": "1",
            "r": "http://weibo.cn/",
            "ec": "0",
            "pagerefer": "",
            "entry": "mweibo",
            "wenter": "",
            "loginfrom": "",
            "client_id": "",
            "code": "",
            "qq": "",
            "mainpageflag": "1",
            "hff": "",
            "hfp": ""
        }
        return post_data
    
    def login(self):
        url = "https://passport.weibo.cn/sso/login"
        try:
            self.session.get(url)
        except:
            print("获取cookie失败！")
            
        post_data = self.build_post_data()
        headers =  {
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://passport.weibo.cn/signin/login?entry=mweibo&r=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt=",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
            "Host": "passport.weibo.cn",
            "Origin": "https://passport.weibo.cn",               
        }
        
        try:
            res = self.session.post(url,data=post_data,headers=headers)
            data = json.loads(res.text)
#           print(data)
            page = self.session.get(data["data"]["loginresulturl"]+"&savestate=1&url=http://weibo.cn/")
            print("Login success!")
            return page
        except:
            print("Login error!")
    
    def get(self,url):
        try:
            logined_res = self.session.get(url)
            return logined_res
        except:
            print("获取页面失败！")

