# -*- coding: UTF-8 -*-
'''
Created on 2020/10/22 10:51
@File  : get_align_test.py
@author: ZL
@Desc  :
'''
from api.get_requests import GetRequests
from commonfunc.change_data_type import ChangeDataType
import os
from tqdm import tqdm

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class Align:

    # 有必要的话在用，取每个测试文件标签列表
    # def get_entity(self):
    #     test_data = ChangeDataType.file_to_dict(
    #         rootPath + "\\testdata\\knowledgegraph\\itemalign\\surgery.csv")
    #     all_entity = test_data.standard_entity.tolist()
    #     final_entity = set(all_entity)
    #     for i in final_entity:
    #         print(i)

    def get_align(self, test_target_file, test_data_file, result_file, target_result_file):
        GetRequests().get_request("http://192.168.1.79:8235/entity_align/v1", "GET", "othertreatment",
                                  "knowledgegraph\\itemalign\\" + test_target_file,
                                  "knowledgegraph\\itemalign\\" + test_data_file,
                                  ["sentence", "entity"], "standard_entity",
                                  result_file,
                                  target_result_file)


if __name__ == '__main__':
    # 其他的治疗方式
    # Align().get_align("othertreatment_target.txt", "othertreatment.csv",
    #                             "othertreatment_test_result.xls", "othertreatment_target_test_result.xls")

    # 症状
    # Align().get_align("symptom_target.txt", "symptom.csv",
    #                             "symptom_test_result.xls", "symptom_target_test_result.xls")

    # 项目
    # Align().get_align("item_target.txt", "item.csv",
    #                             "item_test_result.xls", "item_target_test_result.xls")

    # 病因
    # Align().get_align("cause_target.txt", "cause.csv",
    #                             "cause_test_result.xls", "cause_target_test_result.xls")

    # 手术
    Align().get_align("surgery_target.txt", "surgery.csv",
                      "surgery_test_result.xls", "surgery_target_test_result.xls")
