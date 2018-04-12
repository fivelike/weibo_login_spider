# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 20:54:42 2018
    数据库相关
@author: ASUS
"""

import pymysql

db = pymysql.connect("localhost","root","123456","testdb")

cursor = db.cursor()

cursor.execute("SELECT VERSION()")

data = cursor.fetchone()

print(data)