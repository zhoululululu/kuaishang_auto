# -*- coding: UTF-8 -*-
'''
Created on 2020/2/26
@File  : change_data_type.py
@author: ZL
@Desc  :
'''

import json
import pandas
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class ChangeDataType:

    @staticmethod
    def file_to_dict(path, sheet_name=None):
        test_data = []
        form = str(path).split(".")[-1]
        try:
            if form == "txt":
                f = open(path, "r", encoding="UTF-8")
                for line in f.readlines():
                    test_data.append(line.strip("\n"))

            elif form == "csv":
                test_data = pandas.read_csv(path, encoding="utf-8")

            elif form == "xls" or form == "xlsx":
                test_data = pandas.read_excel(path, sheet_name=sheet_name, encoding="utf-8")
                return test_data

            elif form == "json":
                with open(path, mode='r', encoding='utf-8') as f2:
                    test_data = json.load(f2)

        except Exception as e:
            print(e)
        return test_data

    @staticmethod
    def json_to_dict(path):
        """
        将数据由json转为dict
        :param path: 需要转换的json文件
        :return test_data：已转为dict的数据结果
        """
        with open(path, mode='r', encoding='utf-8') as f2:
            test_data = json.load(f2)
            return test_data

    @staticmethod
    def excel_to_dict(file_name, sheet_name):
        """
        将数据由excel文件转换为dict
        :param file_name: 需要转换的excel
        :param sheet_name: sheet名称
        :return test_data: 转换后的dict字符串
        """
        test_data = pandas.read_excel(file_name, sheet_name=sheet_name, encoding="utf-8")
        return test_data

    @staticmethod
    def dict_to_jsonfile(dict_data, file_name):
        """
        将数据由dict转换为json文件
        :param dict_data: 需要转换的dict数据
        :param file_name: 转换后的json文件
        """
        with open(file_name, 'w') as f:
            # 设置不转换成ascii  json字符串首缩进
            f.write(json.dumps(dict_data, ensure_ascii=False, indent=2))

    @staticmethod
    def dict_to_json(dict_data):
        """
        将数据由dict转换为json字符串
        :param dict_data: 需要转换的dict数据
        :return str_json: 转换后的json字符串
        """
        str_json = json.dumps(dict_data)
        return str_json

    @staticmethod
    def ner_csv_to_dict(file):
        """
        将csv转换为dict（专为妇科ner而立，特殊处理exp_bio，re_bio）
        :param file: 需要转换的dict数据文件（此处应该为ner文件）
        :return exp_bio_list: 转换为dict的预期bio值list
        :return re_bio_list: 转换为dict的实际接口结果bio值list
        """
        test_data = pandas.read_csv(file, encoding="utf-8")
        exp_bio_list = []
        re_bio_list = []
        for idx, temp in test_data.iterrows():
            exp_bio_list.append(temp["exp_bio"])
            re_bio_list.append(temp["re_bio"])
        return exp_bio_list, re_bio_list

    @staticmethod
    def csv_to_dict(file):
        """
        将csv转换为dict
        :param file: 需要转换的dict数据文件
        :return test_data: 转换为dict的数据
        """
        test_data = pandas.read_csv(file, encoding="utf-8")
        return test_data

    @staticmethod
    def txt_to_dict(file):
        """
        将txt文件转换为dict
        :param file: 需要转换成dict的txt数据文件
        :return test_data: 转换为dict的数据
        """
        test_data = []
        f = open(file, "r")
        for line in f.readlines():
            test_data.append(line.strip("\n"))
        return test_data


if __name__ == '__main__':
    print(ChangeDataType().file_to_dict(rootPath + "\\testdata\\apidata\\" + "intent\\andrology\\andrology_intent.csv"))
    print(ChangeDataType().file_to_dict(rootPath + "\\testdata\\apidata\\" + "intent\\andrology\\target.txt"))
    print(ChangeDataType().file_to_dict(rootPath + "\\testdata\\apidata\\" + "symptom\\口语-标准症状映射.json"))
    print(ChangeDataType().file_to_dict(rootPath + "\\testdata\\apidata\\" + "similary\\all\\全科室相似标注-v1.xlsx",
                                        sheet_name="Sheet1"))
    print(ChangeDataType().file_to_dict(
        rootPath + "\\testresults\\resultfile\\" + "20_07_28-14_05_30gynaecology_intention_target_test_result.xls"))
