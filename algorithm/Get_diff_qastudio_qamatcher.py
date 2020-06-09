# -*- coding: UTF-8 -*-
'''
Created on 2020/5/12
@File  : Get_diff_qastudio_qamatcher.py
@author: ZL
@Desc  :
'''

import requests


class GetDiff:

    def get_qamatcher_result(self, sentence):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
        }
        data = {
            "org": "kst",
            "app": "marketing_robot",
            "industry": "psoriasis",
            "kb_names": "psoriasis",
            "question": sentence
        }
        r = requests.post("http://192.168.1.18:32087/qastudio/v2/qamatch", data=data, headers=headers, timeout=50)
        print(r)
        result = r.json()
        print(result)
        question_list = result["question_list"]  # 获取返回question_list
        print(question_list)
        return question_list

    def get_qastudio_result(self, sentence):
        r = requests.get("http://192.168.1.18:30010/faqdiy/v1/sim_questions", timeout=50)
        result = r.json()
        question_list = result["question_list"]  # 获取返回data的intent
        return question_list

    def get_result_excel(self, sentence):
        question_list1 = GetDiff.get_qamatcher_result(self, sentence)
        # question_list2 = GetDiff.get_qastudio_result(sentence)


test = GetDiff()
test.get_qamatcher_result("掌趾脓疱病好治吗")
