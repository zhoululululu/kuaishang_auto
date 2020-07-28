# -*- coding: UTF-8 -*-
'''
Created on 2020/6/19 10:38
@File  : get_zp_test.py
@author: ZL
@Desc  :
'''

from requests_toolbelt import MultipartEncoder
import requests

data = MultipartEncoder(
    fields=[
        ("industry_id", "7"),
        ("template_id", "6"),
        ("method", "rule.upload"),
        ("file", ("医美话术通用总后台模板v1.8.xlsx", open("D:\\医美话术通用总后台模板v1.8.xlsx", "rb"), "application/octet-stream"))
    ])


header = {
    "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb21wYW55X2lkIjoyMzksInJvYm90X2lkIjo2MTIsImV4cCI6MTU5MzA3NTY5NH0.TxRcRkUYusW66kKMB170YZbVAbBAKd6E04dazbB05hA",
    "Content-Type": data.content_type,
}

url = "http://192.168.1.16:11000/x/tools/v1/template/batch_import"
response = requests.post(url, data=data, headers=header)
json = response.json()
print(json)
