# -*- coding: UTF-8 -*-
'''
Created on 2020/2/27
@File  : common_function.py
@author: ZL
@Desc  :
'''
import csv
import zipfile
import os
import pandas
import re
import time
import xlwt
import codecs
from tqdm import tqdm
from algorithm.algorithm_func import MultiClassByWord

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class CommonFunction:

    @staticmethod
    def get_url(port, path):
        """
        通过port 和path确定接口url
        :param port: 端口号
        :param path: 接口路径
        :return url: 接口请求地址
        """
        url = "http://192.168.1.74:8999" + port + path
        return url

    @staticmethod
    def get_re_score(num, mid):
        """
        输入一个二分类接口的score值，mid为相似值界限：即大于这个相似值就视为相似，最后赋值score为1，若不相似则赋值为0
        :param num: 接口返回的num值
        :param mid：定义的相似值界限：大于这个界限即为相似，小于则不相似
        :return re_score：返回一个证
        """
        if float(num) <= float(mid):
            re_score = 0
        else:
            re_score = 1
        return re_score

    @staticmethod
    def get_sys_similary_tf(bz_value, re_value):
        """
        输入一个二分类接口的score值，mid为相似值界限：即大于这个相似值就视为相似，最后赋值score为1，若不相似则赋值为0
        :param num: 接口返回的num值
        :param mid：定义的相似值界限：大于这个界限即为相似，小于则不相似
        :return re_score：返回一个证
        """
        if bz_value == re_value:
            re_score = 1
        else:
            re_score = 0
        return re_score

    @staticmethod
    def get_tf(str1, str2):
        """
        判断两个值是否匹配，相等，并输出TRUE，FALSE值
        :param str1: 第一个判断值
        :param str2：第二个判断值
        :return tf：返回是否匹配：TRUE或FALSE
        """
        if str1 == str2:
            tf = "TRUE"
        else:
            tf = "FALSE"
        return tf

    def get_mult_tf(self, bz_list, re_list):
        """
        判断妇科多意图中意图标签是否匹配，相等，并输出TRUE，FALSE值
        :param str1: 第一个意图对（一个或多个标签）
        :param str2：第二个意图对（一个或多个标签）
        :return tf：返回是否匹配：TRUE或FALSE（根据标注验收规范）
        """
        tf = "FALSE"
        if len(bz_list) == 1:
            if len(re_list) == 1:
                if bz_list == re_list:
                    tf = "TRUE"
                else:
                    tf = "FALSE"
            elif len(re_list) == 2:
                for re_value in re_list:
                    if re_value in bz_list:
                        tf = "TRUE"
            else:
                tf = "FALSE"
        elif len(bz_list) == 2:
            if len(re_list) <= 2:
                for re_value in re_list:
                    if re_value in bz_list:
                        tf = "TRUE"
            elif len(re_list) == 3:
                n = 0
                for re_value in re_list:
                    if re_value in bz_list:
                        n = n + 1
                        if n >= 2:
                            tf = "TRUE"
            else:
                tf = "FALSE"
        elif len(bz_list) == 3:
            if len(re_list) == 1:
                tf = "FALSE"
            elif len(re_list) in range(2, 4):
                n = 0
                for re_value in re_list:
                    if re_value in bz_list:
                        n = n + 1
                        if n >= 2:
                            tf = "TRUE"
        else:
            tf = "FALSE"
        return tf

    @staticmethod
    def get_collection_1(data, tf_list):
        """
        拼接data值，控制台打
        :return data：data拼接更多的指标值对（是否一致，总数，一致数，不一直数，一致率，不一致率等）印算法相关的测试结果
        :param data: 在运行接口处已创建的list-data，里面通常包含多个参数对（例如：人工预测值，接口输出值）
        :param tf_list：传入tf_list;是否匹配对，由所有的测试集所运行处的结果，并再控制台输出
        """
        data["是否一致"] = tf_list
        data["总数"] = len(tf_list)
        data["一致数"] = tf_list.count("TRUE")
        data["不一致数"] = tf_list.count("FALSE")
        data["一致率"] = "{:.2f}%".format(tf_list.count("TRUE") / len(tf_list) * 100)
        data["不一致率"] = "{:.2f}%".format(tf_list.count("FALSE") / len(tf_list) * 100)
        print("总数：", len(tf_list), "，一致数：", tf_list.count("TRUE"), "，不一致数：", tf_list.count("FALSE"), "，一致率：",
              "{:.2f}%".format(tf_list.count("TRUE") / len(tf_list) * 100), "，不一致率：",
              "{:.2f}%".format(tf_list.count("FALSE") / len(tf_list) * 100))
        return data, len(tf_list), "{:.2f}%".format(tf_list.count("TRUE") / len(tf_list) * 100)

    def get_collection_2(self, target_file, bz_intent_list, re_intent_list, final_result):
        """
        通过获取target列表，以及人工及接口返回值，来计算每个target及平均的准确率，召回率，F1
        :param target_file: 储存target的文件
        :param data_file: 储存接口结果数据的文件
        """
        # 获取target列表
        target_list = CommonFunction.get_target(self, target_file)
        # 返回每个target的准确率，召回率，F1
        precision_list, recall_list, f1_list, pn_list, rn_list, tn_list = MultiClassByWord.multi_each_target(self,
                                                                                                             target_list,
                                                                                                             bz_intent_list,
                                                                                                             re_intent_list)
        # 返回平均的准确率，召回率，F1等值
        # target_list.append("平均值（不含无）")
        # p, r, f1, pn, rn, tn = MultiClassByWord.multi_ave_target(self, bz_intent_list, re_intent_list, "无")
        # precision_list.append(p)
        # recall_list.append(r)
        # f1_list.append(f1)
        # pn_list.append(pn)
        # rn_list.append(rn)
        # tn_list.append(tn)
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        workbook = xlwt.Workbook()
        sheet1 = workbook.add_sheet('统计结果', cell_overwrite_ok=True)
        sheet1.write(0, 0, "Target")
        sheet1.write(0, 1, "人工标注数量")
        sheet1.write(0, 2, "接口结果数量")
        sheet1.write(0, 3, "一致数量")
        sheet1.write(0, 4, "准确率")
        sheet1.write(0, 5, "召回率")
        sheet1.write(0, 6, "F1值")
        for i in range(0, len(target_list)):
            print(target_list[i], pn_list[i], rn_list[i], tn_list[i], precision_list[i], recall_list[i], f1_list[i])
            sheet1.write(i + 1, 0, target_list[i])
            sheet1.write(i + 1, 1, pn_list[i])
            sheet1.write(i + 1, 2, rn_list[i])
            sheet1.write(i + 1, 3, tn_list[i])
            sheet1.write(i + 1, 4, precision_list[i])
            sheet1.write(i + 1, 5, recall_list[i])
            sheet1.write(i + 1, 6, f1_list[i])
        workbook.save(rootPath + '\\testresults\\resultfile\\' + now + final_result)

    @staticmethod
    def zip_file(dir_path, zip_path):
        """
        将测试结果添加成压缩包
        :param dir_path: 生成测试结果数据的文件夹路径
        :param zip_path：生成压缩包的文件夹路径
        """
        resultzip = zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED)
        for root, dirnames, filenames in os.walk(dir_path):
            # 去掉根路径，只对目标文件夹下的文件及文件夹进行压缩
            file_path = root.replace(dir_path, '')
            # 循环出一个个文件名
            for filename in filenames:
                resultzip.write(os.path.join(root, filename), os.path.join(file_path, filename))
        resultzip.close()

    @staticmethod
    def get_ner_sentence(test_data_file):
        sentence_value, bio, bios_list, sentence_list = [], [], []
        test_data = codecs.open(test_data_file,
                                encoding="utf-8")
        for line in tqdm(test_data.readlines()):
            if len(line.strip()) == 0:
                sentence_list.append(sentence_value)
                bios_list.extend(bio)
                bio = []
                sentence_value = []
            else:
                line = line.strip()
                sentence_value.append(line.split("\t\t")[0])
                bio.append(line.split("\t\t")[1])
        return sentence_list, bios_list

    @staticmethod
    def change_space_to_comma(test_data_file):
        """
        将文件中的space空格转换为,（此方法为转化妇科ner的原始文件txt，源文件中含有空格）
        :param test_data_file: 需要修改的文件
        :return test_data_file：返回文件
        """
        # 清空文件内容（仅当以 "r+"   "rb+"    "w"   "wb" "wb+"等以可写模式打开的文件才可以执行该功能）
        f1 = open((rootPath + "\\testdata\\apidata\\" + test_data_file), 'r+', encoding='UTF-8',
                  errors='ignore')
        infos = f1.read()
        line_new = re.sub('	', ',', infos)  # 替换功能
        f1.seek(0)  # 清空文件
        f1.truncate()
        f1.write(line_new)  # 重写
        f1.close()

    @staticmethod
    def get_txt_to_csv(test_data_file, result_data_file):
        """
        将txt文件转换为csv，（此方法是为了处理妇科ner，源文件为含有空格的txt文件，转换space到,后，将txt转换为csv
        :param test_data_file: 需要转换文件格式的txt文件
        :param result_data_file: 转换后的csv文件
        """
        CommonFunction.change_space_to_comma(test_data_file)
        # 创建或打开csv文件，以写方式
        with open((rootPath + "\\testdata\\apidata\\" + result_data_file), 'w+', encoding='UTF-8',
                  newline='') as csvfile:
            spamwriter = csv.writer(csvfile, dialect='excel')
            # 打开txt文件，以读方式
            with open((rootPath + "\\testdata\\apidata\\" + test_data_file), 'r', encoding='UTF-8',
                      errors='ignore') as filein:
                spamwriter.writerow("--")
                for line in filein:
                    if "," in line:
                        if ",," in line:
                            line_list = line.strip('\n').split(',,')
                            if line_list[0] == "":
                                line_list[0] = "，"
                        else:
                            line_list = line.strip('\n').split(',')
                        spamwriter.writerow(line_list)
                    else:
                        spamwriter.writerow("--")
                spamwriter.writerow("--")

    @staticmethod
    def get_ner_to_words(file):
        """
        将csv中的-,-标签内的源文件word转换为句子
        :param file: 需要取句子的文件
        :return re_word_list：所有的单词list
        :return words_list:所有的句子list
        :return bios_list:所有的biolist
        """
        test_data = pandas.read_csv(rootPath + "\\testdata\\apidata\\" + file, encoding="utf-8")
        bio_list = []
        re_word_list = []
        word_list = []
        words_list = []
        words_l = []
        bios_list, words_bio_list = [], []
        for idx, temp in test_data.iterrows():
            # 判断只要不是-,-标签
            if temp[1] != "-":
                # 取每行的word
                word = temp[0]
                # 取每行的exp_bio(预期bio)
                exp_bio = temp[1]
                # re_word_list拼接所有的word
                re_word_list.append(word)
                # word_list拼接所有的word
                word_list.append(word)
                # 转换为str
                words = "".join(word_list)
                # bio_list拼接所有的exp_bio
                bio_list.append(exp_bio)
                # words_l拼接所有的words
                words_l.append(words)
            # 碰到标签后，即一个句子完成，重置words_l,word_list,bio_list
            else:
                # 拼接一个句子-words_l
                words_list.append(words_l[len(words_l) - 1])
                words_bio_list.append(words_l[len(words_l) - 1])
                for i in range(0, len(bio_list)):
                    # 拼接一个句子的bio_list
                    bios_list.append(bio_list[i])
                # 重置words_l,word_list,bio_list
                words_l = []
                word_list = []
                bio_list = []
        return re_word_list, words_list, bios_list

    def get_target(self, file):
        """
        获取target
        :param file: 储存target的文件
        :return target_list:返回所有的target列表
        """
        target_list = []
        # 打开target文件
        file = open(rootPath + "\\testdata\\apidata\\" + file, encoding="UTF-8")
        # 循环读每行，取值，拼接
        for line in file.readlines():
            target_list.append(line.strip())
        return target_list


if __name__ == '__main__':
    # test_data = ChangeDataType.excel_to_dict(rootPath + "\\testresults\\resultfile\\" + "120_07_01-17_03_36gynaecology_intention_test_evn.xls",
    #                                          sheet_name="统计结果")
    # target_list = CommonFunction().get_target("intent\\gynaecology\\线上target.txt")
    # bz_label = test_data.label.tolist()
    # re_label = test_data.re_intent.tolist()
    # # 返回每个target的准确率，召回率，F1
    # precision_list, recall_list, f1_list, pn_list, rn_list, tn_list = MultiClassByWord().multi_each_target(target_list,
    #                                                                                                      bz_label,
    #                                                                                                      re_label)
    CommonFunction().get_txt_to_csv("ner\\gynaecology\\" + "test_gynaecology.txt",
                                    "ner\\gynaecology\\" + "test_gynaecology.csv")
