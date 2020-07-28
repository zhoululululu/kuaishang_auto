# -*- coding: UTF-8 -*-
'''
Created on 2020/2/26
@File  : test_get_qa_similarity.py
@author: ZL
@Desc  :
'''

import os
import requests
from commonfunc.change_data_type import ChangeDataType
from commonfunc.common_function import CommonFunction
from algorithm.algorithm_func import Binary
from algorithm.algorithm_func import MultiClassByWord
import xlwt
import time
import pandas as pd
from tqdm import tqdm

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetSentenceSimilarity:

    def get_sentence_similarity_target(self, api_url, test_data_file, result_file):
        test_data = ChangeDataType.csv_to_dict(rootPath + "\\testdata\\apidata\\" + test_data_file)
        score_list, s1_list, s2_list = [], [], []
        re_score_list = []
        lb_list = []
        workbook = xlwt.Workbook()
        sheet1 = workbook.add_sheet("相似度超参数统计结果", cell_overwrite_ok=True)
        sheet1.write(0, 0, "阈值")
        sheet1.write(0, 1, "准确率P")
        sheet1.write(0, 2, "召回率R")
        sheet1.write(0, 3, "F1值")
        sheet1.write(0, 4, "accuracy")
        for idx, temp in tqdm(test_data.iterrows()):
            label = int(temp["label"])
            str1 = temp["sentence"]
            str2 = temp["sentence2"]
            s1_list.append(str1)
            s2_list.append(str2)
            url = api_url.format(str1, str2)
            try:
                r = requests.get(url, timeout=50)
                result = r.json()
                score1 = result["data"]["score"]
                score2 = result["data"]["scorer"]
                score = min(score1, score2)
                score_list.append(score)
                lb_list.append(label)
            except Exception as e:
                score = "bad request"
                print(score)
        n = 0
        i = 0
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        result_data = pd.DataFrame(
            {"sentence1": s1_list, "sentence2": s2_list, "label": lb_list, "score": score_list, })
        result_data.to_excel(rootPath + '\\testresults\\resultfile\\' + now + "1全科室测试结果.xlsx")
        while (i < 0.99):
            n += 1
            i += 0.01
            for j in range(0, len(score_list)):
                re_score = CommonFunction.get_re_score(score_list[j], i)
                re_score_list.append(re_score)
            p, r, f1, pn, rn, tn = MultiClassByWord.class_target(self, lb_list, re_score_list, 1)
            P, R, F1, accuracy, mis_rate = Binary.get_binary_score(lb_list, re_score_list)
            sheet1.write(n, 0, i)
            sheet1.write(n, 1, p)
            sheet1.write(n, 2, r)
            sheet1.write(n, 3, f1)
            sheet1.write(n, 4, accuracy)
            p, r, f1, accuracy = 0, 0, 0, 0
            re_score_list = []
        workbook.save(rootPath + '\\testresults\\resultfile\\' + now + result_file)

    def get_sentence_similarity(self, api_url, test_data_file, result_file):
        # self.logging = Logging()
        testdata2 = {}
        # test_data = ChangeDataType.excel_to_dict(rootPath + "\\testdata\\apidata\\" + test_data_file,
        #                                          sheet_name="Sheet1")
        test_data = ChangeDataType.csv_to_dict(rootPath + "\\testdata\\apidata\\" + test_data_file)
        score_list = []
        re_score_list = []
        tf_list = []
        re_score = ""
        tf = ""
        lb_list, sen1, sen2 = [], [], []
        for idx, temp in tqdm(test_data.iterrows()):
            label = int(temp["label"])
            str1 = temp["sentence1"]
            str2 = temp["sentence2"]
            sen1.append(str1)
            sen2.append(str2)
            url = api_url.format(str1, str2)
            try:
                r = requests.get(url, timeout=50)
                result = r.json()
                score1 = result["data"]["score"]
                score2 = result["data"]["scorer"]
                score = min(score1, score2)
                re_score = CommonFunction.get_re_score(score, 0.916)
                tf = CommonFunction.get_tf(re_score, label)
            except Exception as e:
                score = "bad request"
                print(score)
            score_list.append(score)
            re_score_list.append(re_score)
            tf_list.append(tf)
            lb_list.append(label)
        # test_data = CommonFunction.get_collection_1(test_data, tf_list)
        Binary.binary_plot_curve(lb_list, re_score_list)
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        workbook = xlwt.Workbook()
        sheet1 = workbook.add_sheet('统计结果', cell_overwrite_ok=True)
        sheet1.write(0, 0, "sentence1")
        sheet1.write(0, 1, "sentence2")
        sheet1.write(0, 2, "score")
        sheet1.write(0, 3, "re_score")
        sheet1.write(0, 4, "label")
        sheet1.write(0, 5, "tf")
        for i in range(0, len(score_list)):
            sheet1.write(i + 1, 0, sen1[i])
            sheet1.write(i + 1, 1, sen2[i])
            sheet1.write(i + 1, 2, score_list[i])
            sheet1.write(i + 1, 3, re_score_list[i])
            sheet1.write(i + 1, 4, lb_list[i])
            sheet1.write(i + 1, 5, tf_list[i])

        workbook.save(rootPath + '\\testresults\\resultfile\\' + now + result_file)

    def get_sentence_similarity_twomodel(self, api_url, test_data_file, result_file):
        # self.logging = Logging()
        testdata2 = {}
        # test_data = ChangeDataType.excel_to_dict(rootPath + "\\testdata\\apidata\\" + test_data_file,
        #                                          sheet_name="Sheet1")
        test_data = ChangeDataType.csv_to_dict(rootPath + "\\testdata\\apidata\\" + test_data_file)
        score_list = []
        re_score_list = []
        tf_list = []
        re_score = ""
        tf = ""
        lb_list, sen1, sen2 = [], [], []
        for idx, temp in tqdm(test_data.iterrows()):
            label = int(temp["label"])
            str1 = temp["sentence1"]
            str2 = temp["sentence2"]
            sen1.append(str1)
            sen2.append(str2)
            url = api_url.format(str1, str2)
            try:
                r = requests.get(url, timeout=50)
                result = r.json()
                score = result["data"]["score"]
                re_score = CommonFunction.get_re_score(score, 0.916)
                tf = CommonFunction.get_tf(re_score, label)
            except Exception as e:
                score = "bad request"
                print(score)
            score_list.append(score)
            re_score_list.append(re_score)
            tf_list.append(tf)
            lb_list.append(label)
        Binary.binary_plot_curve(lb_list, re_score_list)
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        workbook = xlwt.Workbook()
        sheet1 = workbook.add_sheet('统计结果', cell_overwrite_ok=True)
        sheet1.write(0, 0, "sentence1")
        sheet1.write(0, 1, "sentence2")
        sheet1.write(0, 2, "score")
        sheet1.write(0, 3, "re_score")
        sheet1.write(0, 4, "label")
        sheet1.write(0, 5, "tf")
        for i in range(0, len(score_list)):
            sheet1.write(i + 1, 0, sen1[i])
            sheet1.write(i + 1, 1, sen2[i])
            sheet1.write(i + 1, 2, score_list[i])
            sheet1.write(i + 1, 3, re_score_list[i])
            sheet1.write(i + 1, 4, lb_list[i])
            sheet1.write(i + 1, 5, tf_list[i])

        workbook.save(rootPath + '\\testresults\\resultfile\\' + now + result_file)

    def get_sentence_similarity_pro(self, api_url, test_data_file, result_file):
        # self.logging = Logging()
        testdata2 = {}
        # test_data = ChangeDataType.excel_to_dict(rootPath + "\\testdata\\apidata\\" + test_data_file,
        #                                          sheet_name="Sheet1")
        test_data = ChangeDataType.csv_to_dict(rootPath + "\\testdata\\apidata\\" + test_data_file)
        score_list = []
        re_score_list = []
        tf_list = []
        re_score = ""
        tf = ""
        lb_list, sen1, sen2 = [], [], []
        for idx, temp in tqdm(test_data.iterrows()):
            label = int(temp["label"])
            str1 = temp["sentence1"]
            str2 = temp["sentence2"]
            sen1.append(str1)
            sen2.append(str2)
            url = api_url.format(str1, str2)
            try:
                r = requests.get(url, timeout=50)
                result = r.json()
                score = result["sim_score"]
                re_score = CommonFunction.get_re_score(score, 0.85)
                tf = CommonFunction.get_tf(re_score, label)
            except Exception as e:
                score = "bad request"
                print(score)
            score_list.append(score)
            re_score_list.append(re_score)
            tf_list.append(tf)
            lb_list.append(label)
        Binary.binary_plot_curve(lb_list, re_score_list)
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        workbook = xlwt.Workbook()
        sheet1 = workbook.add_sheet('统计结果', cell_overwrite_ok=True)
        sheet1.write(0, 0, "sentence1")
        sheet1.write(0, 1, "sentence2")
        sheet1.write(0, 2, "score")
        sheet1.write(0, 3, "re_score")
        sheet1.write(0, 4, "label")
        sheet1.write(0, 5, "tf")
        for i in range(0, len(score_list)):
            sheet1.write(i + 1, 0, sen1[i])
            sheet1.write(i + 1, 1, sen2[i])
            sheet1.write(i + 1, 2, score_list[i])
            sheet1.write(i + 1, 3, re_score_list[i])
            sheet1.write(i + 1, 4, lb_list[i])
            sheet1.write(i + 1, 5, tf_list[i])

        workbook.save(rootPath + '\\testresults\\resultfile\\' + now + result_file)

    def get_collect(self, file, test_result_file):
        re_score_list, p_list, r_list, f1_list, i_list = [], [], [], [], []
        test_data = ChangeDataType.excel_to_dict(rootPath + "\\testresults\\resultfile\\" + file,
                                                 sheet_name="统计结果")
        score_list = test_data.score.tolist()
        label_list = test_data.label.tolist()
        i = 0
        n = 0
        while (i < 0.99):
            n += 1
            i += 0.01
            for j in range(0, len(score_list)):
                re_score = CommonFunction.get_re_score(score_list[j], i)
                re_score_list.append(re_score)
            p, r, f1, pn, rn, tn = MultiClassByWord.class_target(self, label_list, re_score_list, 1)
            p_list.append(p)
            r_list.append(r)
            f1_list.append(f1)
            i_list.append(i)
            re_score_list = []
        excel_data = pd.DataFrame({"阈值": i_list, "准确率": p_list, "召回率": r_list, "f1值": f1_list})
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        excel_data.to_excel(rootPath + '\\testresults\\resultfile\\' + now + test_result_file)

    def get_prf(self, file, i):
        re_score_list = []
        test_data = ChangeDataType.excel_to_dict(rootPath + "\\testresults\\resultfile\\" + file,
                                                 sheet_name="统计结果")
        score_list = test_data.score.tolist()
        label_list = test_data.label.tolist()
        for j in range(0, len(score_list)):
            re_score = CommonFunction.get_re_score(score_list[j], i)
            re_score_list.append(re_score)
        p, r, f1, pn, rn, tn = MultiClassByWord.class_target(self, label_list, re_score_list, 1)
        print("p:", p, "r:", r, "f1:", f1, "pn:", pn, "rn:", rn, "tn:", tn)


if __name__ == '__main__':
    test = GetSentenceSimilarity()
    # test.get_prf("20_017_08-20_50_52新全科室统计结果.xls", 0.916)
    # test.get_prf("20_017_14-14_26_26测试环境_医美统计结果.xls", 0.916)
    test.get_collect("120_07_15-17_38_04测试环境_全科室统计结果.xls", "新全科超参数结果.xls")
    # test.get_collect("1120_07_15-14_49_01测试环境_医美统计结果.xls", "新医美超参数结果.xls")
    #
    # test.get_sentence_similarity_twomodel("http://192.168.1.79:8235/bert_similarity/v2?str1={}&str2={}&model=siamese",
    #                                       "similary\\all\\全科室新测试数据.csv", "测试环境_全科1室统计结果.xls")

    # test.get_sentence_similarity_pro("http://192.168.1.79:8234/bert_similarity/v2?str1={}&str2={}&model=rwms",
    # "similary\\beauty\\beauty_to_test.csv", "医美全科室统计结果.xls")
    # test_data = ChangeDataType.excel_to_dict(
    #     rootPath + "\\testresults\\resultfile\\" + "全科室测试结果2w-测试环境.xls",
    #     sheet_name="统计结果")
    # bz_list = test_data.label.tolist()
    # re_list = test_data.re_score.tolist()
    # print(Binary.get_binary_score(bz_list, re_list))
