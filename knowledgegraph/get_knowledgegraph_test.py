# -*- coding: UTF-8 -*-
'''
Created on 2020/9/23 18:09
@File  : get_knowledgegraph_test.py
@author: ZL
@Desc  :
'''
import json
from commonfunc.change_data_type import ChangeDataType
from itertools import permutations
import os
import math
import tqdm
import requests
import pandas
import time
import profile

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetKnowledgeGraph:
    def __init__(self):
        self.len_list = []
        self.test = 0

    def get_test_data(self, file):
        all_data = ChangeDataType.file_to_dict(rootPath + "\\testdata\\knowledgegraph\\relationship\\" + file)
        pre_post = ['virus', 'physiology', 'cause', 'check', 'fluid', 'symptom', 'part', 'othertreatment', 'tool',
                    'surgery', 'item', "foodtherapy"]
        sentence_list, sentence_l = [], []
        dialog_id_list, dialog_id_l = [], []
        entity_list, entity_l = [], []
        test_list = []
        temp = 401
        all_sentence = all_data.sentence.tolist()
        all_dialog_id = all_data.dialog_id.tolist()
        all_entity = all_data.entity.tolist()
        for i in range(len(all_sentence)):
            if all_dialog_id[i] != temp:
                dialog_id_list.append(temp)
                sentence_list.append(sentence_l)
                # test_list += GetKnowledgeGraph.get_ner_combinations(self, list(set(entity_l)))
                entity_list.append(GetKnowledgeGraph.get_ner_combinations(self, list(set(entity_l))))
                temp = all_dialog_id[i]
                entity_l, sentence_l = [], []
            sentence_l.append(all_sentence[i])
            entitys = eval((all_entity[i].replace("， ", ",")))
            if entitys != "{}":
                for i in entitys:
                    if i in pre_post:
                        if len(entitys[i]) > 1:
                            for j in entitys[i]:
                                entity = (i, j)
                                entity_l.append(entity)
                        else:
                            entity = (i, entitys[i][0])
                            entity_l.append(entity)
            if i == len(all_dialog_id) - 1:
                dialog_id_list.append(temp)
                sentence_list.append(sentence_l)
                entity_list.append(GetKnowledgeGraph.get_ner_combinations(self, list(set(entity_l))))
                # test_list += GetKnowledgeGraph.get_ner_combinations(self, list(set(entity_l)))
                entity_l, sentence_l = [], []
                temp = all_dialog_id[i]
        # print("----------------", max(self.len_list))
        # print(max(self.len_list), self.len_list.index(max(self.len_list)),
        #       self.len_list[self.len_list.index(max(self.len_list))], dialog_id_list[520], self.len_list[520])
        # print(len(test_list))
        return sentence_list, dialog_id_list, entity_list

    def get_ner_combinations(self, enrity_list):
        entity_list, final_entity = [], []
        for i, j in permutations(enrity_list, 2):
            entity_list.append([i, j])
        filter_dict = {
            "part": ["item", "symptom"],
            "symptom": ["item", "physiology", "fluid"],
            "virus": ["item", "symptom"],
            "cause": ["item", "surgery", "symptom"],
            "check": ["item", "symptom"],
            "surgery": ["item", "symptom"],
            "foodtherapy": ["item", "symptom"],
            "othertreatment": ["item", "symptom"],
            "tool": ["item", "symptom", "surgery"],
        }
        self.test += 1
        for i in entity_list:
            for key in filter_dict.keys():
                if (i[1][0] in filter_dict[key] and i[0][0] == key) or (i[0][0] in filter_dict[key] and i[1][0] == key):
                    final_entity.append(i)
                    break
        self.len_list.append(len(final_entity))
        # if len(final_entity) == 1449:
        #     print(len(final_entity))
        return final_entity

    def get_request(self, file, expect_result_file):
        final_expect_entity_list, final_expect_relation_list, final_result_entity_list, final_result_relation_list, threshold_list = [], [], [], [], []
        expect_dialog_list, expect_relation_list, expect_entity_list = GetKnowledgeGraph.get_expect_result_data(self,
                                                                                                                expect_result_file)
        sentence_list, dialog_id_list, entity_list = GetKnowledgeGraph.get_test_data(self, file)
        for i in range(len(dialog_id_list)):
            for j in entity_list[i]:
                url = "http://192.168.120.19:8911/relation/v1"
                param = {
                    "dialog": sentence_list[i],
                    "entity_list": [j[0], j[1]]
                }
                try:
                    test = requests.post(url=url, params=param, timeout=50)
                    result = test.json()
                    re_origin_relation = result["data"]["relation"]
                    threshold = result["data"]["intent_probability"]
                    re_relation_label = re_origin_relation.split("_")[0]
                    print([j[0], j[1]], re_relation_label, threshold)
                except Exception:
                    print(Exception)
                    threshold = 0
                    re_relation_label = "other"
                ex_relation = []
                if expect_entity_list[i] == [[]]:
                    ex_relation.appen("other")
                else:
                    for m in range(len(expect_entity_list[i]) - 1):
                        if set(expect_entity_list[i][m]) == set([j[0], j[1]]):
                            ex_relation.append(expect_relation_list[i][m])
                            break
                        else:
                            ex_relation.append("other")
                if len(set(ex_relation)) > 1:
                    for k in ex_relation:
                        if k != "other":
                            expect_relation = k
                else:
                    expect_relation = "other"
                final_result_entity_list.append([j[0], j[1]])
                final_result_relation_list.append(re_relation_label)
                final_expect_relation_list.append(expect_relation)
                threshold_list.append(threshold)

                # print(dialog_id_list[i], [j[0], j[1]], expect_relation, re_relation_label)
        result_data = pandas.DataFrame(
            {"接口实体信息": final_result_entity_list, "预期关系": final_expect_relation_list, "实际关系": final_result_relation_list,
             "阈值": threshold_list})
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        result_data.to_excel(
            rootPath + "\\testresults\\resultfile\\knowledgegraph\\relationship\\" + now + "relationship.xls")

    def get_request2(self, file, expect_result_file):
        final_expect_entity_list, final_expect_relation_list, final_result_entity_list, final_result_relation_list, threshold_list = [], [], [], [], []
        # expect_dialog_list, expect_relation_list, expect_entity_list = GetKnowledgeGraph.get_expect_result_data(self,
        #                                                                                                         expect_result_file)

        t_list, e_list, r_list, d_list = [], [], [], []
        sentence_list, dialog_id_list, entity_list = GetKnowledgeGraph.get_test_data(self, file)

        for i in range(len(dialog_id_list)):
            if len(entity_list[i]) <= 400:
                long_entity_list = [entity_list[i]]
            elif len(entity_list[i]) > 400 and len(entity_list[i]) <= 800:
                long_entity_list = [
                    entity_list[i][:math.ceil(len(entity_list[i]) / 2)],
                    entity_list[i][math.ceil(len(entity_list[i]) / 2):]]
            elif len(entity_list[i]) > 800 and len(entity_list[i]) <= 1200:
                long_entity_list = [
                    entity_list[i][:math.ceil(len(entity_list[i]) / 3)],
                    entity_list[i][math.ceil(len(entity_list[i]) / 3):math.ceil(len(entity_list[i]) / 3 * 2)],
                    entity_list[i][math.ceil(len(entity_list[i]) / 3):]]
            elif len(entity_list[i]) > 1200:
                long_entity_list = [
                    entity_list[i][:math.ceil(len(entity_list[i]) / 4)],
                    entity_list[i][math.ceil(len(entity_list[i]) / 4):math.ceil(len(entity_list[i]) / 2)],
                    entity_list[i][math.ceil(len(entity_list[i]) / 2):math.ceil(len(entity_list[i]) / 4 * 3)],
                    entity_list[i][math.ceil(len(entity_list[i]) / 4 * 3):]]
            for m in long_entity_list:
                url = "http://192.168.120.19:8911/relation/v1"
                param = {
                    "dialog": sentence_list[i],
                    "entity_list": m
                }
                try:
                    test = requests.post(url=url, params=json.dumps(param, ensure_ascii=False), timeout=50000)
                    result = test.json()
                    re_origin_relation = result["data"]["relation"]
                    threshold = result["data"]["probability"]
                except Exception:
                    print(Exception)
                    threshold = "error"
                    re_origin_relation = "error"
                d_list.append(dialog_id_list[i])
                t_list.append(threshold)
                r_list.append(re_origin_relation)
                e_list.append(m)
                print(dialog_id_list[i])
        result_data = pandas.DataFrame(
            {"d_list": d_list, "e_list": e_list, "r_list": r_list,
             "t_list": t_list})
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        result_data.to_csv(
            rootPath + "\\testresults\\resultfile\\knowledgegraph\\relationship\\" + now + "api_result.csv")

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
                entity_1 = (entitys[0].split("@")[0], entitys[0].split("@")[1])
                entity_2 = (entitys[2].split("@")[0], entitys[2].split("@")[1])
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


#
# def get_test(self):
#     result = []
#     list1 = [(('item', '阳痿'), ('cause', '频繁的手淫')), (('item', '阳痿'), ('physiology', '勃起')), (('item', '阳痿'), ('cause', '长期的手淫')), (('item', '阳痿'), ('symptom', '射的也快')), (('item', '阳痿'), ('symptom', '不坚不久')), (('item', '阳痿'), ('symptom', '龟头神经特别敏感')), (('item', '阳痿'), ('symptom', '血流不足')), (('item', '阳痿'), ('item', '早泄')), (('item', '阳痿'), ('symptom', '龟头神经敏感')), (('item', '阳痿'), ('symptom', '性生活中途疲软')), (('item', '阳痿'), ('symptom', '海绵体有损伤')), (('item', '阳痿'), ('symptom', '没以前硬了')), (('item', '阳痿'), ('item', '肾虚')), (('cause', '频繁的手淫'), ('physiology', '勃起')), (('cause', '频繁的手淫'), ('cause', '长期的手淫')), (('cause', '频繁的手淫'), ('symptom', '射的也快')), (('cause', '频繁的手淫'), ('symptom', '不坚不久')), (('cause', '频繁的手淫'), ('symptom', '龟头神经特别敏感')), (('cause', '频繁的手淫'), ('symptom', '血流不足')), (('cause', '频繁的手淫'), ('item', '早泄')), (('cause', '频繁的手淫'), ('symptom', '龟头神经敏感')), (('cause', '频繁的手淫'), ('symptom', '性生活中途疲软')), (('cause', '频繁的手淫'), ('symptom', '海绵体有损伤')), (('cause', '频繁的手淫'), ('symptom', '没以前硬了')), (('cause', '频繁的手淫'), ('item', '肾虚')), (('physiology', '勃起'), ('cause', '长期的手淫')), (('physiology', '勃起'), ('symptom', '射的也快')), (('physiology', '勃起'), ('symptom', '不坚不久')), (('physiology', '勃起'), ('symptom', '龟头神经特别敏感')), (('physiology', '勃起'), ('symptom', '血流不足')), (('physiology', '勃起'), ('item', '早泄')), (('physiology', '勃起'), ('symptom', '龟头神经敏感')), (('physiology', '勃起'), ('symptom', '性生活中途疲软')), (('physiology', '勃起'), ('symptom', '海绵体有损伤')), (('physiology', '勃起'), ('symptom', '没以前硬了')), (('physiology', '勃起'), ('item', '肾虚')), (('cause', '长期的手淫'), ('symptom', '射的也快')), (('cause', '长期的手淫'), ('symptom', '不坚不久')), (('cause', '长期的手淫'), ('symptom', '龟头神经特别敏感')), (('cause', '长期的手淫'), ('symptom', '血流不足')), (('cause', '长期的手淫'), ('item', '早泄')), (('cause', '长期的手淫'), ('symptom', '龟头神经敏感')), (('cause', '长期的手淫'), ('symptom', '性生活中途疲软')), (('cause', '长期的手淫'), ('symptom', '海绵体有损伤')), (('cause', '长期的手淫'), ('symptom', '没以前硬了')), (('cause', '长期的手淫'), ('item', '肾虚')), (('symptom', '射的也快'), ('symptom', '不坚不久')), (('symptom', '射的也快'), ('symptom', '龟头神经特别敏感')), (('symptom', '射的也快'), ('symptom', '血流不足')), (('symptom', '射的也快'), ('item', '早泄')), (('symptom', '射的也快'), ('symptom', '龟头神经敏感')), (('symptom', '射的也快'), ('symptom', '性生活中途疲软')), (('symptom', '射的也快'), ('symptom', '海绵体有损伤')), (('symptom', '射的也快'), ('symptom', '没以前硬了')), (('symptom', '射的也快'), ('item', '肾虚')), (('symptom', '不坚不久'), ('symptom', '龟头神经特别敏感')), (('symptom', '不坚不久'), ('symptom', '血流不足')), (('symptom', '不坚不久'), ('item', '早泄')), (('symptom', '不坚不久'), ('symptom', '龟头神经敏感')), (('symptom', '不坚不久'), ('symptom', '性生活中途疲软')), (('symptom', '不坚不久'), ('symptom', '海绵体有损伤')), (('symptom', '不坚不久'), ('symptom', '没以前硬了')), (('symptom', '不坚不久'), ('item', '肾虚')), (('symptom', '龟头神经特别敏感'), ('symptom', '血流不足')), (('symptom', '龟头神经特别敏感'), ('item', '早泄')), (('symptom', '龟头神经特别敏感'), ('symptom', '龟头神经敏感')), (('symptom', '龟头神经特别敏感'), ('symptom', '性生活中途疲软')), (('symptom', '龟头神经特别敏感'), ('symptom', '海绵体有损伤')), (('symptom', '龟头神经特别敏感'), ('symptom', '没以前硬了')), (('symptom', '龟头神经特别敏感'), ('item', '肾虚')), (('symptom', '血流不足'), ('item', '早泄')), (('symptom', '血流不足'), ('symptom', '龟头神经敏感')), (('symptom', '血流不足'), ('symptom', '性生活中途疲软')), (('symptom', '血流不足'), ('symptom', '海绵体有损伤')), (('symptom', '血流不足'), ('symptom', '没以前硬了')), (('symptom', '血流不足'), ('item', '肾虚')), (('item', '早泄'), ('symptom', '龟头神经敏感')), (('item', '早泄'), ('symptom', '性生活中途疲软')), (('item', '早泄'), ('symptom', '海绵体有损伤')), (('item', '早泄'), ('symptom', '没以前硬了')), (('item', '早泄'), ('item', '肾虚')), (('symptom', '龟头神经敏感'), ('symptom', '性生活中途疲软')), (('symptom', '龟头神经敏感'), ('symptom', '海绵体有损伤')), (('symptom', '龟头神经敏感'), ('symptom', '没以前硬了')), (('symptom', '龟头神经敏感'), ('item', '肾虚')), (('symptom', '性生活中途疲软'), ('symptom', '海绵体有损伤')), (('symptom', '性生活中途疲软'), ('symptom', '没以前硬了')), (('symptom', '性生活中途疲软'), ('item', '肾虚')), (('symptom', '海绵体有损伤'), ('symptom', '没以前硬了')), (('symptom', '海绵体有损伤'), ('item', '肾虚')), (('symptom', '没以前硬了'), ('item', '肾虚'))]
#
#     # for i in  list1:
#     #     for j in i:
#     #         result.append(j)
#     print(len(list1))


if __name__ == '__main__':
    GetKnowledgeGraph().get_request2("dialog.csv", "result.csv")
# profile.run('GetKnowledgeGraph().get_expect_result_data("result.csv")')
# profile.run('GetKnowledgeGraph().get_expect_result_data("result.csv")')
# sentence_list, dialog_id_list, entity_list = GetKnowledgeGraph().get_test_data("dialog.csv")
#
# print(len(entity_list))
# dialog_list, relation_list, entity_list = GetKnowledgeGraph().get_expect_result_data("result.csv")
# print(len(list(relation_list)))
# print(relation_list)
# GetKnowledgeGraph().get_ner_combinations("")
