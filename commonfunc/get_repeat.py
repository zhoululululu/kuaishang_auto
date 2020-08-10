# -*- coding: UTF-8 -*-
# coding=utf-8
'''
Created on 2020/6/10
@File  : get_repeat.py
@author: ZL
@Desc  :
'''
from commonfunc.change_data_type import ChangeDataType
import os
import time
import pandas as pd
import codecs

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetRepeat:

    @staticmethod
    def get_intention_repeat(file1, file2):
        res_sentence, res_label = [], []
        test_data1 = ChangeDataType.csv_to_dict(rootPath + "\\testdata\\apidata\\" + file1)
        test_data2 = ChangeDataType.excel_to_dict(rootPath + "\\testdata\\apidata\\" + file2, "Sheet1")

        sentence_list = test_data1.sentence.tolist()
        label_list = test_data1.label.tolist()
        hj_list = test_data2.text.tolist()
        for i in range(0, len(sentence_list)):
            if sentence_list[i] not in hj_list:
                res_sentence.append(sentence_list[i])
                res_label.append(label_list[i])
        result_data = pd.DataFrame({"sentence": res_sentence, "label": res_label})
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        result_data.to_excel(rootPath + '\\testresults\\resultfile\\' + now + "new_test_case.xls")

    def get_ner_repeat(self, file1, file2):
        test_data1 = ChangeDataType.file_to_dict(rootPath + "\\testdata\\apidata\\" + file1)
        test_data2 = ChangeDataType.file_to_dict(rootPath + "\\testdata\\apidata\\" + file2)
        test_data = codecs.open(rootPath + "\\testdata\\apidata\\" + "ner\\gynaecology\\test_list.txt", 'w',
                                encoding='utf-8')
        train_data = codecs.open(rootPath + "\\testdata\\apidata\\" + "ner\\gynaecology\\train_list.txt", 'w',
                                 encoding='utf-8')
        sentence1, sentence1_list, sentence2, sentence2_list, same_list = [], [], [], [], []
        for i in range(1, len(test_data1)):
            if len(test_data1[i].strip()) != 0:
                if test_data1[i].strip().split("\t\t")[0] != '"':
                    if test_data1[i].strip().split("\t\t")[0] != '“':
                        if test_data1[i].strip().split("\t\t")[0] != '”':
                            sentence1.append(test_data1[i].strip().split("\t\t")[0])
            else:
                sentence1_list.append("".join(sentence1))
                test_data.write("".join(sentence1) + "\n")
                sentence1 = []
        for i in range(1, len(test_data2)):
            if len(test_data2[i].strip()) != 0:
                # print(test_data[i])
                if test_data2[i].strip().split(" ")[0] != '"':
                    if test_data2[i].strip().split(" ")[0] != '“':
                        if test_data2[i].strip().split(" ")[0] != '”':
                            sentence2.append(test_data2[i].strip().split(" ")[0])
            else:
                sentence2_list.append("".join(sentence2))
                train_data.write("".join(sentence2) + "\n")
                sentence2 = []
        # print(sentence1_list)
        # print(sentence2_list)
        # result_data = codecs.open(rootPath + "\\testdata\\apidata\\" + "ner\\gynaecology\\same_list.txt", 'w',
        #                           encoding='utf-8')
        # n = 0
        # for i in sentence1_list:
        #     if i in sentence2_list:
        #         result_data.write(i + "\n")
        #         n += 1
        result = set(sentence1_list) & set(sentence2_list)
        print(result)
        print(len(result))
        # result_data.write(result)

    @staticmethod
    def get_duplicates(file):
        df = pd.read_csv(file, header=0)
        datalist = df.drop_duplicates()
        datalist.to_csv(file)


if __name__ == '__main__':
    # GetRepeat().get_repeat("intent\\gynaecology\\妇科-总测试数据-线上线下.csv", "intent\\gynaecology\\clear_data_v3_2.xlsx")
    # GetRepeat().quchong(rootPath + "\\testdata\\apidata\\" + "intent\\gynaecology\\妇科-总测试数据-线上线下.csv")
    GetRepeat().get_ner_repeat("ner\\gynaecology\\" + "bio_char_for_test.txt",
                               "ner\\gynaecology\\" + "train_data.txt")
