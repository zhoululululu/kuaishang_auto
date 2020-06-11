# -*- coding: UTF-8 -*-
'''
Created on 2020/2/27
@File  : test_get_intent.py
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
from tqdm import tqdm
from common.get_mult_acount import GetMultCount

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetIntent:

    def get_intent_result(self, target_file, bz_intent_list, re_intent_list, test_result_file, total_num, accuracy):
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

        target_list.append("汇总")
        precision_list.append("用例数：" + total_num)
        recall_list.append("accuracy：" + accuracy)
        f1_list.append("")
        pn_list.append("")
        rn_list.append("")
        tn_list.append("")
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
        workbook.save(rootPath + '\\testresults\\resultfile\\' + now + test_result_file)
        return rootPath + '\\testresults\\resultfile\\' + now + test_result_file

    def get_intent(self, api_url, target_file, test_data_file, result_file, test_result_file):
        """
        通过抽取测试集的数据，调用意图接口，得出的测试结果，在调用函数获取每个target的准确率，召回率，F1
        :param target_file: 储存target的文件
        :param data_file: 储存接口结果数据的文件
        """
        # 获取测试集的data
        test_data = ChangeDataType.csv_to_dict(rootPath + "\\testdata\\apidata\\intent\\" + test_data_file)
        re_intent_list = []
        exp_intent_list = []
        tf_list = []
        # 循环读取sentence，intent
        for idx, temp in tqdm(test_data.iterrows()):
            intent = temp["label"]
            sentence = temp["sentence"]
            url = api_url.format(sentence)  # 接口请求
            try:
                r = requests.get(url, timeout=50)
                result = r.json()
                re_intent = result["data"]["intent"]  # 获取返回data的intent
                print(re_intent)
                tf = CommonFunction.get_tf(intent, re_intent)
            except Exception as e:
                score = "bad request"
            exp_intent_list.append(intent)
            re_intent_list.append(re_intent)
            tf_list.append(tf)

        test_data["re_intent"] = re_intent_list
        test_data, total_num, accuracy = CommonFunction.get_collection_1(test_data, tf_list)
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        # 输出excel
        test_data.to_excel(rootPath + '\\testresults\\resultfile\\' + now + result_file, index=False,
                           encoding="utf-8")
        GetIntent.get_intent_result(self, target_file, exp_intent_list, re_intent_list, test_result_file, total_num,
                                    accuracy)

    def get_pro_intent(self, api_url, target_file, test_data_file, result_file, test_result_file):
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
        # 循环读取sentence，intent
        for idx, temp in tqdm(test_data.iterrows()):
            intent = temp["label"]
            sentence = temp["sentence"]
            now = time.time()
            headers = {
                # 银屑病
                # 'Authorization': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb21wYW55X2lkIjozMjgsInJvYm90X2lkIjo0MDgsImV4cCI6MTU5MTc3MTA4Nn0.yVYXxFgPxRP3IU30BhfN3zmIQSDAvS3tdR8l_WjrS-8",
                # 白癜风
                # "Authorization":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb21wYW55X2lkIjozMjgsInJvYm90X2lkIjo0MDcsImV4cCI6MTU5MTc3MTA4Nn0.Kx8PNK4jE-i9SWOx-RAy29wAZnqvmZjuMUyBxVJSdPo",
                # 妇科
                'Authorization': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb21wYW55X2lkIjo1MDUsInJvYm90X2lkIjo2NjMsImV4cCI6MTU5MjI5NjAwMH0.CtrWIId05L1c2MGf8AvViFIblhT5lFdsK47bJcR1LEs",
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = {
                'dialog': sentence,
                'client_id': "zltest" + str(now),
            }
            url = api_url.format(sentence)  # 接口请求
            try:
                r = requests.post(url, data=data, headers=headers, timeout=50)
                result = r.json()
                # re_intent = result["ner_result"]["ner"]["intent"]["Value"][0]["Value"]  # 获取返回data的intent
                re_intent = result["data"]["ner"]["intent"]["Value"][0]["Value"]  # 获取返回data的intent
                tf = CommonFunction.get_tf(intent, re_intent)
            except Exception as e:
                score = "bad request"
            exp_intent_list.append(intent)
            re_intent_list.append(re_intent)
            tf_list.append(tf)
            time.sleep(0.1)

        test_data["re_intent"] = re_intent_list
        # 调用方法，拼接test_data值
        test_data = CommonFunction.get_collection_1(test_data, tf_list)
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        # 输出excel
        test_data.to_excel(rootPath + '\\testresults\\resultfile\\' + now + result_file, index=False,
                           encoding="utf-8")
        GetIntent.get_intent_result(self, target_file, exp_intent_list, re_intent_list, test_result_file)

    def get_eye_intent(self, api_url, target_file, test_data_file, result_file):
        """
        通过抽取测试集的数据，调用意图接口，得出的测试结果，在调用函数获取每个target的准确率，召回率，F1
        :param target_file: 储存target的文件
        :param data_file: 储存接口结果数据的文件
        """
        # 获取测试集的data
        test_data = ChangeDataType.csv_to_dict(rootPath + "\\testdata\\apidata\\" + test_data_file)
        score_list = []
        re_intent_list = []
        bz_intent_list = []
        tf_list = []
        re_intent = ""
        tf = ""
        # 循环读取sentence，intent
        for idx, temp in test_data.iterrows():
            intent = temp["intention"]
            sentence = temp["sentence"]
            # 发起请求
            url = api_url.format(sentence)
            try:
                r = requests.get(url, timeout=50)
                result = r.json()
                re_intent = result["data"]["intent"]  # 获取返回data的intent
                print(re_intent)
                tf = CommonFunction.get_tf(intent, re_intent)
            except Exception as e:
                score = "bad request"
                print(e)
            bz_intent_list.append(intent)
            re_intent_list.append(re_intent)
            tf_list.append(tf)

        test_data["re_intent"] = re_intent_list
        test_data = CommonFunction.get_collections(test_data, tf_list)
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        # 输出excel
        test_data.to_excel(rootPath + '\\testresults\\resultfile\\' + now + result_file, index=False,
                           encoding="utf-8")
        GetIntent.get_intent_result(self, target_file, bz_intent_list, re_intent_list)

    def get_mult_intent(self, api_url, target_file, test_data_file, result_file, final_result):
        """
        此方法专为多意图测试（妇科）
        通过抽取测试集的数据，调用意图接口，得出的测试结果，在调用函数获取每个target的准确率，召回率，F1
        :param target_file: 储存target的文件
        :param data_file: 储存接口结果数据的文件
        """
        # 获取测试集的data
        test_data = ChangeDataType.excel_to_dict(rootPath + "\\testdata\\apidata\\" + test_data_file, "Sheet1")
        re_intent_list, re_score_list, exp_intent_list, tf_list = [], [], [], []
        # 循环读取sentence，intent
        for idx, temp in tqdm(test_data.iterrows()):
            # 获取用例文件中的意图label值，由于测试用例中多意图以符号、隔开，所以此处做一个切割
            intent = temp["label"].split("、")
            # 获取用例sentence
            sentence = temp["sentence"]
            url = api_url.format(sentence)  # 接口请求
            try:
                r = requests.get(url, timeout=50)
                result = r.json()
                re_intent = result["data"]["intention"][0]  # 获取返回data的intent意图值
                re_score = result["data"]["prob"]  # 获取返回data的score概率值
                intent.sort()
                re_intent.sort()
            except Exception as e:
                score = "bad request"
            exp_intent_list.append(intent)
            re_score_list.append(re_score)
            re_intent_list.append(re_intent)
        tf_list = GetMultCount().get_mult_tf_and_count(exp_intent_list, re_intent_list)
        test_data = CommonFunction.get_collection_1(test_data, tf_list)
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        # 输出excel
        test_data["label"] = exp_intent_list
        test_data["re_score"] = re_score_list
        test_data["re_intent"] = re_intent_list
        test_data["tf"] = tf_list
        test_data.to_excel(rootPath + '\\testresults\\resultfile\\' + now + result_file, index=False,
                           encoding="utf-8")

        # GetMultCount.output_threshold(self, exp_intent_list, re_score_list, target_file)
        # GetMultCount.get_half_threshold(self, target_file)
        # GetMultCount.get_best_threshold(self, target_file)
        # test_data = CommonFunction.get_collection_1(test_data, tf_list)
        # test_data.to_excel(rootPath + '\\testresults\\resultfile\\' + now + result_file, index=False,
        #                    encoding="utf-8")
        CommonFunction.get_collection_2(self, target_file, exp_intent_list, re_intent_list, final_result)

    def get_final_excel(self, target_file, final_result):
        test_data = ChangeDataType.excel_to_dict(
            rootPath + "\\testresults\\resultfile\\20_05_28-17_00_08gynaecology_mult_intent_test_result11.xls",
            "Sheet1")
        exp_list = test_data["label"]
        re_list = test_data["re_intent"]
        CommonFunction.get_collection_2(self, target_file, exp_list, re_list, final_result)

    def get_test_excel(self, target_file, final_result):
        test_data = ChangeDataType.excel_to_dict(
            rootPath + "\\testresults\\resultfile\\20_05_28-19_55_32gynaecology_mix_intent_test_result11.xls",
            "Sheet1")
        exp_list = test_data["label"]
        re_list = test_data["re_score"]
        # GetMultCount.get_half_threshold(self, exp_list, re_list, target_file)
        GetMultCount.get_half_threshold(self, target_file)


if __name__ == '__main__':
    # GetIntent().get_pro_intent("http://robotchat.kuaishangkf.com/x/identify/v1/re_unify/identify",
    #                            "intent\\dermatology\\andpsorasis.txt", "psoriasis\\psoriasis_test_500.csv",
    #                            "psoriasis_pro_result.xls")
    GetIntent().get_pro_intent("http://robotchat.kuaishangkf.com/x/identify/v1/re_unify/identify",
                               "intent\\gynaecology\\线上target.txt", "gynaecology\\hj_test.csv",
                               "gynaecology_pro_result(hj).xls", "gynaecology_pro_target_result(hj).xls")
#     GetIntent().get_mult_intent("http://192.168.1.74:8900/multi_intention/v2?sentence={}",
# #                                 "intent\\gynaecology\\test_target.txt",
# #                                 "intent\\gynaecology\\gynaecology_to_test.xlsx",
# #                                 "gynaecology_mix_intent_test_result.xls", "mix_final_result.xls")
# # GetIntent().get_final_excel("intent\\gynaecology\\test_target.txt", "mult_final_result.xls")
# # GetIntent().get_test_excel("intent\\gynaecology\\test_target.txt", "mix_final_result.xls")
