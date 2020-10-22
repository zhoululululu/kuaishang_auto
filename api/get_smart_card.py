# -*- coding: UTF-8 -*-
'''
Created on 2020/10/20 13:53
@File  : get_smart_card.py
@author: ZL
@Desc  :
'''
import requests
import json
import random
from commonfunc.change_data_type import ChangeDataType
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class SmartCard:

    def get_smartcard(self, url):
        grade_list, course_list, stdent_source_list, error_stdent_course = [], [], [], []
        courses = ChangeDataType.file_to_dict(rootPath + "\\testdata\\apidata\\smartcard\\course_kws.txt")
        for course in courses:
            # id = random.choice(["32092519941128005","350128199306235412"])
            id = random.randint(32092519941128, 390128199306235412)
            grade = random.randint(100, 999)
            stdent_source = random.choice(["初一", "初二", "初三", "高一", "高二", "高三"])
            print(id)
            params = {
                "session_id": "5488745",
                "enterprise_id": "7356182",
                "data": [
                    {
                        "sentence_id": "0",
                        "content": "我身份证是{}".format(id),
                        "role": "visitor"
                    },
                    {
                        "sentence_id": "1",
                        "content": "亲 我们是一条龙服务，代办过户的",
                        "role": "customer"
                    },
                    {
                        "sentence_id": "2",
                        "content": "亲，您提供一下联系方式，我这边打给您",
                        "role": "customer"
                    },
                    {
                        "sentence_id": "3",
                        "content": "宁德",
                        "role": "visitor"
                    },
                    {
                        "sentence_id": "4",
                        "content": "怎么称呼",
                        "role": "customer"
                    },
                    {
                        "sentence_id": "5",
                        "content": "我姓张",
                        "role": "visitor"
                    },
                    {
                        "sentence_id": "6",
                        "content": "今年多大了",
                        "role": "customer"
                    },
                    {
                        "sentence_id": "7",
                        "content": "50",
                        "role": "visitor"
                    },
                    {
                        "sentence_id": "8",
                        "content": "亲，方便提供一下么",
                        "role": "customer"
                    },
                    {
                        "sentence_id": "9",
                        "content": "13162826882",
                        "role": "visitor"
                    },
                    {
                        "sentence_id": "10",
                        "content": course,
                        "role": "visitor"
                    },
                    {
                        "sentence_id": "11",
                        "content": "我现在{}年".format(stdent_source),
                        "role": "visitor"
                    },
                    {
                        "sentence_id": "12",
                        "content": "我考了{}分".format(grade),
                        "role": "visitor"
                    }
                ],
                "department": "beauty"
            }
            result = requests.post(url=url, data=json.dumps(params))
            data = result.json()

            print(result.json())
            re_grade = data["data"]["grade"]
            re_stdent_source = data["data"]["student_source"]
            re_course = data["data"]["course"]
            if re_grade != str(grade) or re_stdent_source != stdent_source or re_course != course:
                print(params)
                error_stdent_course.append(course)
            # print(grade, re_grade, stdent_source, re_stdent_source, course, re_course)
        grade_list.append(re_grade == str(grade))
        stdent_source_list.append(re_stdent_source == stdent_source)
        course_list.append(re_course == course)

        print(set(grade_list), set(stdent_source_list), set(course_list))
        print(error_stdent_course)
    # def test11(self):
    #     test = {'code': 200,
    #      'data': {'name': '张', 'age': 50, 'gender': '', 'qq': '', 'wechat': '', 'mobile': '13162826882', 'item': [],
    #               'identity_card': '32092519941128005', 'course': '', 'address': '武汉', 'stdent_source': '初三',
    #               'grade': '237'}, 'error': ''}
    #
    #     print(test["grade"])


if __name__ == '__main__':
    url = "http://192.168.26.105:30304/smart_card/v1"
    SmartCard().get_smartcard(url)
    # SmartCard().test11()
