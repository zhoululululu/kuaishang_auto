# -*- coding: UTF-8 -*-
'''
Created on 2020/7/24 14:39
@File  : nertest.py
@author: ZL
@Desc  :
'''
import requests


def get_ner_result(sentence):
    url = 'http://192.168.1.74:8062/ner/v1?model_name=gynaecology&utterance={}'.format(sentence)
    try:
        res = requests.get(url).json()
        if res['code'] == 200:
            return res['data']["bio"]
        return {}
    except Exception as e:
        print(e)
        return {}


def get_ner_result2(sentence):
    url = 'http://192.168.1.74:8062/ner/v1'
    params = {
        'model_name': 'gynaecology',
        'utterance': sentence
    }
    try:
        res = requests.get(url, params=params).json()
        if res['code'] == 200:
            return res['data']["bio"]
        return {}
    except Exception as e:
        print(e)
        return {}


print(get_ner_result("25，怀孕16+4"))
print(get_ner_result2("关于"))
