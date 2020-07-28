# -*- coding: UTF-8 -*-
'''
Created on 2020/5/13
@File  : get_requests.py
@author: ZL
@Desc  :
'''
from commonfunc.common_function import CommonFunction
from commonfunc.change_data_type import ChangeDataType
import os
import requests
import time
from algorithm.algorithm_func import MultiClassByWord
import xlwt
from tqdm import tqdm
import csv
from algorithm.algorithm_func import Binary

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetRequests:

    @staticmethod
    def get_params(api_name, data):
        """
        获取接口的请求参数
        :param api_name: 请求接口属于哪个类型
        :param data: 读取的testdata值，拼接params值
        """
        # 线上意图
        if api_name == "pro_intent":
            params = {
                "utterance": data[0],
                "multi_intent_mode": data[1],
                "enterprise": data[2]
            }
        # 测试环境意图
        if api_name == "test_intent":
            params = {
                "sentence": data
            }

        # 皮肤科意图
        if api_name == "a_intent":
            params = {
                "utterance": data
            }
        # 项目
        elif api_name == "item":
            params = {
                "sentence": data
            }
        # 实体
        elif api_name == "ner":
            params = {
                "utterance": data[0],
                "model_name": data[1]
            }
        # 句子相似度
        elif api_name == "qa_similary":
            params = {
                "str1": data[0],
                "str2": data[1],
                "model": data[2]
            }
        # 症状相似度
        elif api_name == "symptom_similary":
            params = {
                "symptom1": data[0],
                "symptom2": data[1]
            }
        # 其他
        else:
            pass
        return params

    @staticmethod
    def get_response(api_name, result):

        """
        获取接口的返回结果所需要的值，例如意图识别的意图值，项目识别的项目值
        :param api_name: 请求接口属于哪个类型
        :param data: 接口返回的result
        """
        # 意图
        if api_name == "pro_intent":
            result = result["data"]["intent"]

        # 意图
        if api_name == "test_intent":
            #result = result["data"]["intention"]
            result = result["label"]

        # 意图
        if api_name == "a_intent":
            # result = result["data"]["intent"]
            result = result["data"]["intent"]

        # 项目
        elif api_name == "item":
            result = result["data"]["item"]
        # 实体
        elif api_name == "ner":
            result = result["data"]["bio"]
        # 句子相似度
        elif api_name == "qa_similary":
            result = result["data"]["score"]
            # result = result["sim_score"]
        # 症状相似度
        elif api_name == "symptom_similary":
            result = result["data"]["score"]
        else:
            pass
        return result

    def get_request(self, api_url, method, api_category, target_file, test_data_file, testdata_param, assert_param,
                    result_file, target_result_file):
        """
        通过抽取测试集的数据，调用请求api接口，得出的测试结果，在调用函数获取二分类或，每个target的准确率，召回率，F1
        :param target_file: 储存target的文件
        :param data_file: 储存接口结果数据的文件
        """
        # 获取测试集的data
        # case1: 如果是ner的话特殊处理，需要提取字集，句子集，以及bio集
        # case2：其他的接口正常读取testdata的所有值后续处理
        # 定义人工标注，接口返回，是否一致列表
        re_list, exp_list, tf_list, mul_params, word_list = [], [], [], [], []
        if api_category == "ner":
            word_list, words_list, exp_list = CommonFunction.get_ner_to_words(test_data_file)
            f = open(rootPath + "\\testresults\\resultfile\\" + result_file, 'w+', encoding='utf-8',
                     newline="")
            csv_writer = csv.writer(f)
            # 输入csv文件四个列的title
            csv_writer.writerow(["word", "exp_bio", "re_bio", "tf"])
            n = -1  # 计数n，用于遍历word_list及bios_list对应的值
            circle_data = words_list
            for temp in tqdm(circle_data):  # 循环读取参数，并传入参数值
                # 获取params参数
                mul_params.append(temp)
                mul_params.append(testdata_param[1])  # 不存在data中的话，直接赋值参数值
                params = GetRequests.get_params(api_category, mul_params)  # 调用函数拼接参数对
                mul_params.clear()  # 清空params
                try:
                    # 发送请求
                    r = requests.request(method=method, url=api_url,
                                         params=params,
                                         timeout=500)
                    result = r.json()
                    response = GetRequests.get_response(api_category, result)  # 获取返回结果中所需要的对比值
                    for i in range(0, len(response)):
                        n = n + 1
                        # 调用函数，查看人工bio与接口返回bio是否一致
                        tf = CommonFunction.get_tf(exp_list[n], response[i])
                        # csv循环填入字，人工bio值，接口返回bio值，以及tf值
                        csv_writer.writerow([word_list[n], exp_list[n], response[i], tf])
                        re_list.append(response[i])
                        tf_list.append(tf)
                except Exception as e:
                    print("bad request")
        else:
            test_data = ChangeDataType.csv_to_dict(rootPath + "\\testdata\\apidata\\" + test_data_file)
            circle_data = test_data.iterrows()
            for idx, temp in tqdm(circle_data):  # 循环读取参数，并传入参数值
                # 获取params参数
                # 针对接口需要两个及以上参数
                if len(testdata_param) > 1:
                    for i in range(0, len(testdata_param)):
                        # 先判断参数值是否在testdata list中存在（因为相似度或者意图等接口会有科室参数，但是测试数据中无科室信息）
                        if str(testdata_param[i]) in temp:
                            mul_params.append(temp[testdata_param[i]])  # 存在的话储存该参数对应的值
                        else:
                            mul_params.append(testdata_param[i])  # 不存在data中的话，直接赋值参数值
                    params = GetRequests.get_params(api_category, mul_params)  # 调用函数拼接参数对
                    mul_params.clear()  # 清空params
                else:  # 其他识别的接口中只有一个参数，直接拼接
                    params = GetRequests.get_params(api_category, temp[testdata_param[0]])
                try:
                    # 发送请求
                    r = requests.request(method=method, url=api_url,
                                         params=params,
                                         timeout=500)
                    result = r.json()
                    response = GetRequests.get_response(api_category, result)  # 获取返回结果中所需要的对比值
                    # 对妇科多意图进行特定判断，处理
                    if "intent" in api_category and "gynaecology" in testdata_param:
                        if "、" in temp[assert_param]:
                            assert_param_list = temp[assert_param].split("、")  # 先对意图进行拆分，根据"、"进行拆分成列表（若只有一个则直接为本值）
                            # 对拆分后的意图及返回结果的意图也进行排序
                            assert_param_list.sort()
                            response.sort()
                            tf = CommonFunction.get_tf(assert_param_list, response)  # 判断排序后的意图是否完全一致，完全一致则匹配成功
                        else:
                            assert_param_list = temp[assert_param]
                            tf = CommonFunction.get_tf(assert_param_list, response)  # 判断是否一致，为后面输出做准备
                        exp_list.append(assert_param_list)  # 拼接已拆解并排序后的意图原始值
                        re_list.append(response)  # 拼接已排序后的结果意图返回值
                    else:
                        # 针对相似度进行一个相似匹配，0.5为匹配阈值，可根据需要修改
                        if "qa_similary" in api_category:
                            response = CommonFunction.get_re_score(response, 0.9)
                        if "symptom_similary" in api_category:
                            response = CommonFunction.get_sys_similary_tf(response, temp["标准症状"])
                        tf = CommonFunction.get_tf(temp[assert_param], response)  # 判断是否一致，为后面输出做准备
                        # 拼接三个列表值
                        exp_list.append(temp[assert_param])  # 拼接原始值
                        re_list.append(response)  # 拼接结果返回值
                    tf_list.append(tf)  # 拼接是否一致值

                # 如果请求失败，打印bad request
                except Exception as e:
                    print(e)

            test_data["response"] = re_list  # 在testdata中拼接接口返回值，方便后期输出excel对齐显示
            # 调用方法控制台打印输出相关信息（是否一致，总数，一致数，不一直数，一致率，不一致率等）
            test_data, total_num, accuracy = CommonFunction.get_collection_1(test_data,
                                                                             tf_list)
            now = time.strftime('%y_%m_%d-%H_%M_%S')
            test_data.to_excel(rootPath + '\\testresults\\resultfile\\' + now + result_file, index=False,
                               encoding="utf-8")  # 输出excel
        if "similary" in api_category:  # 相似度处理（二分类算法，直接调用输出显示prf值）
            Binary.binary_plot_curve(exp_list, re_list)
        else:  # 其他接口（多分类算法，通过调用调用输出显示每个target的prf值）
            file_name = GetRequests.get_target_result(self, target_file, exp_list, re_list, target_result_file,
                                                      total_num, accuracy)
            return file_name

    def get_target_result(self, target_file, bz_intent_list, re_intent_list, target_result_file, total_num, accuracy):
        """
        通过获取target列表，以及人工及接口返回的意图值，来计算每个target及平均的准确率，召回率，F1
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
        target_list.append("汇总")
        precision_list.append("用例数：" + str(total_num))
        recall_list.append("accuracy：" + str(accuracy))
        f1_list.append("")
        pn_list.append("")
        rn_list.append("")
        tn_list.append("")
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        workbook = xlwt.Workbook()
        sheet1 = workbook.add_sheet('统计结果', cell_overwrite_ok=True)
        sheet1.write(0, 0, "target")
        sheet1.write(0, 1, "人工标注数量")
        sheet1.write(0, 2, "接口结果数量")
        sheet1.write(0, 3, "一致数量")
        sheet1.write(0, 4, "准确率")
        sheet1.write(0, 5, "召回率")
        sheet1.write(0, 6, "F1值")
        for i in range(0, len(target_list)):
            sheet1.write(i + 1, 0, target_list[i])
            sheet1.write(i + 1, 1, pn_list[i])
            sheet1.write(i + 1, 2, rn_list[i])
            sheet1.write(i + 1, 3, tn_list[i])
            sheet1.write(i + 1, 4, precision_list[i])
            sheet1.write(i + 1, 5, recall_list[i])
            sheet1.write(i + 1, 6, f1_list[i])
        workbook.save(rootPath + '\\testresults\\resultfile\\' + now + target_result_file)
        return rootPath + '\\testresults\\resultfile\\' + now + target_result_file


if __name__ == '__main__':
    # 参数解释：url+路径，方法，接口名，标签文件，测试用例文件，测试用例中的字段列，校验的返回数据字段，原始数据测试结果文件，标签prf的结果文件
    # GetRequests().get_request("http://192.16.1.79:8900/intention/v2/tcnn", "GET", "intent",
    #                           "intent\\dermatology\\target.txt",
    #                           "intent\\dermatology\\dermatology_test_data_3995.csv", ["sentence"], "label",
    #                           "dermatology_intention_test_result.xls",
    #                           "dermatology_intention_target_test_result.xls")

    GetRequests().get_request("http://192.168.26.105:30014/gynaecology_intention/v1", "GET", "pro_intent",
                              "intent\\gynaecology\\线上target.txt",
                              "intent\\gynaecology\\妇科-总测试数据-线上线下.csv",
                              ["sentence", "False", "gynaecology"], "label",
                              "gynaecology_intention_test_evn.xls",
                              "gynaecology_intention_target_test_evn.xls")
