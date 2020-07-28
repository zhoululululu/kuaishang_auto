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

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetRepeat:

    @staticmethod
    def get_repeat(file1, file2):
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

    @staticmethod
    def get_duplicates(file):
        df = pd.read_csv(file, header=0)
        datalist = df.drop_duplicates()
        datalist.to_csv(file)


if __name__ == '__main__':
    GetRepeat().get_repeat("intent\\gynaecology\\妇科-总测试数据-线上线下.csv", "intent\\gynaecology\\clear_data_v3_2.xlsx")
    # GetRepeat().quchong(rootPath + "\\testdata\\apidata\\" + "intent\\gynaecology\\妇科-总测试数据-线上线下.csv")
