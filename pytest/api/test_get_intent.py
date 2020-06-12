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
        GetRequests().get_request("http://192.168.1.74:8900/fuke_intention/new_39_v2", "GET", "intent",
                                  "intent\\gynaecology\\线上target.txt",
                                  "intent\\gynaecology\\妇科-总测试数据-线上线下.csv", ["sentence"], "label",
                                  "gynaecology_intention_test_result.xls",
                                  "gynaecology_intention_target_test_result.xls")
        # GetRequests().get_request("http://192.168.1.74:8900/fuke_intention/v1", "GET", "intent",
        #                           "intent\\gynaecology\\线上target.txt",
        #                           "intent\\gynaecology\\妇科-总测试数据-线上线下.csv", ["sentence"], "label",
        #                           "gynaecology_intention_test_result.xls",
        #                           "gynaecology_intention_target_test_result.xls")
