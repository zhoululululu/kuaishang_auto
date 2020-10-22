# -*- coding: UTF-8 -*-
'''
Created on 2020/9/22 10:14
@File  : get_collection.py
@author: ZL
@Desc  :
'''
from commonfunc.change_data_type import ChangeDataType
import os
import pandas
from algorithm.algorithm_func import Binary

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetCollection:
    def __init__(self, file):
        self.test_data = ChangeDataType.file_to_dict(rootPath + "\\testdata\\knowledgegraph\\relationship\\" + file)
        # sheet_name="Sheet1")
        # self.true_relation = self.test_data.true_relation.tolist()
        # self.predict_relation = self.test_data.predict_relation.tolist()
        # self.probability = self.test_data.probability.tolist()
        # self.flag = self.test_data.FLAG.tolist()

    def get_collection_1(self):
        """
        总体准确率,覆盖率,含other（负例） 以及 不含other（负例）
        :return:总体准确率
        """
        print("-----整体准确率及覆盖率-----")
        # 含other准确率
        p1 = (self.flag.count(True) / len(self.flag))
        # 正例覆盖率
        t_coverage1 = ((len(self.true_relation) - self.true_relation.count("other")) / len(self.true_relation))

        # 不含other准确率
        for i in range(len(self.true_relation) - 1, -1, -1):
            if self.true_relation[i] == "other":
                self.true_relation.pop(i)
                self.flag.pop(i)
        p2 = (self.flag.count(True) / len(self.flag))
        # 正例覆盖率
        t_coverage2 = ((len(self.true_relation) - self.true_relation.count("other")) / len(self.true_relation))
        print('含other准确率: {:.2%}'.format(p1))
        print('含other正例覆盖率: : {:.2%}'.format(t_coverage1))
        print('含other准确率: {:.2%}'.format(p2))
        print('含other正例覆盖率: : {:.2%}'.format(t_coverage2))
        return p1, t_coverage1, p2, t_coverage2

    # model_1，区分other_1与其他
    def binary_model_1_false(self, bz_list, re_list):
        count_all_p = 0
        count_p = 0
        count_all_r = 0
        count_r = 0
        acc_num = 0
        mis_num, zero_num = 0, 0
        for i in range(0, len(bz_list)):
            if bz_list[i] == "other":
                count_all_r += 1
                # if bz_list[i] == re_list[i]:
                if re_list[i] == "other_1":
                    count_r += 1
            if re_list[i] == "other_1":
                count_all_p += 1
                if bz_list[i] == "other":
                    count_p += 1
            if (bz_list[i] == re_list[i] and re_list[i] != "other_1") or (
                    bz_list[i] == "other" and re_list[i] == "other_1"):
                acc_num += 1
            if bz_list[i] != "other":
                zero_num += 1
                if re_list[i] == "other_1":
                    mis_num += 1
        P = count_p / count_all_p
        R = count_r / count_all_r
        F1 = 2 * P * R / (P + R)
        mis_rate = mis_num / zero_num
        accuracy = acc_num / len(bz_list)
        return P, R, F1, accuracy, mis_rate

    # model_1，区分other_1与其他
    def binary_model_1_true(self, bz_list, re_list):
        count_all_p = 0
        count_p = 0
        count_all_r = 0
        count_r = 0
        acc_num = 0
        mis_num, zero_num = 0, 0
        for i in range(0, len(bz_list)):
            if bz_list[i] != "other":
                count_all_r += 1
                # if bz_list[i] == re_list[i]:
                if re_list[i] != "other_1":
                    count_r += 1
            if re_list[i] != "other_1":
                count_all_p += 1
                if bz_list[i] != "other":
                    count_p += 1
            if (bz_list[i] == re_list[i] and re_list[i] != "other_1") or (
                    bz_list[i] == "other" and re_list[i] == "other_1"):
                acc_num += 1
            if bz_list[i] == "other":
                zero_num += 1
                if re_list[i] != "other_1":
                    mis_num += 1
        P = count_p / count_all_p
        R = count_r / count_all_r
        F1 = 2 * P * R / (P + R)
        mis_rate = mis_num / zero_num
        accuracy = acc_num / len(bz_list)
        return P, R, F1, accuracy, mis_rate

    # model_2，忽略other_1，均为other
    def binary_model_2_true(self, bz_list, re_list):
        count_all_p = 0
        count_p = 0
        count_all_r = 0
        count_r = 0
        acc_num = 0
        mis_num, zero_num = 0, 0
        for i in range(0, len(bz_list)):
            if bz_list[i] != "other":
                count_all_r += 1
                if bz_list[i] == re_list[i]:
                    count_r += 1
            if re_list[i] != "other":
                count_all_p += 1
                if bz_list[i] == re_list[i]:
                    count_p += 1
            if bz_list[i] == re_list[i]:
                acc_num += 1
            if bz_list[i] == "other":
                zero_num += 1
                if re_list[i] != "other":
                    mis_num += 1
        P = count_p / count_all_p
        R = count_r / count_all_r
        F1 = 2 * P * R / (P + R)
        mis_rate = mis_num / zero_num
        accuracy = acc_num / len(bz_list)
        return P, R, F1, accuracy, mis_rate

    def get_accuracy_and_coverage(self, threshold, model, tf):
        """
        在设定的阈值范围内的结果的准确率和覆盖率
        :param threshold:设定的阈值
        :return:
        """
        with_other_flag_list, without_other_flag_list, in_threshold_api_relation = [], [], []
        api_relation = self.test_data.api_relation.tolist()
        expect_relation = self.test_data.expect_relation.tolist()
        api_threshold = self.test_data.api_threshold.tolist()
        tf_list = self.test_data.tf_list.tolist()
        for i in range(len(api_threshold)):
            if float(api_threshold[i]) >= threshold:
                with_other_flag_list.append(tf_list[i])
                in_threshold_api_relation.append(api_relation[i])

        # 总体的准确率
        all_precision = tf_list.count(True) / len(tf_list)
        if model == 1 and tf == True:
            # 模型1（正例）二分类的准确率
            P, R, F1, accuracy, mis_rate = GetCollection.binary_model_1_true(self, expect_relation, api_relation)
            print("模型1（正例）：P, R, F1, accuracy，(负例的)误判率分别为：", P, R, F1, accuracy, mis_rate)
        if model == 1 and tf == False:
            # 模型1（负例）二分类的准确率
            P, R, F1, accuracy, mis_rate = GetCollection.binary_model_1_false(self, expect_relation, api_relation)
            print("模型1（负例）：P, R, F1, accuracy，(正例的)误判率分别为：", P, R, F1, accuracy, mis_rate)
            # 模型1+2（正例）二分类的准确率
        if model == 2 and tf == True:
            P, R, F1, accuracy, mis_rate = GetCollection.binary_model_2_true(self, expect_relation, api_relation)
            print("模型1+2（正例）：P, R, F1, accuracy，(负例的)误判率分别为：", P, R, F1, accuracy, mis_rate)

        # 含other准确率
        with_other_precision = with_other_flag_list.count(True) / len(with_other_flag_list)

        # 正例覆盖率-1（正例/筛选出来的正负例）
        with_other_t_coverage_1 = ((len(in_threshold_api_relation) - in_threshold_api_relation.count("other")) / len(
            expect_relation))

        # 总体覆盖率（筛选后的所有值/总数）
        with_other_t_coverage_2 = len(in_threshold_api_relation) / len(expect_relation)

        # 总体正例覆盖率
        with_other_t_coverage_3 = (len(expect_relation) - expect_relation.count("other")) / len(expect_relation)
        print("总体正例覆盖率", with_other_t_coverage_3)

        in_threshold_without_other_api_relation = []

        for i in range(len(in_threshold_api_relation) - 1, -1, -1):
            if in_threshold_api_relation[i] not in ["other", "other_1"]:
                in_threshold_without_other_api_relation.append(in_threshold_api_relation[i])
                without_other_flag_list.append(with_other_flag_list[i])
        print(in_threshold_without_other_api_relation)
        # 正例（不含other）准确率
        without_other_precision = without_other_flag_list.count(True) / len(without_other_flag_list)
        print("总体准确率", all_precision)
        print("阈值为{}：含other准确率".format(threshold), with_other_precision)
        print("阈值为{}：正例覆盖率-1（正例/筛选出来的正负例）".format(threshold), with_other_t_coverage_1)
        print("阈值为{}：正例覆盖率-2（正例/预期所有的正例）".format(threshold), with_other_t_coverage_2)
        print("阈值为{}：不含other准确率".format(threshold), without_other_precision)

        # not_sure_flag, not_sure_precision_list, not_sure_precision, not_sure_flag = [], [], [], []
        # not_sure_threshold = 0
        # while not_sure_threshold < 0.99:
        #     not_sure_threshold += 0.01
        #     for j in range(len(api_threshold)):
        #         if float(api_threshold[j]) >= not_sure_threshold:
        #             not_sure_flag.append(tf_list[j])
        #             not_sure_precision = not_sure_flag.count(True) / len(not_sure_flag)
        #             not_sure_precision_list.append({not_sure_threshold: not_sure_precision})
        #     print({not_sure_threshold: not_sure_precision})
        # print(not_sure_precision_list)
        return with_other_precision, with_other_t_coverage_1, with_other_t_coverage_2, without_other_precision

    def get_not_sure_threshold_precision(self):
        with_other_precision_list, coverage_1_list, coverage_2_list, without_other_precision_list, threshold_list = [], [], [], [], []
        threshold = 0
        while threshold < 0.99:
            threshold += 0.01
            with_other_precision, with_other_t_coverage_1, with_other_t_coverage_2, without_other_precision = \
                GetCollection.get_accuracy_and_coverage(self, threshold, 2, True)
            with_other_precision_list.append(with_other_precision)
            coverage_1_list.append(with_other_t_coverage_1)
            coverage_2_list.append(with_other_t_coverage_2)
            without_other_precision_list.append(without_other_precision)
            threshold_list.append('{:.2f}'.format(threshold))

        result_data = pandas.DataFrame(
            {"阈值": threshold_list,
             "总体覆盖率（筛选后的所有值/总数）": coverage_2_list,
             "总体准确率（包含正负例）": with_other_precision_list,
             "正例覆盖率（正例/筛选出来的正负例）": coverage_1_list,
             "正例准确率": without_other_precision_list})
        result_data.to_csv(
            rootPath + "\\testdata\\knowledgegraph\\relationship\\" + "result_with_not_sure_threshold_new.csv")

    def get_collection_2(self):
        """
        准确率在95%以上的阈值，覆盖率统计
        :param file:
        :return:
        """
        print("-----准确率在95%以上的阈值，覆盖率统计-----")
        new_flag, new_predict = [], []
        i = 0
        p_list = []
        while i < 0.99:
            i += 0.01
            for j in range(len(self.flag)):
                new_flag.append(GetCollection.get_tf(self.probability[j], i))
                if GetCollection.get_tf(self.probability[j], i) == True:
                    new_predict.append(self.flag[j])
            p1 = (new_predict.count(True) / new_flag.count(True))
            p_list.append({i: p1})
            new_predict = []
            new_flag = []
            # 正例覆盖率
            # t_coverage1 = ((len(self.true_relation) - self.true_relation.count("other")) / len(self.true_relation))
        if float(p1) >= 0.95:
            print(i)
            print('含other准确率: {:.2%}'.format(p1))
            # print('含other正例覆盖率: {:.2%}'.format(t_coverage1))
            # print('不含other准确率: {:.2%}'.format(p2))
            # print('不含other正例覆盖率: : {:.2%}'.format(t_coverage2))
            # return p1, t_coverage1, p2, t_coverage2
        print(p_list)

    @staticmethod
    def get_collection_3(file):
        """
        准确率在90-95%之间的阈值，覆盖率统计
        :param file:
        :return:
        """
        test_data = ChangeDataType.file_to_dict(rootPath + "\\testdata\\knowledgegraph\\relationship\\" + file,
                                                sheet_name="Sheet1")
        true_relation = test_data.true_relation.tolist()
        predict_relation = test_data.predict_relation.tolist()
        probability = test_data.probability.tolist()
        flag = test_data.FLAG.tolist()
        print(true_relation)

    def get_tf(num1, target_num):
        if num1 >= target_num:
            return True
        else:
            return False

    def get_relation_prf_ignore_other_1(self):
        """
        计算api接口返回的relation的prf值,忽略other_1
        :return:
        """
        # 先完成过滤other_1
        api_relation = self.test_data.api_relation.tolist()
        expect_relation = self.test_data.expect_relation.tolist()
        for i in range(len(api_relation) - 1, -1, -1):
            if api_relation[i] == "other_1":
                api_relation.pop(i)
        expect_relation_list = list(set(expect_relation))
        # relation_list = list(set(api_relation))
        label_list = list(set(['可能病因', '需要用到的仪器', 'other', '需做的检查', '关联的病毒', '关联的症状', '关联的部位', '可用的手术方式', '可用的其他治疗方式']))
        # print(relation_list)
        print(expect_relation_list)
        print(label_list)

    def get_reload_result_with_tf(self):
        """
        修改结果文件，将True or False写进结果，方便后期统计
        :return: 无
        """
        tf_list = []
        api_relation = self.test_data.api_relation.tolist()
        expect_relation = self.test_data.expect_relation.tolist()
        entity_list = self.test_data.entity_list.tolist()
        api_threshold = self.test_data.api_threshold.tolist()
        dialog_id = self.test_data.final_dialog_id.tolist()
        for i in range(len(api_relation)):
            if api_relation[i] == "other_1" and expect_relation[i] == "other":
                tf_list.append("True")
            elif api_relation[i] != "other_1" and api_relation[i] == expect_relation[i]:
                tf_list.append("True")
            else:
                tf_list.append("False")
        result_data = pandas.DataFrame(
            {"dialog_id": dialog_id, "entity_list": entity_list, "expect_relation": expect_relation,
             "api_relation": api_relation, "api_threshold": api_threshold, "tf_list": tf_list, })
        result_data.to_csv(rootPath + "\\testdata\\knowledgegraph\\relationship\\" + "more_result_with_tf_model_1.csv")

    def get_compare_two_response(self, file1, file2):
        test1 = ChangeDataType.file_to_dict(rootPath + "\\testdata\\knowledgegraph\\relationship\\" + file1)
        test2 = ChangeDataType.file_to_dict(rootPath + "\\testdata\\knowledgegraph\\relationship\\" + file2)

        dialog_relaition_1 = test1.r_list.tolist()
        dialog_1 = test1.d_list.tolist()
        result_1 = []
        dialog_relaition_2 = test2.api_relation.tolist()
        dialog_2 = test2.final_dialog_id.tolist()
        result_2 = []
        for i in range(len(dialog_1)):
            if dialog_1[i] == 1860:
                result_1.append(dialog_relaition_1[i])

        for j in range(len(dialog_2)):
            if dialog_2[j] == 1860:
                result_2.append(dialog_relaition_2[j])

        print(result_1)
        print(result_2)

    def get_compare_two_expect(self, file1, file2):
        test1 = ChangeDataType.file_to_dict(rootPath + "\\testdata\\knowledgegraph\\relationship\\" + file1)
        test2 = ChangeDataType.file_to_dict(rootPath + "\\testdata\\knowledgegraph\\relationship\\" + file2)

        dialog_relaition_1 = []
        dialog_1 = test1.dialog_id.tolist()
        entity_value_relationship = test1.entity_value_relationship.tolist()
        for i in entity_value_relationship:
            if "无需标注" not in i:
                dialog_relaition_1.append(i.split("#")[1])
            else:
                dialog_relaition_1.append([])

        # print(len(dialog_relaition_1), len(dialog_1))

        result_1, result_2 = [], []
        dialog_relation_2 = test2.expect_relation.tolist()
        dialog_2 = test2.final_dialog_id.tolist()

        for i in range(len(dialog_1)):
            if dialog_1[i] == 1860:
                result_1.append(dialog_relaition_1[i])

        for j in range(len(dialog_2)):
            if dialog_2[j] == 1860:
                result_2.append(dialog_relation_2[j])

        # print(len(result_1))
        # print(len(result_2) - result_2.count("other"))


if __name__ == '__main__':
    # GetCollection("weights_new_model4_21test_zl.xls").get_collection_1()
    # GetCollection("weights_new_model4_21test_zl.xls").get_collection_2()
    GetCollection("more_result_with_tf_model_1.csv").get_accuracy_and_coverage(0.94, 1, True)
    # GetCollection("more_result_with_tf_without_other1.csv").get_not_sure_threshold_precision()
    # GetCollection("more_api_test_result.csv").get_reload_result_with_tf()
    # GetCollection("api_test_result.csv").get_compare_two_expect("result.csv",
    #                                                             "20_10_14-10_42_30final_result_1.csv")
    # GetCollection("more_result_with_tf_model_1.csv").get_relation_prf_ignore_other_1(0.94, 1, True)
