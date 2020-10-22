# -*- coding: UTF-8 -*-
'''
Created on 2020/10/22 16:50
@File  : get_intention_test.py
@author: ZL
@Desc  :
'''
from api.get_requests import GetRequests
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetIntention:
    # 妇科
    def get_gynaecology(self):
        # 根据需求更替url
        # 测试环境:http://192.168.26.105:30014/gynaecology_intention/v1
        # 生产环境:http://10.13.8.230:8104/gynaecology_intention/v1
        GetRequests().get_request("http://192.168.26.105:30014/gynaecology_intention/v1", "GET", "pro_intent",
                                  "apidata\\intent\\gynaecology\\线上target.txt",
                                  "apidata\\intent\\gynaecology\\妇科-总测试数据-线上线下.csv",
                                  ["sentence", "False", "gynaecology"], "label",
                                  "gynaecology_intention_test_evn.xls",
                                  "gynaecology_intention_target_test_evn.xls")

    # 妇产科
    def get_obstetrics(self):
        # 根据需求更替url
        # 测试环境:http://192.168.26.105:30200/intention/v2/obstetrics
        # 生产环境:http://10.13.8.230:8200/intention/v2/obstetrics
        GetRequests().get_request("http://192.168.26.105:30200/intention/v2/obstetrics", "GET", "obstetrics",
                                  "\\apidata\\intent\\obstetrics\\obstetrics_target.txt",
                                  "\\apidata\\intent\\obstetrics\\obstetrics_to_test_9400.csv",
                                  ["sentence"],
                                  "label",
                                  "obstetrics_test_result.xls", "obstetrics_target_test_result.xls")


if __name__ == '__main__':
    # 妇科
    # GetIntention().get_gynaecology()

    # 妇产科
    GetIntention().get_obstetrics()
