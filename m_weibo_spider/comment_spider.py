# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 16:41:56 2018

抓取某一微博的评论信息

api: https://m.weibo.cn/api/comments/show?id="id"&page=1(2,3,4...)

@author: fivelike
"""
import requests
import json
import openpyxl

class Comment:
    session = requests.Session()
    
    
    def __init__(self,passage_id,wbname):
        self.url_start = "https://m.weibo.cn/api/comments/show?id=" +passage_id+"&page="
        self.passage_id = passage_id
        self.wbname = wbname
        
    def write_contents(self):
        page = 1
        count = 0
        
        wb = openpyxl.load_workbook(self.wbname)
        ws2 = wb["评论信息"]
        
        while True:
            try:
                res = self.session.get(self.url_start+str(page))
            except:
                print("获取page{0}失败".format(page))
                continue
            json_data = json.loads(res.text)
            if json_data["ok"] == 0:
                break
            comments = json_data["data"]["data"]
            for comment in comments:
                text = comment["text"]
                like_counts = comment["like_counts"]
                screen_name = comment["user"]["screen_name"]
                user_id = comment["user"]["id"]
                created_at = comment["created_at"]
                try:
                    ws2.append([self.passage_id,
                                text,
                                like_counts,
                                screen_name,
                                user_id,
                                created_at])
                    count+=1
                    if count%200==0:
                        print("已写入{0}条评论数据".format(count))
                except:
                    print("插入数据失败")
                    continue
            page+=1
        #保存文件
        wb.save(self.wbname)
        print("共爬取文章：{0}——{1}条评论".format(self.passage_id,count))
