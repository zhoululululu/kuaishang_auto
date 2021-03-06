# -*- coding: UTF-8 -*-
'''
Created on 2020/7/22 9:34
@File  : get_test.py
@author: ZL
@Desc  :
'''

import os
import requests
from commonfunc.change_data_type import ChangeDataType
from commonfunc.common_function import CommonFunction
import codecs

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]

import pandas


class GetTest:

    def get_test(self):
        test_data = ChangeDataType.csv_to_dict(
            rootPath + "\\testdata\\apidata\\intent\\" + "andrology\\andrology_intent.csv")
        test = test_data.sentence.tolist()
        for i in test:
            print('"' + i + '",')

    def get_accuracy(self, file):
        tf1_list, tf2_list = [], []

        test_data = ChangeDataType.excel_to_dict(
            rootPath + "\\testresults\\resultfile\\" + file,
            "Sheet1")
        label_list = test_data.label.tolist()
        re_label1_list = test_data.re_intent1.tolist()
        re_label2_list = test_data.re_intent2.tolist()

        for i in range(len(label_list)):
            tf1 = CommonFunction.get_tf(label_list[i], re_label1_list[i])
            tf2 = CommonFunction.get_tf(label_list[i], re_label2_list[i])
            tf1_list.append(tf1)
            tf2_list.append(tf2)

        print("------------------------predict1------------------------")
        print("总数：", len(tf1_list), "，一致数：", tf1_list.count("TRUE"), "，不一致数：", tf1_list.count("FALSE"), "，一致率：",
              "{:.2f}%".format(tf1_list.count("TRUE") / len(tf1_list) * 100), "，不一致率：",
              "{:.2f}%".format(tf1_list.count("FALSE") / len(tf1_list) * 100))

        print("------------------------predict2------------------------")
        print("总数：", len(tf2_list), "，一致数：", tf2_list.count("TRUE"), "，不一致数：", tf2_list.count("FALSE"), "，一致率：",
              "{:.2f}%".format(tf2_list.count("TRUE") / len(tf2_list) * 100), "，不一致率：",
              "{:.2f}%".format(tf2_list.count("FALSE") / len(tf2_list) * 100))

    def get_es(self):
        params = {
            "org": "kst",
            "app": "marketing_robot",
            "industry": "andrology",
            "kb_names": ["测试环境医美模板1_andrology_114"],
            "question": "是尿不尽是吧睡觉用手碰了下尿道口有湿湿的湿润的潮湿的"
        }
        requests.post(url="http://192.168.1.79:8086/qastudio/v2/qamatch", params=params)

    def get_resume_ner(self, file2):
        test_data = ChangeDataType.file_to_dict(rootPath + "\\testdata\\apidata\\ner\\andrology\\0827test_nanke.csv")
        result_data = codecs.open(rootPath + "\\testdata\\apidata\\ner\\andrology\\" + file2, 'w', encoding='utf-8')
        sentence = test_data["句子"]
        label = test_data["标签"]
        for i in range(len(sentence)):
            for j in range(len(sentence[i])):
                result_data.write(sentence[i][j] + " " + label[i].split(" ")[j] + "\n")
            result_data.write("\n")

    def get_ner_stander(self):
        test_data = ChangeDataType.file_to_dict(rootPath + "\\testdata\\apidata\\ner\\andrology\\0827test_nanke.csv")
        sentence = test_data["句子"]
        label = test_data["标签"]
        for i in range(len(sentence)):
            if len(sentence[i]) != len(label[i].split(" ")):
                print(sentence[i])

    def get_round(self):
        print(round(1.5))
        print(round(2.5))
        print(round(3.5))
        print(round(4.5))
if __name__ == '__main__':
    # GetTest().get_accuracy("20_07_24-18_59_38infertility_intention_test1.xls")
    # GetTest().get_resume_ner("new_ner_bio.txt")
    # GetTest().get_ner_stander()

    GetTest().get_round()
