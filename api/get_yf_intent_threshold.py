# -*- coding: UTF-8 -*-
'''
Created on 2020/7/10 13:38
@File  : get_yf_intent_threshold.py
@author: ZL
@Desc  :
'''

import os
from commonfunc.change_data_type import ChangeDataType
from commonfunc.common_function import CommonFunction
from algorithm.algorithm_func import MultiClassByWord
import pandas as pd
import time

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class Get_intention_threshold:

    def get_threshold(self, test_result_file):
        test_data = ChangeDataType.excel_to_dict(
            rootPath + '\\testresults\\resultfile\\' + "20_07_10-11_37_03infertility_intention_test.xls",
            sheet_name="Sheet1")
        re_intent_new_l, re_score_new_l, re_intent_new, bz_new_l = [], [], [], []
        alpha_list, p_list, r_list, f_list, pn_list, rn_list, tn_list = [], [], [], [], [], [], []
        bz_list = test_data.label.tolist()
        re_intent_list = test_data.re_intent.tolist()
        re_score_list = test_data.re_score.tolist()
        #
        # for i in range(len(bz_list)):
        #     if re_intent_list[i] == "咨询手术":
        #         bz_new_l.append(bz_list[i])
        #         re_intent_new_l.append(re_intent_list[i])
        #         re_score_new_l.append(re_score_list[i])
        # print(len(re_intent_new_l))
        # print(re_intent_new_l)
        # print(re_score_new_l)
        i, n = 0, 0
        while (i < 0.99):
            n += 1
            i += 0.01
            for j in range(0, len(re_score_list)):
                if re_intent_list[j] == "咨询手术":
                    re_score = CommonFunction.get_re_score(re_score_list[j], i)
                    if re_score == 1:
                        re_intent_new.append("咨询手术")
                    else:
                        re_intent_new.append("无")
                else:
                    re_intent_new.append(re_intent_list[j])
            p, r, f1, pn, rn, tn = MultiClassByWord.class_target(self, bz_list, re_intent_new, "咨询手术")
            alpha_list.append(i)
            p_list.append(p)
            r_list.append(r)
            f_list.append(f1)
            pn_list.append(pn)
            rn_list.append(rn)
            tn_list.append(tn)
            p, r, f1, pn, rn, tn = 0, 0, 0, 0, 0, 0
            re_intent_new, re_score = [], []
        final_data = pd.DataFrame(
            {"阈值": alpha_list, "人工标注数量": pn_list, "接口结果数量": rn_list, "一致数量": tn_list, "准确率": p_list,
             "召回率": r_list, "F1值": f_list})
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        final_data.to_excel(rootPath + '\\testresults\\resultfile\\' + now + test_result_file)


if __name__ == '__main__':
    Get_intention_threshold().get_threshold("咨询手术全参数.xls")
