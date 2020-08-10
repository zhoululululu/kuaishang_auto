# -*- coding: UTF-8 -*-
'''
Created on 2020/7/24 14:39
@File  : nertest.py
@author: ZL
@Desc  :
'''
import requests
import codecs
import os
from commonfunc.change_data_type import ChangeDataType

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


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


def get_ner_testdata(file1, file2):
    # 更换tab为空格
    raw_data = codecs.open(rootPath + "\\testdata\\apidata\\" + file1, encoding='utf-8')
    result_data = codecs.open(rootPath + "\\testdata\\apidata\\" + file2, 'w', encoding='utf-8')
    for line in raw_data.readlines():
        if len(line.strip()) == 0:
            result_data.write(line.strip())
        line = line.replace("\t\t", " ")

        line = line.strip()
        if line == "O":
            line = "， O"
        if line.startswith("B_") or line.startswith("I_"):
            continue
        result_data.write(line.strip() + "\n")


def get_target(ner_test_file):
    raw_data = ChangeDataType().file_to_dict(rootPath + "\\testdata\\apidata\\" + ner_test_file)
    target ,new_target= [],[]
    for i in raw_data:
        if len(i.strip()) != 0:
            target.append(i.strip().split(" ")[1])
    # print(target)

    set_target = set(target)
    #print(set_target)
    for j in set_target:
        if j.startswith("B_"):
            new_target.append(j)
            print(j)



get_target("ner\\andrology\\new_test_andrology_bio.txt")
# get_ner_testdata("ner\\andrology\\test_andrology_bio.txt", "ner\\andrology\\new_test_andrology_bio.txt")
