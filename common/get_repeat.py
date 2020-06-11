# -*- coding: UTF-8 -*-
# coding=utf-8
'''
Created on 2020/6/10
@File  : get_repeat.py
@author: ZL
@Desc  :
'''
from common.change_data_type import ChangeDataType
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
import pandas as pd

class GetRepeat:

    def get_repeat(self, file1, file2):
        n = 0
        list_1, list_2 = [], []
        test_data1 = ChangeDataType.csv_to_dict(rootPath + "\\testdata\\apidata\\" + file1)
        test_data2 = ChangeDataType.excel_to_dict(rootPath + "\\testdata\\apidata\\" + file2, "Sheet1")
        for idx, temp in test_data2.iterrows():
            list_1.append(temp["text"])
        for idx, temp in test_data1.iterrows():
            list_2.append(temp["sentence"])

        for i in range(0, len(list_1)):
            if list_1[i] in list_2:
                n = n + 1
                print(list_1[i])

    def quchong(self,file):
        df = pd.read_csv(file, header=0)
        datalist = df.drop_duplicates()
        datalist.to_csv(file)

if __name__ == '__main__':
    #GetRepeat().get_repeat("intent\\gynaecology\\妇科-总测试数据-线上线下.csv", "intent\\gynaecology\\new_data_all_1.xlsx")
    GetRepeat().quchong(rootPath + "\\testdata\\apidata\\" + "intent\\gynaecology\\妇科-总测试数据-线上线下.csv")
