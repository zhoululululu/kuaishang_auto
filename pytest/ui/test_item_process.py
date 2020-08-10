# -*- coding: UTF-8 -*-
'''
Created on 2020/3/6
@File  : test_item_process.py
@author: ZL
@Desc  :
'''
import pytest
from ui.item_process import ItemProcess


class TestItemProcess(object):

    def __init__(self):
        self.url = "http://tkfk.kuaishang.cn/bs/im.htm?cas=117576___665228&fi=120040"
        self.file = "耳鼻喉测试相关.xlsx"
        self.dialog_result_file = "1dialog_test_result.xls"
        self.comp_result_file = "1comp_dialog_test_result.xls"

    @pytest.mark.webtest
    def test_item_process(self):
        '''验证测试流程'''
        ItemProcess().item_process(self.url, self.file, self.dialog_result_file, self.comp_result_file)

