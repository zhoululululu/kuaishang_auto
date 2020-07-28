# -*- coding: UTF-8 -*-
'''
Created on 2020/5/12
@File  : test_get_item.py
@author: ZL
@Desc  :
'''
import pytest
import allure
from api.get_requests import GetRequests


class TestItem(object):

    @pytest.mark.beauty_item_test
    @allure.feature("项目识别")
    def test_get_item(self):
        GetRequests().get_request("http://192.168.1.74:8900/meal", "GET", "item", "beauty_item.txt",
                                  "est_for_request_item.csv", "sentence", "label",
                                  "beauty_test_result.xls")
