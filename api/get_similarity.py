# -*- coding: UTF-8 -*-
'''
Created on 2020/2/26
@File  : test_get_symptom_similarity.py
@author: ZL
@Desc  :
'''

import os
import requests
import time
from tqdm import tqdm
from common.change_data_type import ChangeDataType
from common.common_function import CommonFunction
from algorithm.algorithm_func import Binary

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetSymptomSimilarity:

    def get_symptom_similarity(self, api_url, test_data_file, result_file):
        test_data = ChangeDataType.csv_to_dict(rootPath + "\\testdata\\apidata\\" + test_data_file)
        lb_list, re_label_list, normal_sys_list, tf_list = [], [], [], []
        for idx, temp in tqdm(test_data.iterrows()):
            label = int(temp["label"])
            str1 = temp["普通症状"]
            str2 = temp["标准症状"]
            url = api_url.format(str1)
            try:
                r = requests.get(url, timeout=1000)
                print(r)
                result = r.json()
                normal_sys = result["standard"]
                re_label = CommonFunction.get_sys_similary_tf(normal_sys, str2)
                tf = CommonFunction.get_tf(re_label, label)
            except Exception as e:
                score = "bad request"
                print(e)
            # self.logging.info("症状1：" + str1 + "---症状2：" + str2 + "---预期分数："
            #                   + str(label) + "---实际分数：" + str(re_score) + "---是否一致：" + tf)
            normal_sys_list.append(normal_sys)
            # score_list.append(score)
            re_label_list.append(re_label)
            tf_list.append(tf)
            lb_list.append(label)
        test_data["normal_sys"] = normal_sys_list
        test_data["re_label"] = re_label_list
        test_data = CommonFunction.get_collection_1(test_data, tf_list)
        Binary.binary_plot_curve(lb_list, re_label_list)
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        test_data.to_excel(rootPath + '\\testresults\\resultfile\\' + now + result_file, index=False,
                           encoding="utf-8")


if __name__ == '__main__':
    GetSymptomSimilarity().get_symptom_similarity("http://192.168.1.74:1122/demo?sentence={}",
                                                  "similary\\gynaecology_sym_test_1740.csv",
                                                  "gynaecology_symptom_similary_test_result.xls")
