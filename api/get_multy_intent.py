# -*- coding: UTF-8 -*-
'''
Created on 2020/5/12
@File  : get_intent.py
@author: ZL
@Desc  :
'''

import os
import requests
import time
from common.change_data_type import ChangeDataType
from common.common_function import CommonFunction
from algorithm.algorithm_func import MultiClassByWord
import xlwt
import operator

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetMultIntent:

    def get_intent_result(self, target_file, bz_intent_list, re_intent_list):
        """
        通过获取target列表，以及人工及接口返回的意图值，来计算每个target及平均的准确率，召回率，F1
        :param target_file: 储存target的文件
        :param data_file: 储存接口结果数据的文件
        """
        # 获取target列表
        target_list = CommonFunction.get_target(self, target_file)
        # 返回每个target的准确率，召回率，F1
        precision_list, recall_list, f1_list, pn_list, rn_list, tn_list = MultiClassByWord.multi_each_target(self,
                                                                                                             target_list,
                                                                                                             bz_intent_list,
                                                                                                             re_intent_list)
        # 返回平均的准确率，召回率，F1
        target_list.append("平均值（不含无）")
        p, r, f1, pn, rn, tn = MultiClassByWord.multi_ave_target(self, bz_intent_list, re_intent_list, "无")
        precision_list.append(p)
        recall_list.append(r)
        f1_list.append(f1)
        pn_list.append(pn)
        rn_list.append(rn)
        tn_list.append(tn)
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        workbook = xlwt.Workbook()
        sheet1 = workbook.add_sheet('意图统计结果', cell_overwrite_ok=True)
        sheet1.write(0, 0, "意图列表")
        sheet1.write(0, 1, "人工标注数量")
        sheet1.write(0, 2, "接口结果数量")
        sheet1.write(0, 3, "一致数量")
        sheet1.write(0, 4, "准确率")
        sheet1.write(0, 5, "召回率")
        sheet1.write(0, 6, "F1值")
        for i in range(0, len(target_list)):
            sheet1.write(i + 1, 0, target_list[i])
            sheet1.write(i + 1, 1, pn_list[i])
            sheet1.write(i + 1, 2, rn_list[i])
            sheet1.write(i + 1, 3, tn_list[i])
            sheet1.write(i + 1, 4, precision_list[i])
            sheet1.write(i + 1, 5, recall_list[i])
            sheet1.write(i + 1, 6, f1_list[i])
        workbook.save(rootPath + '\\testresults\\resultfile\\' + now + "each_target_result.xls")

    def get_intent(self, api_url, target_file, test_data_file, result_file):
        """
        通过抽取测试集的数据，调用意图接口，得出的测试结果，在调用函数获取每个target的准确率，召回率，F1
        :param target_file: 储存target的文件
        :param data_file: 储存接口结果数据的文件
        """
        # 获取测试集的data
        test_data = ChangeDataType.csv_to_dict(rootPath + "\\testdata\\apidata\\intent\\" + test_data_file)
        score_list = []
        re_intent_list = []
        exp_intent_list = []
        tf_list = []
        # re_intent = ""
        # 循环读取sentence，intent
        for idx, temp in test_data.iterrows():
            intent = temp["label"]
            sentence = temp["sentence"]
            url = api_url.format(sentence)  # 接口请求
            try:
                r = requests.get(url, timeout=50)
                result = r.json()
                re_intent = result["data"]["intent"]  # 获取返回data的intent
                print(re_intent)
                score = result["data"]["score"]  # 获取返回data的score
                tf = CommonFunction.get_tf(intent, re_intent)
            except Exception as e:
                score = "bad request"
            exp_intent_list.append(intent)
            re_intent_list.append(re_intent)
            tf_list.append(tf)

        test_data["re_intent"] = re_intent_list
        # test_data["score"] = score_list
        # 调用方法，拼接test_data值
        test_data = CommonFunction.get_collections(test_data, tf_list)
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        # 输出excel
        test_data.to_excel(rootPath + '\\testresults\\resultfile\\' + now + result_file, index=False,
                           encoding="utf-8")
        GetMultIntent.get_intent_result(self, target_file, exp_intent_list, re_intent_list)

    def get_mul_intent_1(self, sentence):
        """
         意图标签完全匹配，顺序可不同
        """
        api_url = "http://192.168.1.79:8198/gynaecology_intent/v2?sentence={}"
        url = api_url.format(sentence)  # 接口请求
        r = requests.get(url, timeout=50)
        pro_intent = ['咨询案例', '描述生理现象', '描述症状', '咨询病因']
        result = r.json()
        re_intent = result["data"]["intent"]  # 获取返回data的intent
        # 对两个意图进行排序，排序后的意图可进行匹配关系
        re_intent.sort()
        pro_intent.sort()
        print(re_intent)
        print(pro_intent)
        print(operator.eq(re_intent, pro_intent))

    def get_mul_intent_2(self, sentence):
        """
         意图标签不完全匹配，但是须有包含关系，标注的意图包括接口返回，或接口意图包含标注意图均可
        """
        api_url = "http://192.168.1.79:8198/gynaecology_intent/v2?sentence={}"
        url = api_url.format(sentence)  # 接口请求
        r = requests.get(url, timeout=50)
        pro_intent = ['咨询案例', '描述生理现象']
        result = r.json()
        re_intent = result["data"]["intent"]  # 获取返回data的intent
        # 对两个意图进行排序，排序后的意图可进行匹配关系
        re_intent.sort()
        pro_intent.sort()
        # 做匹配关系的比较，若有一边有包含关系，则认为匹配成功
        if set(re_intent) > set(pro_intent) or set(pro_intent) > set(re_intent):
            print("TRUE")
        else:
            print("FALSE")

    def get_mul_intent_3(self, sentence):
        """
         意图标签不完全匹配，只要接口返回中有一个可对应上即算匹配成功
        """
        api_url = "http://192.168.1.79:8198/gynaecology_intent/v2?sentence={}"
        url = api_url.format(sentence)  # 接口请求
        r = requests.get(url, timeout=50)
        pro_intent = ['111', '描述生理现象']
        result = r.json()
        re_intent = result["data"]["intent"]  # 获取返回data的intent
        # 对两个意图进行排序，排序后的意图可进行匹配关系
        re_intent.sort()
        pro_intent.sort()
        tf_list = []
        re_list = []
        for i in range(0, len(re_intent)):
            # 做匹配关系的比较，若有一边有包含关系，则认为匹配成功
            re_list.append(re_intent[i])
            if set(re_list) > set(pro_intent) or set(pro_intent) > set(re_list):
                tf_list.append("TRUE")
            re_list = []
        if set(tf_list) >= set(["TRUE"]):
            print("TRUE")
        else:
            print("FALSE")


test = GetMultIntent()
test.get_mul_intent_3("月经推迟三四天 伴有呕吐 恶心 白带有血丝 嗓子肿疼 太阳穴疼 的症状 请问这是怎么了")
