# -*- coding: UTF-8 -*-
'''
Created on 2020/10/21 15:13
@File  : get_relationship_discren.py
@author: ZL
@Desc  :
'''
from commonfunc.change_data_type import ChangeDataType
import os
from itertools import permutations
import requests

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetRelationshipDiscern:

    def get_permutations(self, origin_entity_list):
        entity_list, final_entity = [], []
        for i, j in permutations(origin_entity_list, 2):
            entity_list.append([i, j])
        return entity_list

    def get_test_data(self, file):
        testdata = ChangeDataType.file_to_dict(rootPath + "\\testdata\\knowledgegraph\\discern\\" + file,
                                               sheet_name="Sheet1")

        sentence_list = testdata.sentence.tolist()
        entity_list = testdata.entity.tolist()
        for i in range(len(sentence_list)):
            entity_list = GetRelationshipDiscern.get_permutations(self, entity_list)
            print(entity_list)


if __name__ == '__main__':
    GetRelationshipDiscern().get_test_data("dialog.xlsx")
