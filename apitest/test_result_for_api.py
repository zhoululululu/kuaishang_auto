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
        request_url = "http://192.168.120.37:8911/gynaecology_intention/v1"
        industry = "妇科"
        herder = {
            "Connection": "keep-alive",
            "Content_type": "multipart/form-data; application/octet-stream"
        }

        params = {
            "url": request_url,
            "industry": industry
        }
        r = requests.get(url="http://192.168.120.67:8895/test_test_result/download", headers=herder, data=params,
                         timeout=999999)
        fp = open(rootPath + "\\testresults\\resultfile\\1test_result.xlsx", "wb")
        fp.write(r.content)
        fp.close()


if __name__ == '__main__':
    ApiTest().api_test()
