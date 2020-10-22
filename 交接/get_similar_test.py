# -*- coding: UTF-8 -*-
'''
Created on 2020/10/22 17:14
@File  : get_similar_test.py
@author: ZL
@Desc  :
'''
from commonfunc.change_data_type import ChangeDataType
import os
import requests
import time
import pandas as pd
from algorithm.algorithm_func import Binary
from commonfunc.common_function import CommonFunction

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class Similar:

    def get_similar_test(self, api_url, threshold, test_data_file, result_file):
        # 根据需求修改testdata
        test_data = ChangeDataType.csv_to_dict(rootPath + "\\testdata\\apidata\\similary\\andrology\\" + test_data_file)
        score_list, re_score_list, tf_list = [], [], []
        sentence1_list = test_data.sentence.tolist()
        sentence2_list = test_data.sentence2.tolist()
        label_list = test_data.label.tolist()
        for i in range(len(sentence1_list)):

            # 根据需求修改params
            params = {
                "str1": sentence1_list[i],
                "str2": sentence2_list[i],
                "model": "Siamese",
            }
            try:
                r = requests.get(url=api_url, params=params, timeout=50)
                result = r.json()
                score = result["sim_score"]
                re_score = CommonFunction.get_re_score(score, threshold)
                tf = CommonFunction.get_tf(re_score, label_list[i])
            except Exception as e:
                score = "bad request"
                re_score = 2
                tf = CommonFunction.get_tf(re_score, label_list[i])
            score_list.append(score)
            re_score_list.append(re_score)
            tf_list.append(tf)
        Binary.binary_plot_curve(label_list, re_score_list)
        testresult = pd.DataFrame({"sentence1": sentence1_list, "sentence2": sentence2_list, "label_list": label_list,
                                   "response": score_list, "re_response": re_score_list, "tf_list": tf_list})

        now = time.strftime('%y_%m_%d-%H_%M_%S')
        testresult.to_excel(rootPath + "\\testresults\\resultfile\\similar\\" + now + result_file)


if __name__ == '__main__':
    # 根据需求修改url及threshold
    Similar().get_similar_test("http://192.168.1.79:8234/bert_similarity/v2", 0.757, "相似度原始数据-男科.csv",
                               "andrology_similar_result.xls")
