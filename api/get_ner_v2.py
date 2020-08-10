# -*- coding: UTF-8 -*-
'''
Created on 2020/8/4 10:23
@File  : get_ner_v2.py
@author: ZL
@Desc  :
'''

import os
from commonfunc.change_data_type import ChangeDataType
import pandas as pd
import requests
from tqdm import tqdm
import time
from algorithm.algorithm_func import MultiClassByWord

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetNer:
#     def get_stander_testfile(self, test_data_file):
#         test_file = open(rootPath + "\\testdata\\apidata\\" + test_data_file, "w", encoding="utf-8")


    def get_ner_test(self, test_data_file, test_result_file):
        # GetNer.get_stander_testfile(self, test_data_file)
        test_data = ChangeDataType.file_to_dict(rootPath + "\\testdata\\apidata\\" + test_data_file)
        sentence_list, bio_list, sentence, re_bio_list, bio, bz_ner_list, word_list = [], [], [], [], [], [], []
        for i in range(1, len(test_data)):
            if len(test_data[i].strip()) != 0:
                # print(test_data[i])
                if test_data[i].strip().split("\t\t")[0] != '"':
                    if test_data[i].strip().split("\t\t")[0] != '“':
                        if test_data[i].strip().split("\t\t")[0] != '”':
                            sentence.append(test_data[i].strip().split("\t\t")[0])
                            bio.append(test_data[i].strip().split("\t\t")[1])
            else:
                sentence_list.append("".join(sentence))
                bio_list.append(bio)
                sentence, bio = [], []
        for j in tqdm(range(len(sentence_list))):
            params = {
                'utterance': sentence_list[j],
                'model_name': "nanfuke_embedding"
            }
            try:
                results = requests.get(url="http://192.168.1.74:8062/ner/v1", params=params)
                ner_bio = results.json()["data"]["bio"]
                for m in range(len(ner_bio)):
                    bz_ner_list.append(bio_list[j][m])
                    re_bio_list.append(ner_bio[m])
            except Exception as e:
                print(e)
        result_data = pd.DataFrame({"bz_bio": bz_ner_list, "re_bio": re_bio_list})
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        result_data.to_csv(rootPath + "\\testresults\\resultfile\\" + now + test_result_file)
        return bz_ner_list, re_bio_list

    def get_target(self, test_data_file, test_target_file, test_result_file, test_target_result_file):
        bz_bio_list, re_bio_list = GetNer.get_ner_test(self, test_data_file, test_result_file)
        # test_data = ChangeDataType.file_to_dict(rootPath + "\\testdata\\apidata\\" + "ner\\common\\testresult.csv")
        # bz_bio_list = test_data.bz_bio.tolist()
        # re_bio_list = test_data.re_bio.tolist()

        target_list = ChangeDataType().file_to_dict(rootPath + "\\testdata\\apidata\\" + test_target_file)
        precision_list, recall_list, f1_list, pn_list, rn_list, tn_list = MultiClassByWord.multi_each_target(self,
                                                                                                             target_list,
                                                                                                             bz_bio_list,
                                                                                                             re_bio_list)
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        test_result = pd.DataFrame(
            {"target": target_list, "标注数量": pn_list, "接口返回数量": rn_list, "一致数量": tn_list, "准确率": precision_list,
             "召回率": recall_list, "F1": f1_list})
        test_result.to_excel(rootPath + "\\testresults\\resultfile\\" + now + test_target_result_file)


if __name__ == '__main__':
    # 男妇科
    GetNer().get_target("ner\\gynaecology\\bio_char.txt", "ner\\gynaecology\\tag.txt",
                        "ner_gynaecology_testresult.csv",
                        "ner_gynaecology_target_testresult.xls")
    # 妇科 url:http://192.168.26.105:32060/ner/v1
    # GetNer().get_target("ner\\common\\common_mix.txt", "ner\\common\\mix_target.txt", "ner_testresult.csv",
    #                     "ner_target_testresult.xls")
    # 男科 url:http://192.168.26.105:32060/ner/v1
    # GetNer().get_target("ner\\common\\common_mix.txt", "ner\\common\\mix_target.txt", "ner_testresult.csv",
    #                     "ner_target_testresult.xls")