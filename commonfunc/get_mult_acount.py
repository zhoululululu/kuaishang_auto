# -*- coding: UTF-8 -*-
'''
Created on 2020/5/26
@File  : get_mult_acount.py
@author: ZL
@Desc  :
'''
import xlwt
from commonfunc.common_function import CommonFunction
from algorithm.algorithm_func import MultiClassByWord
import os
from commonfunc.change_data_type import ChangeDataType

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetMultCount:
    """
    创建9个case函数，后续使用数组调用方法
    标注验收规范：
    1	1个标签	1个标签	 标签一致      	合格
    2	1个标签	2个标签	其中1个标签一致	合格
    3	1个标签	3个标签	            	不合格
    4	2个标签	1个标签	其中1个标签一致	合格
    5	2个标签	2个标签	其中1个标签一致	合格
    6	2个标签	3个标签	其中2个标签一致	合格
    7	3个标签	1个标签	                不合格
    8	3个标签	2个标签	其中2个标签一致	合格
    9	3个标签	3个标签	其中2个标签一致	合格
    """

    def __init__(self):
        """
        预先定义好case1-case9的数量为0
        """
        self.c1, self.c2, self.c3, self.c4, self.c5, self.tf = 0, 0, 0, 0, 0, "FALSE"
        self.c6, self.c7, self.c8, self.c9, self.c10, self.i, self.tf_list = 0, 0, 0, 0, 0, 0, []

    def case1(self, bz_list, re_list):
        # 长度均等于1，对即对，错即错
        self.c1 += 1
        if bz_list == re_list:
            self.tf = "TRUE"
        else:
            self.tf = "FALSE"
        return self.tf

    def case2(self, bz_list, re_list):
        # 返回意图标签长度为2，需要其中一个匹配，否则不匹配
        self.c2 += 1
        n = 0
        for re_value in re_list:
            if re_value in bz_list:
                n = n + 1
        if n >= 1:
            self.tf = "TRUE"
        else:
            self.tf = "FALSE"
        return self.tf

    def case3(self, bz_list, re_list):
        # 返回意图标签长度为3，即不匹配
        self.c3 += 1
        self.tf = "FALSE"
        return self.tf

    def case4(self, bz_list, re_list):
        # 标注意图标签长度为2，接口返回1个接口返回需要其中一个匹配，否则不匹配
        self.c4 += 1
        if re_list[0] in bz_list:
            self.tf = "TRUE"
        else:
            self.tf = "FALSE"
        return self.tf

    def case5(self, bz_list, re_list):
        # 标注与接口返回意图标签长度为2，需要其中一个匹配，否则不匹配
        self.c5 += 1
        n = 0
        for re_value in re_list:
            if re_value in bz_list:
                n += 1
        if n >= 1:
            self.tf = "TRUE"
        else:
            self.tf = "FALSE"
        return self.tf

    def case6(self, bz_list, re_list):
        # 标注意图标签长度为2，接口返回为3，需要其中两个匹配，否则不匹配
        self.c6 += 1
        n = 0
        for re_value in re_list:
            if re_value in bz_list:
                n = n + 1
        if n >= 2:
            self.tf = "TRUE"
        else:
            self.tf = "FALSE"
        return self.tf

    def case7(self, bz_list, re_list):
        # 标注意图标签长度为3，接口返回为1，即不匹配
        self.c7 += 1
        self.tf = "FALSE"
        return self.tf

    def case8(self, bz_list, re_list):
        # 标注意图标签长度为3，接口返回为2，需要其中两个匹配，否则不匹配
        self.c8 += 1
        n = 0
        for re_value in re_list:
            if re_value in bz_list:
                n += 1
        if n >= 2:
            self.tf = "TRUE"
        else:
            self.tf = "FALSE"
        return self.tf

    def case9(self, bz_list, re_list):
        # 标注意图标签长度为3，接口返回为3，需要其中两个匹配，否则不匹配
        self.c9 += 1
        n = 0
        for re_value in re_list:
            if re_value in bz_list:
                n += 1
        if n >= 2:
            self.tf = "TRUE"
        else:
            self.tf = "FALSE"
        return self.tf

    def case10(self):
        # 其他情况：标注或接口返回意图标签大于3，小于1，默认不匹配
        self.tf = "FALSE"
        self.c10 += 1
        return self.tf

    def get_mult_tf_and_count(self, all_bz_list, all_re_list):
        """
        判断妇科多意图中意图标签是否匹配，相等，并输出TRUE，FALSE值,以及9种情况下的每种情况数量值
        :param str1: 第一个意图对（一个或多个标签）
        :param str2：第二个意图对（一个或多个标签）
        :return tf_list,c1, c2, c3, c4, c5, c6, c7, c8, c9：返回是否匹配：TRUE或FALSE（根据标注验收规范），
                                                        以及9种情况下的每种情况数量值
        """
        # 遍历all_bz_list的所有的列表值（由于两个列表的长度一致，只需判断一个即可）
        print(all_bz_list, all_re_list)
        while self.i < len(all_bz_list):
            bz_list = all_bz_list[self.i]  # 当前标注的意图列表
            re_list = all_re_list[self.i]  # 当前接口的意图列表
            # def_list :根据标注标签与接口返回标签的长度，进入不同的case函数（共9个case）
            # 进入后每个case会对该case进行一个计数递增操作，并返回是否匹配值
            def_list = {
                (1, 1): GetMultCount.case1,
                (1, 2): GetMultCount.case2,
                (1, 3): GetMultCount.case3,
                (2, 1): GetMultCount.case4,
                (2, 2): GetMultCount.case5,
                (2, 3): GetMultCount.case6,
                (3, 1): GetMultCount.case7,
                (3, 2): GetMultCount.case8,
                (3, 3): GetMultCount.case9
            }
            try:
                # 进行一个数组的key值匹配后，运行函数，传参数值
                if (len(bz_list), len(re_list)) in def_list.keys():
                    tf = def_list[(len(bz_list), len(re_list))](self, bz_list, re_list)
                else:  # key值（即标注意图与接口返回意图长度）不匹配时，默认不匹配
                    tf = GetMultCount.case10(self)
                self.tf_list.append(tf)
            except Exception as e:
                print(e)
            self.i = self.i + 1
        print(self.tf_list, self.c1, self.c2, self.c3, self.c4, self.c5, self.c6, self.c7, self.c8, self.c9, self.c10)
        return self.tf_list

    @staticmethod
    def get_re_label(label_value_list, score_value_list, threshold_value):
        re_list = []
        for i in range(0, len(score_value_list)):
            re_score = CommonFunction.get_re_score(score_value_list[i], threshold_value)
            if re_score == 1:
                re_list.append(label_value_list[i])
        return re_list

    def output_threshold(self, bz_list, score_list, target_file):
        all_re_list, i, j = [], 0.01, 0
        target_list = CommonFunction.get_target(self, target_file)
        for point in target_list:
            n = 0
            workbook = xlwt.Workbook()
            sheet1 = workbook.add_sheet(point + "_多意图超参数统计结果", cell_overwrite_ok=True)
            sheet1.write(0, 0, "阈值")
            sheet1.write(0, 1, "准确率P")
            sheet1.write(0, 2, "召回率R")
            sheet1.write(0, 3, "F1值")
            while i <= 0.99:
                n = n + 1
                while j < len(score_list):
                    all_re_list.append(GetMultCount.get_re_label(target_list, score_list[j][0], i))
                    j += 1
                p, r, f1, pn, rn, tn = MultiClassByWord.mult_class_target(self, bz_list, all_re_list, point)
                sheet1.write(n, 0, i)
                sheet1.write(n, 1, p)
                sheet1.write(n, 2, r)
                sheet1.write(n, 3, f1)
                i += 0.01
                j = 0
                all_re_list = []
            i = 0
            workbook.save(rootPath + '\\testresults\\resultfile\\mult_intention\\' + point + "_多意图超参数统计结果.xls")

    def get_best_threshold(self, target_file):
        f1_list, p_list, r_list, alpha_list = [], [], [], []
        target_list = CommonFunction.get_target(self, target_file)
        n = 0
        workbook = xlwt.Workbook()
        sheet1 = workbook.add_sheet("多意图超参数最佳阈值prf统计结果", cell_overwrite_ok=True)
        sheet1.write(0, 0, "意图")
        sheet1.write(0, 1, "阈值")
        sheet1.write(0, 2, "准确率P")
        sheet1.write(0, 3, "召回率R")
        sheet1.write(0, 4, "F1值")
        for point in target_list:
            n += 1
            test_data = ChangeDataType.excel_to_dict(
                rootPath + '\\testresults\\resultfile\\mult_intention\\' + point + "_多意图超参数统计结果.xls",
                point + "_多意图超参数统计结果")
            for idx, temp in test_data.iterrows():
                alpha = temp["阈值"]
                p = temp["准确率P"]
                r = temp["召回率R"]
                f1 = temp["F1值"]
                alpha_list.append(alpha)
                f1_list.append(f1)
                p_list.append(p)
                r_list.append(r)
            print(p_list[f1_list.index(max(f1_list))],
                  r_list[f1_list.index(max(f1_list))], f1_list[f1_list.index(max(f1_list))])
            sheet1.write(n, 0, point)
            sheet1.write(n, 1, alpha_list[f1_list.index(max(f1_list))])
            sheet1.write(n, 2, p_list[f1_list.index(max(f1_list))])
            sheet1.write(n, 3, r_list[f1_list.index(max(f1_list))])
            sheet1.write(n, 4, f1_list[f1_list.index(max(f1_list))])
            f1_list, p_list, r_list = [], [], []
        workbook.save(rootPath + "\\testresults\\resultfile\\mult_intention\\多意图超参数最佳阈值prf统计结果.xls")

    def get_half_threshold(self, target_file):
        f1_list, p_list, r_list, alpha_list = [], [], [], []
        target_list = CommonFunction.get_target(self, target_file)
        n = 0
        workbook = xlwt.Workbook()
        sheet1 = workbook.add_sheet("多意图超参数最佳阈值prf统计结果", cell_overwrite_ok=True)
        sheet1.write(0, 0, "意图")
        sheet1.write(0, 1, "阈值")
        sheet1.write(0, 2, "准确率P")
        sheet1.write(0, 3, "召回率R")
        sheet1.write(0, 4, "F1值")
        for point in target_list:
            n += 1
            test_data = ChangeDataType.excel_to_dict(
                rootPath + '\\testresults\\resultfile\\mult_intention\\' + point + "_多意图超参数统计结果.xls",
                point + "_多意图超参数统计结果")
            for idx, temp in test_data.iterrows():
                alpha = temp["阈值"]
                p = temp["准确率P"]
                r = temp["召回率R"]
                f1 = temp["F1值"]
                alpha_list.append(alpha)
                f1_list.append(f1)
                p_list.append(p)
                r_list.append(r)
            print(p_list[49],
                  r_list[49], f1_list[50])
            sheet1.write(n, 0, point)
            sheet1.write(n, 1, alpha_list[49])
            sheet1.write(n, 2, p_list[49])
            sheet1.write(n, 3, r_list[49])
            sheet1.write(n, 4, f1_list[49])
            f1_list, p_list, r_list = [], [], []
        workbook.save(rootPath + '\\testresults\\resultfile\\' + "1多意图0.5阈值prf测试结果.xls")

    def get_re_threshold(self, bz_list, re_list, target_file):
        all_re_list, i, j = [], 0.01, 0
        target_list = CommonFunction.get_target(self, target_file)
        workbook = xlwt.Workbook()
        sheet1 = workbook.add_sheet("多意图prf统计结果", cell_overwrite_ok=True)
        sheet1.write(0, 0, "意图列表")
        sheet1.write(0, 1, "准确率P")
        sheet1.write(0, 2, "召回率R")
        sheet1.write(0, 3, "F1值")
        n = 0
        for point in target_list:
            n = n + 1
            p, r, f1, pn, rn, tn = MultiClassByWord.mult_class_target(self, bz_list, re_list, point)
            sheet1.write(n, 0, point)
            sheet1.write(n, 1, p)
            sheet1.write(n, 2, r)
            sheet1.write(n, 3, f1)
            j = 0
            all_re_list = []
        workbook.save(rootPath + '\\testresults\\resultfile\\' + "多意图prf测试结果（接口返回）.xls")
