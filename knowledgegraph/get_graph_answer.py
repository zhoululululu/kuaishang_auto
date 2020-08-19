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

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetGraphAnswer:

    # url:http://192.168.120.37:8705/knowledge_graph/v1/answer?utterance={}&department=andrology&use_attr=1
    def get_cause_answer_mapping(self, api_url, result_file):
        sentence_list, item_list, answer_list, item_cause_list, cause_tf_list, re_item_list, answer_type_list, knowledge_item_list = [], [], [], [], [], [], [], []
        test_data = GetTestData.get_cause_and_item()
        all_item_list = list(test_data.keys())
        cause_list = list(test_data.values())
        # all_item_info_list = GetTestData.get_all_item_info()
        # for i in all_item_info_list:
        #     knowledge_item_list.append(i["_fields"][0]["properties"]["name"])
        #     item_cause_list.append(i["_fields"][0]["properties"]["cause"])
        # all_item_list = item_list + list(set(knowledge_item_list) - set(item_list))
        for i in range(0, len(all_item_list)):
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
                print(answer)
                answer_type = result["data"]["answer_type"]
                if result["code"] == 200:
                    if "可能" in answer:
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
                        if item_cause_list == result_cause:
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
        result_data = pd.DataFrame(
            {"项目": item_list, "项目定义病因": cause_list, "句子参数": sentence_list, "接口返回项目": re_item_list,
             "接口返回答案类型": answer_type_list,
             "接口返回答案": answer_list,
             "接口返回答案是否在项目定义病因中": cause_tf_list})
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        result_data.to_excel(
            rootPath + '\\testresults\\resultfile\\knowledgegraph\\' + now + result_file)


if __name__ == '__main__':
    GetGraphAnswer().get_cause_answer_mapping("http://192.168.26.105:32201/knowledge_graph/v1/answer",
                                              "cause_answer_mapping_result.xls")
