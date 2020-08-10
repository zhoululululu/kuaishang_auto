# -*- coding: UTF-8 -*-
'''
Created on 2020/3/13
@File  : algorithm_func.py
@author: ZL
@Desc  : 算法prf值
'''
from sklearn import metrics
from sklearn.metrics import auc
import pandas as pd
from commonfunc.change_data_type import ChangeDataType
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class Binary:

    @staticmethod
    def get_auc(truth_value, prob_value):
        fpr, tpr, threshold = metrics.roc_curve(truth_value, prob_value)
        re_auc = auc(fpr, tpr)
        return re_auc, fpr, tpr

    @staticmethod
    def get_binary_score(bz_list, re_list):
        """
        传入标注内容
        :param bz_list: 人工标注数据
        :param re_list：接口返回数据
        :return P, R, F1, accuracy：对应的测试指标
        """
        count_all_p = 0
        count_p = 0
        count_all_r = 0
        count_r = 0
        acc_num = 0
        mis_num, zero_num = 0, 0
        for i in range(0, len(bz_list)):
            if bz_list[i] == 1:
                count_all_r += 1
                if bz_list[i] == re_list[i]:
                    count_r += 1
            if re_list[i] == 1:
                count_all_p += 1
                if re_list[i] == bz_list[i]:
                    count_p += 1
            if bz_list[i] == re_list[i]:
                acc_num += 1
            if bz_list[i] == 0:
                zero_num += 1
                if re_list[i] == 1:
                    mis_num += 1

        P = count_p / count_all_p
        R = count_r / count_all_r
        F1 = 2 * P * R / (P + R)
        mis_rate = mis_num / zero_num
        accuracy = acc_num / len(bz_list)
        print(P, R, F1, mis_num, zero_num)
        return P, R, F1, accuracy, mis_rate

    @staticmethod
    def binary_plot_curve(truth_value, prob_value):
        precision, recall, f1, accuracy, misrate = Binary.get_binary_score(truth_value, prob_value)
        print("召回率R为：", recall)
        print("准确率P为：", precision)
        print("F1值为：", f1)
        print("Accuracy值为：", accuracy)
        print("误判率为：", misrate)


class MultiClassByWord:
    def class_target_for_ner(self, bz_intent_list, re_intent_list, point):
        """
        传入标注内容
        :param bz_list: 人工标注数据
        :param re_list：接口返回数据
        :param point：标签值（可为单分类或多分类）
        :return P, R, F1, accuracy：对应的测试指标
        """
        result = list(zip(bz_intent_list, re_intent_list))
        f1, p, r, count_all_p, count_p, count_all_r, count_r = 0, 0, 0, 0, 0, 0, 0
        for res in result:
            bz_bio = res[0]  # 人工标注
            re_bio = res[1]  # 接口返回
            if point in bz_bio:
                count_all_r = count_all_r + 1
                if point in re_bio:
                    count_r = count_r + 1
            if point in re_bio:
                count_all_p = count_all_p + 1
                if point in bz_bio:
                    count_p = count_p + 1
        if count_all_p != 0 and count_all_r != 0:
            p = count_p / count_all_p
            r = count_r / count_all_r
            if p != 0 and r != 0:
                f1 = 2 * p * r / (p + r)
        else:
            p = 0
            r = 0
            f1 = 0
        return p, r, f1, count_all_r, count_all_p, count_r
    # 得出每个分类的prf值
    def class_target(self, bz_intent_list, re_intent_list, point):
        """
        传入标注内容
        :param bz_list: 人工标注数据
        :param re_list：接口返回数据
        :param point：标签值（可为单分类或多分类）
        :return P, R, F1, accuracy：对应的测试指标
        """
        result = list(zip(bz_intent_list, re_intent_list))
        f1, p, r, count_all_p, count_p, count_all_r, count_r = 0, 0, 0, 0, 0, 0, 0
        for res in result:
            bz_bio = res[0]  # 人工标注
            re_bio = res[1]  # 接口返回
            if point == bz_bio:
                count_all_r = count_all_r + 1
                if point == re_bio:
                    count_r = count_r + 1
            if point == re_bio:
                count_all_p = count_all_p + 1
                if point == bz_bio:
                    count_p = count_p + 1
        if count_all_p != 0 and count_all_r != 0:
            p = count_p / count_all_p
            r = count_r / count_all_r
            if p != 0 and r != 0:
                f1 = 2 * p * r / (p + r)
        else:
            p = 0
            r = 0
            f1 = 0
        return p, r, f1, count_all_r, count_all_p, count_r

    # 直接算出平均召回率，准确率，F1值
    def ave_target(self, bz_intent_list, re_intent_list, point):
        result = list(zip(bz_intent_list, re_intent_list))
        count_all_p, count_p, count_all_r, count_r, p, r, f1 = 0, 0, 0, 0, 0, 0, 0
        for res in result:
            bz_bio = res[0]  # 人工标注
            re_bio = res[1]  # 接口返回
            if bz_bio != point:
                count_all_r += 1
                if bz_bio == re_bio:
                    count_r += 1
            if re_bio != point:
                count_all_p += 1
                if re_bio == bz_bio:
                    count_p += 1
        if count_all_p != 0 and count_all_r != 0:
            p = count_p / count_all_p
            r = count_r / count_all_r
            if p != 0 and r != 0:
                f1 = 2 * p * r / (p + r)
        else:
            p = 0
            r = 0
            f1 = 0
        return p, r, f1, count_all_r, count_all_p, count_r

    def mult_class_target(self, bz_intent_list, re_intent_list, point):
        f1 = 0
        result = list(zip(bz_intent_list, re_intent_list))
        count_all_p = 0
        count_p = 0
        count_all_r = 0
        count_r = 0
        for res in result:
            bz_bio = res[0]  # 人工标注
            re_bio = res[1]  # 接口返回
            if point in bz_bio:
                count_all_r = count_all_r + 1
                if point in re_bio:
                    count_r = count_r + 1
            if point in re_bio:
                count_all_p = count_all_p + 1
                if point in bz_bio:
                    count_p = count_p + 1
        if count_all_p != 0 and count_all_r != 0:
            p = count_p / count_all_p
            r = count_r / count_all_r
            if p != 0 and r != 0:
                f1 = 2 * p * r / (p + r)
        else:
            p = 0
            r = 0
            f1 = 0
        return p, r, f1, count_all_r, count_all_p, count_r

    def multi_each_target(self, target_list, bz_intent_list, re_intent_list):
        recall_list, precision_list, f1_list, pn_list, rn_list, tn_list = [], [], [], [], [], []
        for i in range(0, len(target_list)):
            print("------", target_list[i], "------")
            p, r, f1, pn, rn, tn = MultiClassByWord.class_target_for_ner(self, bz_intent_list, re_intent_list, target_list[i])
            print("人工标注数量为：", pn)
            print("接口预测数量为：", rn)
            print("结果一致数量为：", tn)
            print("准确率P为：", p)
            print("召回率R为：", r)
            print("F1为：", f1)
            recall_list.append(r)
            precision_list.append(p)
            f1_list.append(f1)
            pn_list.append(pn)
            rn_list.append(rn)
            tn_list.append(tn)
        return precision_list, recall_list, f1_list, pn_list, rn_list, tn_list

    def multi_ave_target(self, bz_intent_list, re_intent_list, point):
        print("------平均值(有效数据)------")
        p, r, f1, pn, rn, tn = MultiClassByWord.ave_target(self, bz_intent_list, re_intent_list, point)
        print("人工标注数量为：", pn)
        print("接口预测数量为：", rn)
        print("结果一致数量为：", tn)
        print("召回率R为：", r)
        print("准确率P为：", p)
        print("F1为：", f1)
        return p, r, f1, pn, rn, tn

#
# if __name__ == '__main__':
#     test_data = ChangeDataType.excel_to_dict(rootPath + "\\testresults\\resultfile\\" + "120_07_01-17_03_36gynaecology_intention_test_evn.xls",
#                                              sheet_name="统计结果")
#     target_list = CommonFunction().get_target("intent\\gynaecology\\线上target.txt")
#     bz_label = test_data.label.tolist()
#     re_label = test_data.re_intent.tolist()
#     # 返回每个target的准确率，召回率，F1
#     precision_list, recall_list, f1_list, pn_list, rn_list, tn_list = MultiClassByWord().multi_each_target(target_list,
#                                                                                                          bz_label,
#                                                                                                          re_label)
#
#     Binary.binary_plot_curve(bz_label,re_label)
