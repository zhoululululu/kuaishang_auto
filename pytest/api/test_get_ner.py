# -*- coding: UTF-8 -*-
'''
Created on 2020/4/1
@File  : test_get_ner.py
@author: ZL
@Desc  :妇科NER测试
'''

import pytest
import allure
from api.get_requests import GetRequests
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class TestNer(object):


    @pytest.mark.ner_apitest
    @allure.feature("Ner实体识别")
    def test_get_common_ner(self):
        GetRequests().get_request("http://192.168.1.74:8062/ner/v1", "GET", "ner", "ner\\gynaecology\\tag.txt",
                                  "ner\\gynaecology\\bio_char_result1.csv", ["sentence", "gynaecology"], "bio",
                                  "gynaecology_ner_test_result1.xls", "gynaecology_ner_target_test_result1.xls")
