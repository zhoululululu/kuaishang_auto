# -*- coding: UTF-8 -*-
'''
Created on 2020/7/16 14:26
@File  : get_answer.py
@author: ZL
@Desc  :
'''

from commonfunc.change_data_type import ChangeDataType
import os
import json
from tqdm import tqdm
import requests
import pandas as pd
import time

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetAnswer:
    @staticmethod
    def get_check_and_item():
        test_data = ChangeDataType.csv_to_dict(rootPath + "\\testdata\\knowledgegraph\\" + "check_simple.csv")
        item = test_data.item.tolist()
        check = test_data.check.tolist()
        return item, check

    @staticmethod
    def get_othertreatment_and_item():
        test_data = ChangeDataType.csv_to_dict(rootPath + "\\testdata\\knowledgegraph\\" + "othertreatment_simple.csv")
        item = test_data.item.tolist()
        othertreatment = test_data.check.tolist()
        return item, othertreatment

    @staticmethod
    def get_symptom_mapping():
        test_data = ChangeDataType.json_to_dict(rootPath + "\\testdata\\knowledgegraph\\" + "sy.json")
        sym_list = list(test_data.keys())
        item_list = list(test_data.values())
        return sym_list, item_list

    @staticmethod
    def get_item_mapping():
        test_data = ChangeDataType.json_to_dict(rootPath + "\\testdata\\knowledgegraph\\" + "item_mapping.json")
        item_list = list(test_data.keys())
        to_item_list = list(test_data.values())
        return item_list, to_item_list

    @staticmethod
    def get_cause_mapping():
        data = ChangeDataType.json_to_dict(rootPath + "\\testdata\\knowledgegraph\\" + "entity_mapping.json")
        test_data = data["PROBABLE_CAUSE"]
        to_cause_list = list(test_data.keys())
        cause_list = list(test_data.values())
        print()
        return to_cause_list, cause_list

    @staticmethod
    def get_all_item():
        test_data = ChangeDataType.json_to_dict(rootPath + "\\testdata\\knowledgegraph\\" + "all_item_knowledge.json")
        return test_data

    def get_normal_cause_answer(self):
        item_list, cause_list = GetAnswer.get_cause_and_item()
        answer_list, answer_item, answer_cause, cause_tf, item_tf, sentence_list = [], [], [], [], [], []
        for i in range(0, len(item_list)):
            sentence = "{}是怎么回事啊".format(item_list[i])
            response = requests.get(
                "http://192.168.120.37:8705/knowledge_graph/v1/answer?utterance={}&department=andrology&use_attr=1".format(
                    sentence))
            result = response.json()
            if result["code"] == 200:
                print(result)
                if len(result["data"]["answer"][0].split("可能")) > 1:
                    result_cause_list = result["data"]["answer"][0].split("可能")[0].split("、")
                else:
                    result_cause_list = result["data"]["answer"][0].split("可能")[0]
                item = result["data"]["answer"][0].split("引起")[1]
                if set(result_cause_list) <= set(cause_list[i]):
                    c_tf = "true"
                else:
                    c_tf = "false"
                if item == item_list[i]:
                    i_tf = "true"
                else:
                    i_tf = "false"
            sentence_list.append(sentence)
            answer_list.append(result["data"]["answer"][0])
            cause_tf.append(c_tf)
            item_tf.append(i_tf)
            answer_item.append(item)
            answer_cause.append(result_cause_list)
        result_data = pd.DataFrame(
            {"sentence": sentence_list, "cause": cause_list, "item": item_list, "answer": answer_list,
             "answer_cause": answer_cause, "answer_item": answer_item, "cause_tf": cause_tf, "item_tf": item_tf})

        now = time.strftime('%y_%m_%d-%H_%M_%S')
        result_data.to_excel(rootPath + '\\testresults\\resultfile\\' + now + "testresult_.xls")

    def get_request_sym_mapping(self):
        sym_list, item_list = GetAnswer.get_symptom_mapping()
        sentence_list, re_item_list, item_tf_list = [], [], []
        for i in range(0, len(sym_list)):
            sentence = "{}是怎么回事啊？".format(sym_list[i])
            response = requests.get(
                "http://192.168.26.105:32201/knowledge_graph/v1/answer?utterance={}&department=andrology&use_attr=1".format(
                    sentence))
            result = response.json()
            re_item = result["data"][""]
            if set(re_item) <= set(item_list[i]):
                item_tf = "true"
            else:
                item_tf = "false"
            sentence_list.append(sentence)
            re_item_list.append(re_item)
            item_tf_list.append(item_tf)

        result_data = pd.DataFrame(
            {"sentence": sentence_list, "sym_list": sym_list, "item_list": item_list, "re_item_list": re_item_list,
             "item_tf_list": item_tf_list})

        now = time.strftime('%y_%m_%d-%H_%M_%S')
        result_data.to_excel(rootPath + '\\testresults\\resultfile\\' + now + "sym_to_item_testresult.xls")

    def get_request_item_mapping(self):
        item_list, to_item_list = GetAnswer.get_item_mapping()
        m_item_list, cause_list = GetAnswer.get_cause2item_mapping2()
        all_item = GetAnswer.get_all_item()
        sentence_list, answer_list, re_item_list, re_cause_list, item_tf_list, cause_tf_list, item_label, cause_label = [], [], [], [], [], [], [], []
        for i in range(0, len(item_list)):
            if to_item_list[i] in m_item_list:
                cause = cause_list.__getitem__(m_item_list.index(to_item_list[i]))
            else:
                for j in range(len(all_item)):
                    print(all_item[j]["_fields"][0]["properties"]["name"])
                    if all_item[j]["_fields"][0]["properties"]["name"] == to_item_list[i]:
                        cause = all_item[j]["_fields"][0]["properties"]["cause"]
            sentence = "{}是怎么回事啊？".format(item_list[i])
            try:
                response = requests.get(
                    "http://192.168.120.37:8705/knowledge_graph/v1/answer?utterance={}&department=andrology&use_attr=1".format(
                        sentence))
                result = response.json()
                print(result)
                if result["code"] == 200:
                    re_answer = result["data"]["answer"]
                else:
                    re_answer = result["code"] + "error"

                if len(result["data"]["answer"][0].split("可能")) > 1:
                    result_cause_list = result["data"]["answer"][0].split("可能")[0].split("、")
                else:
                    result_cause_list = result["data"]["answer"][0].split("可能")[0]
                item = result["data"]["answer"][0].split("引起")[1]
                if set(result_cause_list) <= set(cause):
                    c_tf = "true"
                else:
                    c_tf = "false"
                if item == to_item_list[i]:
                    i_tf = "true"
                else:
                    i_tf = "false"
            except Exception:
                print(Exception)
            sentence_list.append(sentence)
            item_label.append(to_item_list[i])
            cause_label.append(cause)
            answer_list.append(re_answer)
            re_item_list.append(item)
            re_cause_list.append(result_cause_list)
            cause_tf_list.append(c_tf)
            item_tf_list.append(i_tf)
            result_cause_list = []
            cause = []

        result_data = pd.DataFrame(
            {"sentence": sentence_list, "item_label": item_label, "cause_label": cause_label,
             "answer_list": answer_list, "re_item_list": re_item_list, "re_cause_list": re_cause_list,
             "cause_tf_list": cause_tf_list, "item_tf_list": item_tf_list})
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        result_data.to_excel(rootPath + '\\testresults\\resultfile\\' + now + "sym_to_item_testresult.xls")

    def get_request_cause_mapping(self):

        to_cause_list, cause_list = GetAnswer.get_cause_mapping()
        cause_list, item_list = GetAnswer.get_cause2item_mapping()
        sentence_list, answer_list, re_answer_list, answer_tf_list = [], [], []

        for i in range(0, len(cause_list)):
            item = item_list[to_cause_list[i]]
            answer = "{}可能引起{}".format(to_cause_list[i], item)
            for j in range(0, len(cause_list[i])):
                sentence = "{}是因为{}吗".format(item, cause_list[i][j])
                response = requests.get(
                    "http://192.168.120.37:8705/knowledge_graph/v1/answer?utterance={}&department=andrology&use_attr=1".format(
                        sentence))
                result = response.json()
                re_answer = result["data"]["answer"]
                if re_answer == answer:
                    answer_tf = "true"
                else:
                    answer_tf = "false"
                sentence_list.append(sentence)
                answer_list.append(answer)
                re_answer_list.append(re_answer)
                answer_tf_list.append(answer_tf)

        result_data = pd.DataFrame(
            {"sentence": sentence_list, "re_answer_list": re_answer_list, "answer_tf_list": answer_tf_list})

        now = time.strftime('%y_%m_%d-%H_%M_%S')
        result_data.to_excel(rootPath + '\\testresults\\resultfile\\' + now + "cause_mapping_testresult.xls")


if __name__ == '__main__':
    GetAnswer().get_request_item_mapping()
