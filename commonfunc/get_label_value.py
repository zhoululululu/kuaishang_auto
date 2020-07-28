# -*- coding: UTF-8 -*-
'''
Created on 2020/6/18 11:53
@File  : get_label_value.py
@author: ZL
@Desc  :
'''

from commonfunc.change_data_type import ChangeDataType
import os
import requests
import xlwt
from tqdm import tqdm
import time

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetValue:

    def get_value(self, file1, file2):
        test1_sentence1, test2_sentence1, test2_sentence2, test_label2 = [], [], [], []
        test_data_131 = ChangeDataType.csv_to_dict(rootPath + "\\testdata\\apidata\\" + file1)
        test_data_200 = ChangeDataType.csv_to_dict(rootPath + "\\testdata\\apidata\\" + file2)

        for idx, temp in tqdm(test_data_131.iterrows()):
            test1_sentence1.append(temp["sentence1"])

        for idx, temp in tqdm(test_data_200.iterrows()):
            test2_sentence1.append(temp["sentence1"])
            test2_sentence2.append(temp["sentence2"])

        for i in range(0, len(test2_sentence1)):
            if test2_sentence1[i] in test1_sentence1:
                test_label2.append(1)
            else:
                test_label2.append(0)

        workbook = xlwt.Workbook()
        sheet1 = workbook.add_sheet('统计结果', cell_overwrite_ok=True)
        sheet1.write(0, 0, "faq_list")
        sheet1.write(0, 1, "similar_faq_list")
        sheet1.write(0, 2, "bz_label")
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        for j in range(0, len(test2_sentence1)):
            sheet1.write(j + 1, 0, test2_sentence1[j])
            sheet1.write(j + 1, 1, test2_sentence2[j])
            sheet1.write(j + 1, 2, test_label2[j])

        workbook.save(rootPath + '\\testresults\\resultfile\\' + now + "get_value_test_result.xls")


if __name__ == '__main__':
    GetValue().get_value("qamatcher\\test_131.csv", "qamatcher\\test_8_233.csv")
