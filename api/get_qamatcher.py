# -*- coding: UTF-8 -*-
'''
Created on 2020/5/29
@File  : get_qamatcher.py
@author: ZL
@Desc  :
'''

import requests
from common.change_data_type import ChangeDataType
import os
import xlwt
from tqdm import tqdm

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetQaMatcher:

    def __init__(self):
        pass

    @staticmethod
    def get_params(question):
        params = {
            "org": "kst",
            "app": "marketing_robot",
            "industry": "vitiligo",
            "kb_names": ["vitiligo"],
            "question": question,
            "final": 10
        }
        return params

    def get_qa_matcher_result(self, api_url, test_data_file, result_file):
        workbook = xlwt.Workbook()
        sheet1 = workbook.add_sheet('结果', cell_overwrite_ok=True)
        sheet1.write(0, 0, "question")
        sheet1.write(0, 1, "hit_question")
        sheet1.write(0, 2, "answer")
        n = 0
        test_data = ChangeDataType.csv_to_dict(rootPath + "\\testdata\\apidata\\qamatcher\\" + test_data_file)
        for idx, question in tqdm(test_data.iterrows()):
            params = GetQaMatcher.get_params(question[0])
            try:
                r = requests.post(api_url, data=params, timeout=50)
                result = r.json()
                # print(result)
                if "hit_question" in result:
                    re_question = str(result["hit_question"])
                    answer = str(result["faq_answer"])
                    if re_question != "" or answer != "":
                        n += 1
                        print(question[0])
                        sheet1.write(n, 0, question[0])
                        sheet1.write(n, 1, re_question)
                        sheet1.write(n, 2, answer)
                else:
                    pass
            except Exception as e:
                print("")

        workbook.save(rootPath + '\\testresults\\resultfile\\' + result_file)

    def get_caq(self, test_file, result_file):
        test_data = ChangeDataType.txt_to_dict(test_file)
        cqa_test_data, c_test_data = [], []
        for value in test_data:
            if "C00000" in value:
                c_test_data.append(value.split("##$$：")[1])
        for value in test_data:
            if "Q00000" in value:
                cqa_test_data.append(value.split("##$$：")[1])
        workbook = xlwt.Workbook()
        sheet1 = workbook.add_sheet('行业库数据', cell_overwrite_ok=True)
        sheet1.write(0, 0, "c")
        sheet1.write(0, 1, "question")
        sheet1.write(0, 2, "frequency")
        for i in range(0, len(cqa_test_data)):
            sheet1.write(i + 1, 0, c_test_data[i])
            sheet1.write(i + 1, 1, cqa_test_data[i])
            sheet1.write(i + 1, 2, 0)
        workbook.save(rootPath + '\\testdata\\apidata\\qamatcher\\' + result_file)

    def get_frequency(self, test_file, re_test_file, final_result):
        test_data = ChangeDataType.excel_to_dict(test_file, "行业库数据")
        re_test_data = ChangeDataType.excel_to_dict(re_test_file, "结果")
        no_list, re_question_list, cqa_list, c_list = [], [], [], []
        for idx, data in test_data.iterrows():
            cqa = data["question"]
            c = data["c"]
            no = data["frequency"]
            cqa_list.append(cqa)
            c_list.append(c)
            no_list.append(no)
        i = 0
        for idx, data in re_test_data.iterrows():
            re_question = data["hit_question"]
            n = 0
            while i < len(cqa_list):
                if re_question == cqa_list[i] or re_question == str(cqa_list[i]) + str(
                        c_list[i]) or re_question == str(c_list[i]) + str(cqa_list[i]) or re_question == c_list[i]:
                    no_list[i] += 1
                    i = len(cqa_list)
                else:
                    i += 1
                    n = n + 1
            if n == len(cqa_list):
                print(re_question)
            i = 0

        workbook = xlwt.Workbook()
        sheet1 = workbook.add_sheet('行业库数据', cell_overwrite_ok=True)
        sheet1.write(0, 0, "question")
        sheet1.write(0, 1, "frequency")
        for j in range(0, len(cqa_list)):
            sheet1.write(j + 1, 0, cqa_list[j])
            sheet1.write(j + 1, 1, no_list[j])
        workbook.save(rootPath + '\\testdata\\apidata\\qamatcher\\' + final_result)


if __name__ == '__main__':
    test = GetQaMatcher()
    test.get_qa_matcher_result("http://192.168.26.105:30086/qastudio/v2/qamatch", "白癜风抽样50W.csv",
                               "qamatcher_test_result.xls")
    # test.get_caq("D:\\workspace\\kuaishang_auto\\testdata\\apidata\\qamatcher\\vitiligo.txt",
    #              "cqa_collection.xls")
# test.get_frequency("D:\\workspace\\kuaishang_auto\\testdata\\apidata\\qamatcher\\cqa_collection.xls",
#                    "D:\\workspace\\kuaishang_auto\\testdata\\apidata\\qamatcher\\qamatcher_test_result.xls",
#                    "qa_final_frequency_test_result.xls"
#                    )
