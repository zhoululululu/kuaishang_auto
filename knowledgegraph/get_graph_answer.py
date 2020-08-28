# -*- coding: UTF-8 -*-
'''
Created on 2020/8/18 15:14
@File  : get_graph_answer.py
@author: ZL
@Desc  :
'''

from knowledgegraph.get_test_data import GetTestData
import requests
import os
import pandas as pd
import time
import random
from knowledgegraph.neo4j_connect import Neo4jConnect

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetGraphAnswer:

    # url:http://192.168.120.37:8705/knowledge_graph/v1/answer?utterance={}&department=andrology&use_attr=1
    def get_cause_answer_mapping(self, api_url, result_file):
        '''
        :param api_url: url
        :param result_file: 生成的文件
        :return: None
        主要是正向问题的回答：关系库+item属性,单纯的咨询病因，sentence中未提及病因
        '''
        sentence_list, item_list, answer_list, item_cause_list, cause_tf_list, re_item_list, answer_type_list, knowledge_item_list = [], [], [], [], [], [], [], []
        item_info_list = {}
        test_data = GetTestData.get_cause_and_item()
        item_list = list(test_data.keys())
        cause_list = list(test_data.values())
        all_item_info_list = GetTestData.get_all_item_info()
        for i in all_item_info_list:
            # print(i["_fields"][0]["properties"].get("咨询病因"))
            item_info_list[i["_fields"][0]["properties"]["name"]] = i["_fields"][0]["properties"].get("咨询病因")[0]
        all_item_list = item_list + list(set(item_info_list.keys()) - set(item_list))
        for i in range(0, len(all_item_list)):
            time.sleep(5)
            sentence = "{}是怎么回事啊".format(all_item_list[i])
            params = {
                "utterance": sentence,
                "department": "andrology",
                "use_attr": 1
            }
            try:
                response = requests.get(url=api_url, params=params)
                result = response.json()
                answer = result["data"]["answer"]
                answer_type = result["data"]["answer_type"]
                print(answer)
                if "可能" in str(answer):
                    if len(result["data"]["answer"][0].split("可能")) > 1:
                        result_cause_list = result["data"]["answer"][0].split("可能")[0].split("、")
                    else:
                        result_cause_list = result["data"]["answer"][0].split("可能")[0]
                    item = result["data"]["answer"][0].split("引起")[1]
                    if set(result_cause_list) <= set(cause_list[i]):
                        c_tf = "true"
                    else:
                        c_tf = "false"
                else:
                    result_cause = result["data"]["answer"][0]
                    item = all_item_list[i]
                    cause_list.append(item_info_list[all_item_list[i]])
                    if item_info_list[all_item_list[i]] == result_cause:
                        c_tf = "true"
                    else:
                        c_tf = "false"
            except Exception as e:
                print(item)
                item = "bad case"
                answer = "bad case"
                c_tf = "bad case"
                answer_type = "bad case"
            sentence_list.append(sentence)
            re_item_list.append(item)
            answer_list.append(answer)
            answer_type_list.append(answer_type)
            cause_tf_list.append(c_tf)
            # print(len(all_item_list), len(cause_list), len(sentence_list), len(re_item_list), len(answer_list),
            #       len(answer_type_list), len(cause_tf_list))
        result_data = pd.DataFrame(
            {"项目": all_item_list, "项目定义病因": cause_list, "句子参数": sentence_list, "接口返回项目": re_item_list,
             "接口返回答案类型": answer_type_list,
             "接口返回答案": answer_list,
             "接口返回答案是否在项目定义病因中": cause_tf_list})
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        result_data.to_excel(
            rootPath + '\\testresults\\resultfile\\knowledgegraph\\' + now + result_file)

    def get_cause_mix(self, api_url, result_file):
        '''
        :param api_url: url
        :param result_file: 生成的文件
        :return: None
        根据输入句子的病因，进行正反面的问题回答：可能引起或者不能引起
        '''
        sentence_list, item_list, answer_list, item_cause_list, cause_tf_list, re_item_list, answer_type_list, knowledge_item_list = [], [], [], [], [], [], [], []
        item_info_list = {}
        test_data = GetTestData.get_cause_and_item()
        item_list = list(test_data.keys())
        cause_list = list(test_data.values())
        item_cause_list = list(test_data.values())
        all_item_info_list = GetTestData.get_all_item_info()
        for i in all_item_info_list:
            item_info_list[i["_fields"][0]["properties"]["name"]] = i["_fields"][0]["properties"].get("咨询病因")[0]
        all_item_list = item_list + list(set(item_info_list.keys()) - set(item_list))
        for i in range(0, len(all_item_list)):
            cause1 = random.choice(random.choice(cause_list))
            cause2 = random.choice(random.choice(cause_list))
            time.sleep(5)
            sentence = "{}是因为{}和{}引起的吗".format(all_item_list[i], cause1, cause2)
            params = {
                "utterance": sentence,
                "department": "andrology",
                "use_attr": 1
            }
            try:
                response = requests.get(url=api_url, params=params)
                result = response.json()
                answer = result["data"]["answer"]
                answer_type = result["data"]["answer_type"]
                if all_item_list[i] not in item_list:
                    item_cause = item_info_list[all_item_list[i]]
                    item_cause_list.append(item_cause)
                else:
                    item_cause = cause_list[i]
                if result["code"] == 200:
                    if len(answer) == 1:
                        if "可能" in str(answer):
                            result_cause_list = result["data"]["answer"][0].split("可能")[0].split("、")
                            item = result["data"]["answer"][0].split("引起")[1]
                            if set(result_cause_list) <= set(item_cause):
                                c_tf = "true"
                            else:
                                c_tf = "false"
                        elif "不能" in str(answer):
                            result_cause_list = result["data"]["answer"][0].split("不能")[0].split("和")
                            item = result["data"]["answer"][0].split("引起")[1]
                            if set(result_cause_list) not in set(item_cause):
                                c_tf = "true"
                            else:
                                c_tf = "false"
                        else:
                            result_cause = result["data"]["answer"][0]
                            item = all_item_list[i]
                            item_cause_list.append(item_info_list[all_item_list[i]])
                            if item_info_list[all_item_list[i]] == result_cause:
                                c_tf = "true"
                            else:
                                c_tf = "false"
                    else:
                        tf_all, item_all = [], []
                        for i in answer:
                            if "可能" in i:
                                result_cause_list = i.split("可能")[0].split("、")
                                item = i.split("引起")[1]
                                if set(result_cause_list) <= set(item_cause):
                                    tf = "true"
                                else:
                                    tf = "false"
                            if "不能" in i:
                                result_cause_list = i.split("不能")[0].split("、")
                                item = i.split("引起")[1]
                                if set(result_cause_list) not in set(item_cause):
                                    tf = "true"
                                else:
                                    tf = "false"
                            tf_all.append(tf)
                            item_all.append(item)
                        c_tf = "true" if set(tf_all) == {"true"} else "false"
                else:
                    item = "bad case"
                    c_tf = "bad case"
                print(answer, c_tf)
            except Exception as e:
                print(e)
            sentence_list.append(sentence)
            re_item_list.append(item)
            answer_list.append(answer)
            answer_type_list.append(answer_type)
            cause_tf_list.append(c_tf)
        result_data = pd.DataFrame(
            {"项目": all_item_list, "项目定义病因": item_cause_list, "句子参数": sentence_list, "接口返回项目": re_item_list,
             "接口返回答案类型": answer_type_list,
             "接口返回答案": answer_list,
             "接口返回答案是否在项目定义病因中": cause_tf_list})
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        result_data.to_excel(
            rootPath + '\\testresults\\resultfile\\knowledgegraph\\' + now + result_file)

    def get_cause_yes_or_no(self, api_url, result_file):
        '''
        :param api_url: url
        :param result_file: 生成的文件
        :return: None
        根据输入句子的病因，进行正反面的问题回答：可能引起或者不能引起
        '''
        sentence_list, item_list, answer_list, item_cause_list, cause_tf_list, re_item_list, answer_type_list, knowledge_item_list = [], [], [], [], [], [], [], []
        item_info_list = {}
        test_data = GetTestData.get_cause_and_item()
        item_list = list(test_data.keys())
        cause_list = list(test_data.values())
        item_cause_list = list(test_data.values())
        all_item_info_list = GetTestData.get_all_item_info()
        for i in all_item_info_list:
            item_info_list[i["_fields"][0]["properties"]["name"]] = i["_fields"][0]["properties"].get("咨询病因")[0]
        all_item_list = item_list + list(set(item_info_list.keys()) - set(item_list))
        for i in range(0, len(all_item_list)):
            cause = random.choice(random.choice(cause_list))
            time.sleep(5)
            sentence = "{}是因为{}引起的吗".format(all_item_list[i], cause)
            params = {
                "utterance": sentence,
                "department": "andrology",
                "use_attr": 1
            }
            try:
                response = requests.get(url=api_url, params=params)
                result = response.json()
                answer = result["data"]["answer"]
                answer_type = result["data"]["answer_type"]
                if result["code"] == 200:
                    if all_item_list[i] not in item_list:
                        print(i, sentence, item_info_list[all_item_list[i]])
                        item_cause = item_info_list[all_item_list[i]]
                        item_cause_list.append(item_cause)
                    else:
                        item_cause = cause_list[i]
                    if "可能" in str(answer):
                        result_cause_list = result["data"]["answer"][0]
                        item = result["data"]["answer"][0].split("引起")[1]
                        if set(result_cause_list) & set(item_cause) != None:
                            c_tf = "true"
                        else:
                            c_tf = "false"
                    if "不能" in str(answer):
                        result_cause_list = result["data"]["answer"][0].split("不能")[0]
                        item = result["data"]["answer"][0].split("引起")[1]
                        if set(result_cause_list) not in set(item_cause):
                            c_tf = "true"
                        else:
                            c_tf = "false"
                else:
                    item = "bad case"
                    c_tf = "bad case"
            except Exception as e:
                print(e)
            print(answer, c_tf)
            sentence_list.append(sentence)
            re_item_list.append(item)
            answer_list.append(answer)
            answer_type_list.append(answer_type)
            cause_tf_list.append(c_tf)
        result_data = pd.DataFrame(
            {"项目": all_item_list, "项目定义病因": item_cause_list, "句子参数": sentence_list, "接口返回项目": re_item_list,
             "接口返回答案类型": answer_type_list,
             "接口返回答案": answer_list,
             "接口返回答案是否在项目定义病因中": cause_tf_list})
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        result_data.to_excel(
            rootPath + '\\testresults\\resultfile\\knowledgegraph\\' + now + result_file)

    def get_double_item_answer_mapping(self, api_url, result_file):
        '''
        :param api_url: url
        :param result_file: 生成的文件
        :return: None
        主要是正向问题的回答：关系库+item属性,单纯的咨询病因，sentence中未提及病因
        '''
        sentence_list, item_list, answer_list, item_cause_list, cause_tf_list, re_item_list, answer_type_list, knowledge_item_list = [], [], [], [], [], [], [], []
        item_info_list = {}
        test_data = GetTestData.get_cause_and_item()
        item_list = list(test_data.keys())
        cause_list = list(test_data.values())
        all_item_info_list = GetTestData.get_all_item_info()
        for i in all_item_info_list:
            # print(i["_fields"][0]["properties"].get("咨询病因"))
            item_info_list[i["_fields"][0]["properties"]["name"]] = i["_fields"][0]["properties"].get("咨询病因")[0]
        all_item_list = item_list + list(set(item_info_list.keys()) - set(item_list))
        for i in range(0, len(all_item_list)):
            time.sleep(5)
            sentence = "{}，{}是怎么回事啊".format(random.choice(all_item_list[i]), random.choice(all_item_list[i]))
            params = {
                "utterance": sentence,
                "department": "andrology",
                "use_attr": 1
            }
            try:
                response = requests.get(url=api_url, params=params)
                result = response.json()
                answer = result["data"]["answer"]
                answer_type = result["data"]["answer_type"]
                tf_all, item = [], []
                for i in answer:
                    print(i)
                    if "可能" in i:
                        if len(i.split("可能")) > 1:
                            result_cause_list = i.split("、")
                        else:
                            result_cause_list = i.split("可能")[0]
                        item = i.split("引起")[1]
                        if set(result_cause_list) <= set(cause_list[i]):
                            c_tf = "true"
                        else:
                            c_tf = "false"
                    else:
                        result_cause = i
                        item = all_item_list[i]
                        cause_list.append(item_info_list[all_item_list[i]])
                        if item_info_list[all_item_list[i]] == result_cause:
                            c_tf = "true"
                        else:
                            c_tf = "false"
            except Exception as e:
                print(item)
                item = "bad case"
                answer = "bad case"
                c_tf = "bad case"
                answer_type = "bad case"
            sentence_list.append(sentence)
            re_item_list.append(item)
            answer_list.append(answer)
            answer_type_list.append(answer_type)
            cause_tf_list.append(c_tf)
            # print(len(all_item_list), len(cause_list), len(sentence_list), len(re_item_list), len(answer_list),
            #       len(answer_type_list), len(cause_tf_list))
        result_data = pd.DataFrame(
            {"项目": all_item_list, "项目定义病因": cause_list, "句子参数": sentence_list, "接口返回项目": re_item_list,
             "接口返回答案类型": answer_type_list,
             "接口返回答案": answer_list,
             "接口返回答案是否在项目定义病因中": cause_tf_list})
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        result_data.to_excel(
            rootPath + '\\testresults\\resultfile\\knowledgegraph\\' + now + result_file)

    def get_check_answer_match(self, api_url, result_file):
        '''
        :param api_url: url
        :param result_file: 生成的文件
        :return: None
        主要是正向问题的回答：关系库+item属性,单纯的咨询病因，sentence中未提及病因,包含单+多个item的check
        '''
        testdata = Neo4jConnect().get_match(
            'MATCH (i:Item{flag:"andrology_v1"})-[r:NEED_TO_CHECK]->(c:Check{flag:"andrology_v1"})'
            "RETURN i.name as item,c.name as check")
        item_check, item, check = {}, [], []
        print(testdata)
        for i in testdata:  # 第一层for循环，获取各个元素（即各个不同的字典）
            print(i.items())
            for key, value in i.items():  # 在第一层for循环得到的“字典”情况下，对各个“字典”进行第二层for循环，通过items获取到每个“字典“的key和value
                print(key, value)
                item_check[key] = value
                item.append(key)
                check.append(value)
        print(item_check)
        print(item)
        print(check)


if __name__ == '__main__':
    GetGraphAnswer().get_check_answer_match("http://192.168.26.105:30201/knowledge_graph/v1/answer",
                                            "cause_yes_or_no_result.xls")
# GetGraphAnswer().get_cause_answer_mapping("http://192.168.26.105:30201/knowledge_graph/v1/answer",
#                                           "cause_answer_mapping_result.xls")
# GetGraphAnswer().get_cause_mix("http://192.168.26.105:30201/knowledge_graph/v1/answer",
#                                "cause_mix_result.xls")
