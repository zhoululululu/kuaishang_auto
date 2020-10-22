# -*- coding: UTF-8 -*-
'''
Created on 2020/10/12 10:31
@File  : get_finally_result.py
@author: ZL
@Desc  :
'''

# -*- coding: UTF-8 -*-
'''
Created on 2020/9/30 17:39
@File  : get_final_result.py
@author: ZL
@Desc  :
'''

from commonfunc.change_data_type import ChangeDataType
import os
import pandas
import ast
import time

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
            # print(temp)
            if dialog_id[i] != temp:
                # if dialog_id[i] == 4216:
                #     print(entity_l)
                relation_list.append(relation_l)
                entity_list.append(entity_l)
                dialog_list.append(temp)
                temp = dialog_id[i]
                relation_l, entity_l = [], []
            if "无需标注" not in entity_value_relationship[i]:
                entitys = entity_value_relationship[i].split("#")
                # if not str(entitys[0]).startswith("拥有子实体"):
                relation = entitys[1]
                # print(entitys[0], entitys[2])
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

        # print(dialog_list)
        return dialog_list, relation_list, entity_list

    def get_api_result_data(self, file):
        api_result = ChangeDataType.file_to_dict(rootPath + "\\testdata\\knowledgegraph\\relationship\\" + file)
        api_dialog_id = api_result.d_list.tolist()
        api_entity = api_result.e_list.tolist()
        api_relation = api_result.r_list.tolist()
        api_threshold = api_result.t_list.tolist()
        # print(api_dialog_id)
        return api_dialog_id, api_entity, api_relation, api_threshold

    def get_final_result(self, file1, file2):
        dialog_list, relation_list, entity_list = GetFinalResult.get_expect_result_data(self, file1)
        api_dialog_id, api_entity, api_relation, api_threshold = GetFinalResult.get_api_result_data(self, file2)
        # print(len(api_dialog_id), len(api_entity), len(api_relation), len(api_threshold))
        final_dialog_id, final_expect_relation_list, final_entity_list, final_threshold_list, final_api_relation_list = [], [], [], [], []
        for i in range(len(api_entity)):

            for j in range(len(ast.literal_eval(api_entity[i]))):
                try:
                    final_entity_list.append(ast.literal_eval(api_entity[i])[j])
                    final_threshold_list.append(ast.literal_eval(api_threshold[i])[j])
                    final_api_relation_list.append(ast.literal_eval(api_relation[i])[j])
                except Exception:
                    print(ast.literal_eval(api_entity[i]))
                    print(ast.literal_eval(api_threshold[i]))
        for i in range(len(api_dialog_id)):
            for j in ast.literal_eval(api_entity[i]):
                test_relation = "other"
                final_dialog_id.append(api_dialog_id[i])
                try:
                    if api_entity[i] != []:
                        # print("---------------dialog_id", dialog_list.index(api_dialog_id[i]))
                        # print("---------------entity", entity_list[dialog_list.index(api_dialog_id[i])])
                        # print(entity_list[dialog_list.index(api_dialog_id[i])])
                        # print(relation_list[dialog_list.index(api_dialog_id[i])])
                        if [j[0], j[1]] in entity_list[dialog_list.index(api_dialog_id[i])]:
                            # print("-----------", [j[0], j[1]])
                            test_relation = relation_list[dialog_list.index(api_dialog_id[i])][entity_list
                            [dialog_list.index(api_dialog_id[i])].index([j[0], j[1]])]
                            # print(test_relation)
                            # final_expect_relation_list.append(relation_list[i][entity_list
                            # [dialog_list.index(api_dialog_id[i])].index([j[0], j[1]])])
                        elif [j[1], j[0]] in entity_list[dialog_list.index(api_dialog_id[i])]:
                            # print([j[1], j[0]])
                            test_relation = relation_list[dialog_list.index(api_dialog_id[i])][entity_list
                            [dialog_list.index(api_dialog_id[i])].index([j[1], j[0]])]
                            # print(test_relation)
                            # final_expect_relation_list.append(relation_list[i][entity_list
                            # [dialog_list.index(api_dialog_id[i])].index([j[1], j[0]])])
                    #     else:
                    #         final_expect_relation_list.append("other")
                    # else:
                    #     final_expect_relation_list.append("other")
                except Exception as e:
                    print(j)
                final_expect_relation_list.append(test_relation)
        print(final_expect_relation_list)
        print(len(final_entity_list), len(final_threshold_list), len(final_api_relation_list),
              len(final_expect_relation_list))

        now = time.strftime('%y_%m_%d-%H_%M_%S')
        final_result_data = pandas.DataFrame(
            {"final_dialog_id": final_dialog_id, "entity_list": final_entity_list,
             "expect_relation": final_expect_relation_list,
             "api_relation": final_api_relation_list,
             "api_threshold": final_threshold_list})
        final_result_data.to_csv(rootPath + "\\testresults\\resultfile\\knowledgegraph\\" + now + "final_result_2.csv")


if __name__ == '__main__':
    GetFinalResult().get_final_result("result_more.csv", "20_10_11-04_56_33api_result_2.csv")
    # GetFinalResult().gettest()
