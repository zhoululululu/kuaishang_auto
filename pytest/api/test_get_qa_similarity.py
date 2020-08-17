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
    @allure.feature("线上全科室")
    def test_get_qa_similarity(self):
        GetRequests().get_request("http://192.168.1.79:32088/without_bert_similarity/v2/sim", "GET", "jh_similary", "None",
                                  "similary\\all\\first_test_23202.csv", ["sentence1", "sentence2"],
                                  "label",
                                  "全科室（23202）测试结果.xls", "None")
        GetRequests().get_request("http://192.168.1.79:32088/without_bert_similarity/v2/sim", "GET", "jh_similary", "None",
                                  "similary\\all\\second_test_30000.csv", ["sentence1", "sentence2"],
                                  "label",
                                  "全科室（30000）测试结果.xls", "None")
        GetRequests().get_request("http://192.168.1.79:32088/without_bert_similarity/v2/sim", "GET", "jh_similary", "None",
                                  "similary\\all\\origin_test_21753.csv", ["sentence1", "sentence2"],
                                  "label",
                                  "全科室（21753）测试结果.xls", "None")

    # @pytest.mark.qa_similary_apitest
    # @allure.feature("测试环境-医美FAQ相似度")
    # def test_get_qa_similarity(self):
    #     GetRequests().get_request("http://192.168.1.79:8233/bert_similarity/v2", "GET", "qa_similary", "None",
    #                               "similary\\qa_similary\\beauty_to_test.csv", ["sentence", "sentence2", "cos"],
    #                               "label",
    #                               "beauty_to_test_result.xls", "None")
    #
    # @pytest.mark.qa_similary_apitest
    # @allure.feature("测试环境-癫痫FAQ相似度")
    # def test_get_qa_similarity(self):
    #     GetRequests().get_request("http://192.168.1.79:8233/bert_similarity/v2", "GET", "qa_similary", "None",
    #                               "similary\\qa_similary\\epilepsy_to_test.csv", ["sentence", "sentence2", "cos"],
    #                               "label",
    #                               "epilepsy_to_test_result.xls", "None")
    #
    # @pytest.mark.qa_similary_apitest
    # @allure.feature("测试环境-不孕不育FAQ相似度")
    # def test_get_qa_similarity(self):
    #     GetRequests().get_request("http://192.168.1.79:8233/bert_similarity/v2", "GET", "qa_similary", "None",
    #                               "similary\\qa_similary\\infertility_to_test_5020.csv", ["sentence", "sentence2", "cos"],
    #                               "label",
    #                               "infertility_to_test_5020_result.xls", "None")
    #
    # @pytest.mark.qa_similary_apitest
    # @allure.feature("测试环境-银屑病FAQ相似度")
    # def test_get_qa_similarity(self):
    #     GetRequests().get_request("http://192.168.1.79:8233/bert_similarity/v2", "GET", "qa_similary", "None",
    #                               "similary\\qa_similary\\psoriasis_to_test.csv", ["sentence", "sentence2", "cos"],
    #                               "label",
    #                               "psoriasis_to_test_result.xls", "None")
    #
    # @pytest.mark.qa_similary_apitest
    # @allure.feature("测试环境-白癜风FAQ相似度")
    # def test_get_qa_similarity(self):
    #     GetRequests().get_request("http://192.168.1.79:8233/bert_similarity/v2", "GET", "qa_similary", "None",
    #                               "similary\\qa_similary\\vitiligo_to_test.csv", ["sentence", "sentence2", "cos"],
    #                               "label",
    #                               "vitiligo_to_test_result.xls", "None")
