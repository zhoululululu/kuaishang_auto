# -*- coding: UTF-8 -*-
'''
Created on 2020/6/11
@File  : test_result_for_api.py
@author: ZL
@Desc  :
'''

import requests
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class ApiTest:

    @staticmethod
    def api_test():
        request_url = "http://192.168.1.74:8930/fuke_intention/new_39_v5"

        herder = {
            "Connection": "keep-alive",
            "Content_type": "multipart/form-data; application/octet-stream"
        }

        params = {
            "url": request_url
        }

        r = requests.get(url="http://192.168.120.6:8892/test_test_result/download", headers=herder, data=params,
                         timeout=999999)
        fp = open(rootPath + "\\testresults\\resultfile\\test_result.xlsx", "wb")
        fp.write(r.content)
        fp.close()


if __name__ == '__main__':
    ApiTest().api_test()
