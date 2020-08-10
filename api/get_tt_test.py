# -*- coding: UTF-8 -*-
'''
Created on 2020/6/19 10:38
@File  : get_zp_test.py
@author: ZL
@Desc  :
'''

from requests_toolbelt import MultipartEncoder, multipart
import requests
from urllib import parse
import json
import requests


def get_test():
    params = {
        'utterance': "恩，我加您QQ您好，”有什么问题可以帮您的“，请讲！（网页咨询患者较多，您电话/微信多少？一对一分析和解答）",
        'model_name': "andrology"
    }
    result = requests.get(url="http://192.168.1.74:8062/ner/v1", params=params)
    ner = result.json()["data"]["bio"]
    print(len("恩，我加您QQ您好，“有什么问题可以帮您的”，请讲！（网页咨询患者较多，您电话/微信多少？一对一分析和解答）"))
    print(ner)
    print(len(ner))


get_test()
