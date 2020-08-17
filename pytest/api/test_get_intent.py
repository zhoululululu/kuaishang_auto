# -*- coding: UTF-8 -*-
'''
Created on 2020/2/27
@File  : test_get_intent.py
@author: ZL
@Desc  :
'''

from api.get_requests import GetRequests
import pytest
import allure


class TestIntent(object):
    @pytest.mark.api_intention_test
    @allure.feature("测试环境通用意图识别")
    def test_get_pro_intent(self):
        # 意图测试
        # GetRequests().get_request("http://192.168.1.79:8900/intention/v2/skin", "GET", "skin_intent",
        #                           "intent\\dermatology\\target.txt",
        #                           "intent\\dermatology\\dermatology_test_data_3995.csv", ["sentence"], "label",
        #                           "dermatology_intention_test_result.xls",
        #                           "dermatology_intention_target_test_result.xls")
        # GetRequests().get_request("http://192.168.1.79:8905/intention/v2/infertility", "GET", "a_intent",
        #                           "intent\\infertility\\test_target.txt",
        #                           "intent\\infertility\\intention_to_test.csv", ["sentence"],
        #                           "label",
        #                           "infertility_intention_test_result.xls",
        #                           "infertility_intention_target_test_result.xls")
        # GetRequests().get_request("http://10.13.8.230:8204/intention/v2/anorectal", "GET", "a_intent",
        #                           "intent\\anorectal\\target.txt",
        #                           "intent\\anorectal\\anorectal_intention_to_test_4930.csv", ["sentence"],
        #                           "label",
        #                           "anorectal_intention_test_result.xls",
        #                           "anorectal_intention_target_test_result.xls")
        GetRequests().get_request("http://10.13.8.230:8098/andrology_intent/v2", "GET", "test_intent",
                                  "intent\\andrology\\target.txt",
                                  "intent\\andrology\\andrology_intent.csv", ["sentence"],
                                  "label",
                                  "andrology_intention_test_result.xls",
                                  "andrology_intention_target_test_result.xls")
        # GetRequests().get_request("http://192.168.1.79:8905/intention/v2/infertility", "GET", "a_intent",
        #                           "intent\\infertility\\test_target.txt",
        #                           "intent\\infertility\\intention_to_test.csv", ["sentence"],
        #                           "label",
        #                           "infertility_intention_test_result.xls",
        #                           "infertility_intention_target_test_result.xls")
        # GetRequests().get_request("http://192.168.1.79:8905/intention/v2/common", "GET", "a_intent",
        #                           "intent\\common\\common_intent.txt",
        #                           "intent\\common\\commo_intent_4000.csv", ["sentence"],
        #                           "label",
        #                           "obstetrics_intention_test_result.xls",
        #                           "obstetrics_intention_target_test_result.xls")
