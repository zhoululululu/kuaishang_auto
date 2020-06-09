# -*- coding: UTF-8 -*-
'''
Created on 2020/2/26
@File  : test_get_symptom_similarity.py
@author: ZL
@Desc  :
'''

import pytest
import allure
from api.get_requests import GetRequests


class TestSymptomSimilarity(object):

    # @pytest.mark.apitest
    # @allure.feature("测试环境症状相似度")
    # def test_get_symptom_similarity(self):
    #     GetRequests().get_request("http://192.168.1.74:8999/symptom_similarity/v1", "GET", "symptom_similary",
    #                               "None",
    #                               "item\\test_for_request_symptom_similary.csv", ["症状a", "症状b"], "label",
    #                               "symptom_similary_test_result.xls", "None")

    @pytest.mark.similary_apitest
    @allure.feature("测试环境症状相似度")
    def test_get_symptom_similarity(self):
        GetRequests().get_request("http://192.168.1.74:8999/symptom_similarity/v1", "GET", "symptom_similary",
                                  "None",
                                  "similary\\gynaecology_sym_test_1740.csv", "sentence", "label",
                                  "gynaecology_symptom_similary_test_result.xls", "None")
