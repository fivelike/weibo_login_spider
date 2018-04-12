# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 20:08:22 2018
抓取某一微博的转发信息
@author: fivelike
"""

import requests
import json
import openpyxl

class Repost:
    session = requests.Session()
    
    
    def __init__(self,passage_id,wbname):
        self.url_start = "https://m.weibo.cn/api/statuses/repostTimeline?id="+passage_id+"&page="
        self.passage_id = passage_id
        self.wbname = wbname
        
    def write_contents(self):
        page = 1
        count = 0
        
        wb = openpyxl.load_workbook(self.wbname)
        ws3 = wb["转发信息"]
        
        while True:
            try:
                res = self.session.get(self.url_start+str(page))
            except:
                print("获取page{0}失败".format(page))
                continue
            json_data = json.loads(res.text)
            if json_data["ok"] == 0:
                break
            reposts = json_data["data"]["data"]
            for repost in reposts:
                text = repost["text"]
                screen_name = repost["user"]["screen_name"]
                user_id = repost["user"]["id"]
                created_at = repost["created_at"]
                try:
                    ws3.append([self.passage_id,
                                text,
                                screen_name,
                                user_id,
                                created_at])
                    count+=1
                    if count%200==0:
                        print("已写入{0}条转发数据".format(count))
                except:
                    print("插入数据失败")
                    continue
            page+=1
        #保存文件
        wb.save(self.wbname)
        print("共爬取文章：{0}——{1}条转发信息".format(self.passage_id,count))