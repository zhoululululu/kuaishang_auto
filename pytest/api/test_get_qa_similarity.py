# -*- coding: UTF-8 -*-
'''
Created on 2020/4/13
@File  : test_get_qa_similarity.py
@author: ZL
@Desc  :
'''

import pytest
import allure
from api.get_requests import GetRequests


class TestQASimilarity(object):

    @pytest.mark.qa_similary_apitest
    @allure.feature("测试环境-男科FAQ相似度")
    def test_get_qa_similarity(self):
        GetRequests().get_request("http://192.168.1.79:8233/bert_similarity/v2", "GET", "qa_similary", "None",
                                  "similary\\qa_similary\\andrology_to_test.csv", ["sentence", "sentence2", "cos"],
                                  "label",
                                  "andrology_to_test_result.xls", "None")

    @pytest.mark.qa_similary_apitest
    @allure.feature("测试环境-医美FAQ相似度")
    def test_get_qa_similarity(self):
        GetRequests().get_request("http://192.168.1.79:8233/bert_similarity/v2", "GET", "qa_similary", "None",
                                  "similary\\qa_similary\\beauty_to_test.csv", ["sentence", "sentence2", "cos"],
                                  "label",
                                  "beauty_to_test_result.xls", "None")

    @pytest.mark.qa_similary_apitest
    @allure.feature("测试环境-癫痫FAQ相似度")
    def test_get_qa_similarity(self):
        GetRequests().get_request("http://192.168.1.79:8233/bert_similarity/v2", "GET", "qa_similary", "None",
                                  "similary\\qa_similary\\epilepsy_to_test.csv", ["sentence", "sentence2", "cos"],
                                  "label",
                                  "epilepsy_to_test_result.xls", "None")

    @pytest.mark.qa_similary_apitest
    @allure.feature("测试环境-不孕不育FAQ相似度")
    def test_get_qa_similarity(self):
        GetRequests().get_request("http://192.168.1.79:8233/bert_similarity/v2", "GET", "qa_similary", "None",
                                  "similary\\qa_similary\\infertility_to_test_5020.csv", ["sentence", "sentence2", "cos"],
                                  "label",
                                  "infertility_to_test_5020_result.xls", "None")

    @pytest.mark.qa_similary_apitest
    @allure.feature("测试环境-银屑病FAQ相似度")
    def test_get_qa_similarity(self):
        GetRequests().get_request("http://192.168.1.79:8233/bert_similarity/v2", "GET", "qa_similary", "None",
                                  "similary\\qa_similary\\psoriasis_to_test.csv", ["sentence", "sentence2", "cos"],
                                  "label",
                                  "psoriasis_to_test_result.xls", "None")

    @pytest.mark.qa_similary_apitest
    @allure.feature("测试环境-白癜风FAQ相似度")
    def test_get_qa_similarity(self):
        GetRequests().get_request("http://192.168.1.79:8233/bert_similarity/v2", "GET", "qa_similary", "None",
                                  "similary\\qa_similary\\vitiligo_to_test.csv", ["sentence", "sentence2", "cos"],
                                  "label",
                                  "vitiligo_to_test_result.xls", "None")
