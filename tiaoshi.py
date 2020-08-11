# !/usr/bin/python3
# _*_ coding:utf-8 _*_
# Author : william - xwj
# Github: https://githun.com/
# CreatDate : 2020/7/28-11:45
# Description : PyCharm
# 项目名称：Python+selenium+unittest
# 当前用户/文件名： Administrator /tiaoshi
import os,sys
# path = os.path._get_bothseps(__file__)
# print(path)
import requests

url = r"https://test-api.cityocean.com:10001/sso/connect/token?timestamp=1594032384000"

payload = {'scope': 'PlatformApi offline_access ids4-api',
'client_id': 'cityOcean',
'client_secret': '282F4E3E-AD56-4FE1-BAF3-FE99BBC11AD2',
'grant_type': 'password',
'username': '630615293@qq.com',
'password': 'co123456'}
files = [

]
headers = {
  'Accept': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)
res = response.content.decode()
res1 = response.text.encode('utf8')
res2 = response.request
res3 = response.status_code
res4 = response.json()
res5 = response.apparent_encoding
res6 = response.headers
res7 = response.json()['access_token']
print(type(res))
print(res)
print("--"*30)
print(type(res1))
print(res1)
print("--"*30)
print(type(res2))
print(res2)
print("--"*30)
print(type(res3))
print(res3)
print("--"*30)
print(type(res4))
print(res4)
print("--"*30)
print(type(res5))
print(res5)
print("--"*30)
print(type(res6))
print(res6)
print("--"*30)
print(type(res7))
print(res7)
print("--"*30)


