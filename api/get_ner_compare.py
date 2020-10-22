# -*- coding: UTF-8 -*-
'''
Created on 2020/9/25 13:49
@File  : get_ner_compare.py
@author: ZL
@Desc  :
'''

from commonfunc.change_data_type import ChangeDataType
import requests
import os
import tqdm
import operator

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetNerCompare:

    def get_compare(self, industry, url1, url2, file):
        r1_list, r2_list = [], []
        test_data = ChangeDataType.file_to_dict(rootPath + "\\testdata\\apidata\\ner\\compare\\" + file)
        for idx, temp in test_data.iterrows():
            params = {
                'model_name': industry,
                'utterance': temp["question"]
            }
            try:
                r1 = requests.get(url1, params=params, timeout=50).json()
                r1_list.append(r1["data"])
                r2 = requests.get(url2, params=params, timeout=50).json()
                r2_list.append(r2["data"])

                if r1["data"] != r2["data"]:
                    print(temp["question"])
                    print("线上：", r1["data"])
                    print("线下：", r2["data"])

            except Exception:
                print(Exception)

        print(operator.eq(r1_list, r2_list))

    # def get_hair_tar(self,file):
    #     test_data = ChangeDataType.file_to_dict(rootPath + "\\testdata\\apidata\\intent\\hairtransplant\\" + file)
    #     target = set(test_data.label.tolist())
    #     for i in target:
    #         print(i)

if __name__ == '__main__':
    # GetNerCompare().get_hair_tar("hairtransplant_to_test_first_9998.csv")
    # cda
    GetNerCompare().get_compare("cda", "http://192.168.26.105:30060/ner/v1", "http://192.168.26.105:30220/ner/v1",
                                "cda.csv")
    # edupromotion
    # GetNerCompare().get_compare("edupromotion", "http://192.168.26.105:30060/ner/v1",
    #                             "http://192.168.26.105:30223/ner/v1",
    #                             "edupromotion.csv")

    # makeup
    # GetNerCompare().get_compare("makeup", "http://192.168.26.105:30060/ner/v1",
    #                             "http://192.168.26.105:30223/ner/v1",
    #                             "makeup.csv")

    # fiscal_and_taxation
    # GetNerCompare().get_compare("fiscal_and_taxation", "http://192.168.26.105:30060/ner/v1",
    #                             "http://192.168.26.105:30223/ner/v1",
    #                             "fiscal_and_taxation.csv")

    # purpura
    # GetNerCompare().get_compare("vitiligo", "http://192.168.26.105:30060/ner/v1",
    #                             "http://192.168.26.105:30210/ner/v1",
    #                             "purpura.csv")