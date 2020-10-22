# -*- coding: UTF-8 -*-
'''
Created on 2020/9/17 9:44
@File  : get_item_align.py
@author: ZL
@Desc  :
'''

from commonfunc.change_data_type import ChangeDataType
import os
import requests
from commonfunc.common_function import CommonFunction
import time
import pandas as pd

from algorithm.algorithm_func import MultiClassByWord

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetItemAlign:
    def get_target_prf(self, test_data_file, result_file, bz_result, re_result):  #
        # result_data = pd.read_excel(
        #     rootPath + "\\testresults\\resultfile\\knowledgegraph\\itemalign\\" + "20_09_17-11_15_34item_align_result.xls")
        # bz_result = result_data.expect_item.tolist()
        # re_result = result_data.re_item.tolist()
        test_data = pd.read_csv(
            rootPath + "\\testdata\\knowledgegraph\\itemalign\\" + test_data_file)
        target_list = list(set(test_data.item.tolist()))
        precision_list, recall_list, f1_list, pn_list, rn_list, tn_list = MultiClassByWord.multi_each_target(self,
                                                                                                             target_list,
                                                                                                             bz_result,
                                                                                                             re_result)
        result_data = pd.DataFrame(
            {"target_list": target_list, "precision_list": precision_list, "recall_list": recall_list,
             "f1_list": f1_list, "pn_list": pn_list, "rn_list": rn_list,
             "tn_list": tn_list})
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        result_data.to_excel(rootPath + '\\testresults\\resultfile\\knowledgegraph\\itemalign\\' + now + result_file,
                             index=False,
                             encoding="utf-8")

    def get_item_align(self, api_url, test_data_file, result_file, target_result):
        """
        通过抽取测试集的数据，调用项目对齐接口，得出的测试结果，在调用函数获取每个target的准确率，召回率，F1
        :param result_file: 储存接口结果数据文件
        :param test_data_file: 储存测试数据文件
        """
        # 获取测试集的data
        test_data = ChangeDataType.csv_to_dict(
            rootPath + "\\testdata\\knowledgegraph\\itemalign\\" + test_data_file)
        sentence_list, origin_item_list, expect_item_list, re_item_list, tf_list, re_entity_list, entity_tf_list = [], [], [], [], [], [], []
        for idx, temp in test_data.iterrows():
            if temp["label"] == 1 and temp["origin_item"] != temp["item"]:
                origin_item = temp["origin_item"]
                sentence = temp["sentence"]
                expect_item = temp["item"]
                try:
                    url = api_url.format(sentence, origin_item)  # 接口请求
                    r = requests.get(url, timeout=50)
                    result = r.json()
                    re_item = result["data"]["align"]
                    re_entity = result["data"]["entity"]
                    tf = CommonFunction.get_tf(expect_item, re_item)
                    entity_tf = CommonFunction.get_tf(origin_item, expect_item)
                    sentence_list.append(sentence)
                    origin_item_list.append(origin_item)
                    expect_item_list.append(expect_item)
                    re_entity_list.append(re_entity)
                    re_item_list.append(re_item)
                    tf_list.append(tf)
                    entity_tf_list.append(entity_tf)
                except Exception as e:
                    print(e)
        result_data = pd.DataFrame(
            {"sentence": sentence_list, "origin_item": origin_item_list, "expect_item": expect_item_list,
             "re_entity": re_entity_list, "re_item": re_item_list, "re_entity_tf": entity_tf_list,
             "re_item_tf": tf_list,
             "all_num": len(tf_list), "re_item_true_num": tf_list.count("TRUE"),
             "re_item_true_percent": "{:.2f}%".format(tf_list.count("TRUE") / len(tf_list) * 100),
             "re_item_false_num": tf_list.count("FALSE"),
             "re_item_false_percent": "{:.2f}%".format(tf_list.count("FALSE") / len(tf_list) * 100),
             "re_entity_true_num": entity_tf_list.count("TRUE"),
             "re_entity_true_percent": "{:.2f}%".format(entity_tf_list.count("TRUE") / len(entity_tf_list) * 100),
             "re_entity_false_num": entity_tf_list.count("FALSE"),
             "re_entity_false_percent": "{:.2f}%".format(entity_tf_list.count("FALSE") / len(entity_tf_list) * 100)
             })
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        result_data.to_excel(rootPath + '\\testresults\\resultfile\\knowledgegraph\\itemalign\\' + now + result_file,
                             index=False,
                             encoding="utf-8")
        GetItemAlign.get_target_prf(self, "relation_to_test_first_3019.csv",
                                    target_result, expect_item_list, re_item_list)

if __name__ == '__main__':
    GetItemAlign().get_item_align("http://192.168.1.79:8235/entity_align/v1?sentence={}&entity={}",
                                  "relation_to_test_first_3019.csv", "item_align_result.xls", "target_result.xls")
#     GetItemAlign().get_target_prf("relation_to_test_first_3019.csv","target_result.xls")
