# -*- coding: UTF-8 -*-
'''
Created on 2020/8/18 14:08
@File  : get_test_data.py
@author: ZL
@Desc  :
'''

from commonfunc.change_data_type import ChangeDataType
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetTestData:

    @staticmethod
    def get_all_item_info():
        '''
        获取项目各个知识图谱的常规话术
        '''
        test_data = ChangeDataType.json_to_dict(rootPath + "\\testdata\\knowledgegraph\\" + "all_item_knowledge.json")
        return test_data

    @staticmethod
    def get_symptom_mapping():
        '''
        症状到项目的映射关系
        '''
        sy_test_data = ChangeDataType.json_to_dict(rootPath + "\\testdata\\knowledgegraph\\" + "sy.json")
        print(sy_test_data)
        # sym_list = list(test_data.keys())
        # item_list = list(test_data.values())
        # return sym_list, item_list
        return sy_test_data

    @staticmethod
    def get_item_mapping():
        '''
        项目到项目的实体对齐关系
        '''
        test_data = ChangeDataType.json_to_dict(rootPath + "\\testdata\\knowledgegraph\\" + "item_mapping.json")
        return test_data

    @staticmethod
    def get_cause_and_item():
        '''
        获取项目与病因的关系
        '''
        test_data, cause_list = {}, []
        all_data = ChangeDataType.csv_to_dict(
            rootPath + "\\testdata\\knowledgegraph\\" + "cause_item_mapping.csv")
        item = list(set(all_data.item.tolist()))
        for i in item:
            for j in all_data.values.tolist():
                if j[0] == i:
                    cause_list.append(j[1])
            test_data[i] = cause_list
            cause_list = []
        return test_data

    @staticmethod
    def get_entity_mapping(type_name=None):
        data = ChangeDataType.json_to_dict(rootPath + "\\testdata\\knowledgegraph\\" + "entity_mapping.json")
        cause_test_data = data["PROBABLE_CAUSE"]
        check_test_data = data["NEED_TO_CHECK"]
        treat_test_data = data["TREAT_BY_OTHER_WAY"]
        if type_name == "cause":
            return cause_test_data
        elif type_name == "check":
            return check_test_data
        elif type_name == "other_treat":
            return treat_test_data
        else:
            return cause_test_data, check_test_data, treat_test_data


if __name__ == '__main__':
    print(GetTestData().get_cause_and_item())
