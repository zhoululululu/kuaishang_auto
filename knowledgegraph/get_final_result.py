# -*- coding: UTF-8 -*-
'''
Created on 2020/9/30 17:39
@File  : get_final_result.py
@author: ZL
@Desc  :
'''

from commonfunc.change_data_type import ChangeDataType
import os
import json
import ast

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetFinalResult:
    def get_expect_result_data(self, file):
        temp = 401
        relation_list, relation_l = [], []
        entity_list, entity_l = [], []
        dialog_list = []
        test_list = []
        expect_result = ChangeDataType.file_to_dict(rootPath + "\\testdata\\knowledgegraph\\relationship\\" + file)
        entity_value_relationship = expect_result.entity_value_relationship.tolist()
        dialog_id = expect_result.dialog_id.tolist()
        for i in range(len(dialog_id)):
            if dialog_id[i] != temp:
                relation_list.append(relation_l)
                entity_list.append(entity_l)
                dialog_list.append(temp)
                temp = dialog_id[i]
                relation_l, entity_l = [], []
            if "无需标注" not in entity_value_relationship[i]:
                entitys = entity_value_relationship[i].split("#")
                relation = entitys[1]
                entity_1 = [entitys[0].split("@")[0], entitys[0].split("@")[1]]
                entity_2 = [entitys[2].split("@")[0], entitys[2].split("@")[1]]
                relation_l.append(relation)
                entity_l.append([entity_1, entity_2])
                test_list.append([entity_1, entity_2])
            else:
                relation_l = []
                entity_l = []
            if i == len(dialog_id) - 1:
                relation_list.append(relation_l)
                entity_list.append(entity_l)
                dialog_list.append(temp)
                temp = dialog_id[i]
                relation_l, entity_l = [], []
        return dialog_list, relation_list, entity_list

    def get_final_result(self, file1, file2):
        dialog_list, relation_list, entity_list = GetFinalResult.get_expect_result_data(self, file1)

        api_result = ChangeDataType.file_to_dict(rootPath + "\\testdata\\knowledgegraph\\relationship\\" + file2)
        api_entity = api_result.e_list.tolist()
        api_relation = api_result.r_list.tolist()
        api_threshold = api_result.t_list.tolist()

        new_re_list = []
        for i in range(len(api_entity)):
            new_relation_list = []
            print(api_entity[i])
            for j in ast.literal_eval(api_entity[i]):
                print(j)
                if j in entity_list[i]:
                    new_relation_list.append(relation_list[i][entity_list[i].index(j)])
                else:
                    new_relation_list.append("other")
            new_re_list.append(new_relation_list)
        print(len(new_relation_list))
        print(new_relation_list)


if __name__ == '__main__':
    GetFinalResult().get_final_result("result.csv", "20_10_11-04_56_33api_result_1.csv")
