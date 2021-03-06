# -*- coding: UTF-8 -*-
'''
Created on 2020/5/12
@File  : get_diff_qastudio_qamatcher.py
@author: ZL
@Desc  : 临时测试文件：测试qamatcher与qastudio的效果
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
            "industry": "gynaecology",
            "kb_names": ["gynaecology"],
            "question": sentence
        }
        r = requests.post("http://192.168.26.105:30086/qastudio/v2/qamatch", data=data, timeout=50)
        result = r.json()
        print(result)
        return result

    def get_qastudio_result(self, sentence):
        r = requests.get("http://192.168.1.18:30010/faqdiy/v1/sim_questions", timeout=50)
        result = r.json()
        question_list = result["question_list"]  # 获取返回data的intent
        return question_list

    def get_result_excel(self, sentence):
        question_list1 = GetDiff.get_qamatcher_result(self, sentence)
        question_list2 = GetDiff.get_qastudio_result(sentence)
        print(question_list1, question_list2)


if __name__ == '__main__':
    test = GetDiff()
    test.get_qamatcher_result("熬夜会导致月经推迟")
