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


class TestNer(object):

    @pytest.mark.apitest
    @allure.feature("Ner实体识别")
    def test_get_common_ner(self):
        GetRequests().get_request("http://192.168.1.18:32060/ner/v1", "GET", "ner", "ner\\tag.txt",
                                  "item\\test_for_request_ner.csv", ["sentence", "all_area"], "bio",
                                  "ner_test_result.xls", "ner_target_test_result.xls")
