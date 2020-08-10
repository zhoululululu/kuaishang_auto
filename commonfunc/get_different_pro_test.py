# -*- coding: UTF-8 -*-
'''
Created on 2020/8/7 16:47
@File  : get_different_pro_test.py
@author: ZL
@Desc  :
'''

import time
import requests
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class DifferentProTest:
    def get_all_clinet_id_test(self, pro_url, sentence_list):
        test_result_list = []
        headers = {
            'Authorization': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb21wYW55X2lkIjoxMjksInJvYm90X2lkIjoxMjksImV4cCI6MTU5NzM5ODgyMn0.9vLFaAt8wyxRVxM-wqlO0yx4azjrVBrFErdwmuhGDT8",
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        start_time1 = time.time()
        for sentence in sentence_list:
            params = {
                'dialog': sentence,
                'client_id': "zltest111",
            }

            try:
                r = requests.post(pro_url, params=params, headers=headers, timeout=50)
                result = r.json()
                re_intent = result["data"]["ner"]["intent"]["Value"][0]["Value"]  # 获取返回data的intent
                test_result_list.append(re_intent)

            except Exception as e:
                print(e)
        end_time1 = time.time()
        print(test_result_list)
        print("time_cost", end_time1 - start_time1)

    def get_diff_clinet_id_test(self, pro_url, sentence_list):
        test2_result_list = []
        headers = {
            'Authorization': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb21wYW55X2lkIjoxMjksInJvYm90X2lkIjoxMjksImV4cCI6MTU5NzM5ODgyMn0.9vLFaAt8wyxRVxM-wqlO0yx4azjrVBrFErdwmuhGDT8",
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        start_time2 = time.time()
        for sentence in sentence_list:
            now = time.time()
            params = {
                'dialog': sentence,
                'client_id': "zltest" + str(now),
            }
            try:
                r = requests.post(pro_url, params=params, headers=headers, timeout=50)
                result = r.json()
                re_intent = result["data"]["ner"]["intent"]["Value"][0]["Value"]  # 获取返回data的intent
                test2_result_list.append(re_intent)

            except Exception as e:
                print(e)
        end_time2 = time.time()
        print(test2_result_list)
        print("time_cost", end_time2 - start_time2)


if __name__ == '__main__':
    pro_url = "http://robotchat.kuaishangkf.com/x/identify/v1/re_unify/identify"
    sentence_list1 = ['这病能断根吗', '你们医院有比较厉害的专家吗？', '你们医院厉害的主任有吗？', '有专业的医生吗？', '你们医资力量怎么样？', '你们医院会有比较专业的主任吗？',
                      '有专业的医师吗',
                      '吃什么药好的快',
                      '那我应该吃什么药', '你们医院一般都开什么药', '吃那些药比较好', '可以帮我开点药吗', '有什么特效药吗', '我想通过药物治疗', '你们医院用什么药', '请问是专家号吗？',
                      '有妇产科的专家吗',
                      '材料有哪些', '用料有哪些', '你们医院采用的是什么材料']
    DifferentProTest().get_all_clinet_id_test(pro_url, sentence_list1)
    DifferentProTest().get_diff_clinet_id_test(pro_url, sentence_list1)
    DifferentProTest().get_all_clinet_id_test(pro_url, sentence_list1)
    DifferentProTest().get_diff_clinet_id_test(pro_url, sentence_list1)
