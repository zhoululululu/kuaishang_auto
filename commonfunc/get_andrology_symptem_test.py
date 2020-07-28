# -*- coding: UTF-8 -*-
'''
Created on 2020/7/14 15:05
@File  : get_andrology_symptem_test.py
@author: ZL
@Desc  :
'''

import requests
import time


class AndrologySymptomTest:

    def get_test(self):
        url = "http://10.13.8.230:8094/symptom_norm/v1?symptoms=有点长$有点痒$特别痒$红肿"
        i = 0
        while i < 10000:
            i += 0.1
            response = requests.get(url, timeout=10)
            result = response.json()
            symptom = result["norm_symptoms"]
            try:
                assert symptom == "不射精$下面痒$下面痒$红肿"
                time.sleep(0.1)
            except:
                raise Exception('实际结果与预期结果不一致，报错')


if __name__ == '__main__':
    AndrologySymptomTest().get_test()
