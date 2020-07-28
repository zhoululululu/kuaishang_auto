# -*- coding: UTF-8 -*-
'''
Created on 2020/3/26
@File  : qamatcher_test.py
@author: ZL
@Desc  : 临时脚本：qamatcher测试，阈值可调整，测试结果包含：用例，相似句，以及相似句的相似程度
'''
from commonfunc.change_data_type import ChangeDataType
import os
import requests
import xlwt
from tqdm import tqdm
import time
import pandas as pd

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class Test:

    def __init__(self):
        self.faq_list, self.similar_list, self.test_data, self.score_list, self.params = [], [], [], [], []

    def get_params(self, question):
        self.params = {
            "org": "kst",
            "app": "marketing_robot",
            "industry": "infertility",
            "kb_names": ["infertility"],
            "question": question,
            "final": 10,
            "threshold": 0.6
        }
        return self.params

    def get_qamatcher_result(self, api_url, file):
        self.test_data = ChangeDataType.csv_to_dict(rootPath + "\\testdata\\apidata\\" + file)
        for idx, temp in tqdm(self.test_data.iterrows()):
            Test.get_params(self, temp["sentence"])
            r = requests.post(api_url, data=self.params, timeout=50)
            result = r.json()
            similar_faq = result["hit_question"]
            if similar_faq != "":
                self.faq_list.append(temp["sentence"])
                self.similar_list.append(similar_faq)
        Test.get_similar(self)

    def get_similar(self):
        for i in range(0, len(self.faq_list)):
            str1 = self.faq_list[i]
            str2 = self.similar_list[i]
            url = "http://192.168.1.79:8234/bert_similarity/v2?str1={}&str2={}".format(str1, str2)
            r = requests.get(url=url, timeout=100)
            result = r.json()
            score = result["sim_score"]
            self.score_list.append(score)

        result_data = pd.DataFrame(
            {"faq_list": self.faq_list, "similar_faq_list": self.similar_list, "score": self.score_list})
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        result_data.to_excel(rootPath + '\\testresults\\resultfile\\' + now + "1qamatcher_similar_test_result.xls")


if __name__ == '__main__':
    Test().get_qamatcher_result("http://192.168.26.105:30086/qastudio/v2/qamatch",
                                "qamatcher\\不孕不育qa_matcher.csv")
