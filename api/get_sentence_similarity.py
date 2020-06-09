# -*- coding: UTF-8 -*-
'''
Created on 2020/2/26
@File  : test_get_qa_similarity.py
@author: ZL
@Desc  :
'''

import os
import requests
import time
from common.change_data_type import ChangeDataType
from common.common_function import CommonFunction
from algorithm.algorithm_func import Binary
from algorithm.algorithm_func import MultiClassByWord
import xlwt
from tqdm import tqdm

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetSentenceSimilarity:

    def get_sentence_similarity_target(self, api_url, test_data_file, result_file):
        test_data = ChangeDataType.csv_to_dict(rootPath + "\\testdata\\apidata\\" + test_data_file)
        score_list = []
        re_score_list = []
        lb_list = []
        workbook = xlwt.Workbook()
        sheet1 = workbook.add_sheet("相似度超参数统计结果", cell_overwrite_ok=True)
        sheet1.write(0, 0, "阈值")
        sheet1.write(0, 1, "准确率P")
        sheet1.write(0, 2, "召回率R")
        sheet1.write(0, 3, "F1值")
        for idx, temp in tqdm(test_data.iterrows()):
            label = int(temp["label"])
            str1 = temp["sentence"]
            str2 = temp["sentence2"]
            url = api_url.format(str1, str2)
            try:
                r = requests.get(url, timeout=50)
                result = r.json()
                score = result["sim_score"]
                # print(score)
                score_list.append(score)
                lb_list.append(label)
            except Exception as e:
                score = "bad request"
                print(score)
        n = 0
        i = 0
        while (i < 0.95):
            n += 1
            i += 0.05
            for j in range(0, len(score_list)):
                re_score = CommonFunction.get_re_score(score_list[j], i)
                print(i, lb_list[j], re_score)
                re_score_list.append(re_score)
            print(lb_list)
            print(re_score_list)
            p = Binary.get_precision_score(lb_list, re_score_list)
            r = Binary.get_recall_score(lb_list, re_score_list)
            f1 = Binary.get_f1_score(lb_list, re_score_list)
            sheet1.write(n, 0, i)
            sheet1.write(n, 1, p)
            sheet1.write(n, 2, r)
            sheet1.write(n, 3, f1)
            p, r, f1 = 0, 0, 0
            re_score_list = []
        workbook.save(rootPath + '\\testresults\\resultfile\\' + result_file)

    def get_sentence_similarity(self, api_url, test_data_file, result_file):
        # self.logging = Logging()
        print("begin")
        test_data = ChangeDataType.csv_to_dict(rootPath + "\\testdata\\apidata\\similary\\" + test_data_file)
        print(test_data)
        score_list = []
        re_score_list = []
        tf_list = []
        re_score = ""
        tf = ""
        lb_list = []
        for idx, temp in test_data.iterrows():
            label = int(temp["label"])
            str1 = temp["sentence"]
            str2 = temp["sentence2"]
            url = api_url.format(str1, str2)
            try:
                r = requests.get(url, timeout=50)
                result = r.json()
                score = result["data"]["score"]
                re_score = CommonFunction.get_re_score(score, 0.85)
                tf = CommonFunction.get_tf(re_score, label)
                print(re_score, tf)
            except Exception as e:
                score = "bad request"
                print(score)
            # self.logging.info("症状1：" + str1 + "---症状2：" + str2 + "---预期分数："
            #                   + str(label) + "---实际分数：" + str(re_score) + "---是否一致：" + tf)
            score_list.append(score)
            re_score_list.append(re_score)
            tf_list.append(tf)
            lb_list.append(label)
        test_data["score"] = score_list
        test_data["re_score"] = re_score_list
        test_data = CommonFunction.get_collection_1(test_data, tf_list)
        Binary.binary_plot_curve(lb_list, re_score_list)
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        test_data.to_excel(rootPath + '\\testresults\\resultfile\\' + now + result_file, index=False,
                           encoding="utf-8")


test = GetSentenceSimilarity()

test.get_sentence_similarity_target("http://192.168.1.79:8234/bert_similarity/v2?str1={}&str2={}",
                                    "similary\\qa_similary\\相似度原始数据-白癜风.csv", "白癜风超参数统计结果.xls")

test.get_sentence_similarity_target("http://192.168.1.79:8234/bert_similarity/v2?str1={}&str2={}",
                                    "similary\\qa_similary\\相似度原始数据-银屑病.csv", "银屑病超参数统计结果.xls")
