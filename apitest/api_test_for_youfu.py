# -*- coding: UTF-8 -*-
'''
Created on 2020/6/11
@File  : api_test_for_youfu.py
@author: ZL
@Desc  :
'''
import pandas
from io import BytesIO
import time
from flask import Flask, request, Response
from commonfunc.change_data_type import ChangeDataType
import os
from api.get_requests import GetRequests

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]

app = Flask(__name__)  # 创建一个服务，赋值给APP


# , rename_dict, col_order
def trans_record_data_to_io(data):
    """
    将列表数据转为excel的io对象
    """
    rename_dict = {"col1": "target", "col2": "人工标注数量", "col3": "接口结果数量", "col4": "一致数量", "col5": "准确率", "col6": "召回率",
                   "col7": "F1值"}
    col_order = ["target", "人工标注数量", "接口结果数量", "一致数量", "准确率", "召回率", "F1值"]
    file = BytesIO()
    df = pandas.DataFrame(data)
    df.rename(columns=rename_dict, inplace=True)
    writer = pandas.ExcelWriter(file, engine='xlsxwriter')
    df.to_excel(writer, index=False, columns=col_order)
    writer.save()
    return file.getvalue()


@app.route('/test_result/download', methods=['GET'])
def download():
    data_list = []
    data = {}
    url = request.form.get("url")  # 获取接口请求中form-data的url参数传入的值
    industry = request.form.get("industry")  # 获取接口请求中form-data的url参数传入的值
    if industry == "植发科":
        file_name = GetRequests().get_request(url, "GET", "a_intent",
                                              "intent\\hairtransplant\\target.txt",
                                              "intent\\hairtransplant\\hairtransplant_to_test_first_9998.csv", ["sentence"],
                                              "label",
                                              "hairtransplant_intention_test_result.xls",
                                              "hairtransplant_intention_target_test_result.xls")
    if industry == "妇产科":
        file_name = GetRequests().get_request(url, "GET", "a_intent",
                                              "intent\\obstetrics\\obstetrics_target.txt",
                                              "intent\\obstetrics\\obstetrics_to_test_9400.csv", ["sentence"],
                                              "label",
                                              "obstetrics_intention_test_result.xls",
                                              "obstetrics_intention_target_test_result.xls")
    if industry == "皮肤科":
        file_name = GetRequests().get_request(url, "GET", "a_intent",
                                              "intent\\dermatology\\target.txt",
                                              "intent\\dermatology\\dermatology_test_data_3995.csv", ["sentence"],
                                              "label",
                                              "dermatology_intention_test_result.xls",
                                              "dermatology_intention_target_test_result.xls")
    if industry == "肛肠科":
        file_name = GetRequests().get_request(url, "GET", "a_intent",
                                              "intent\\anorectal\\target.txt",
                                              "intent\\anorectal\\anorectal_intention_to_test_4930.csv", ["sentence"],
                                              "label",
                                              "anorectal_intention_test_result.xls",
                                              "anorectal_intention_target_test_result.xls")
    if industry == "通用":
        file_name = GetRequests().get_request(url, "GET", "a_intent",
                                              "intent\\common\\common_intent.txt",
                                              "intent\\common\\intention_common_test-6962.csv",
                                              ["sentence"], "label",
                                              "common_intention_test_result.xls",
                                              "common_intention_target_test_result.xls")
    if industry == "妇科":
        file_name = GetRequests().get_request(url, "GET", "pro_intent",
                                              "intent\\gynaecology\\线上target.txt",
                                              "intent\\gynaecology\\妇科-总测试数据-线上线下.csv",
                                              ["sentence", "xxx", "False"], "label",
                                              "gynaecology_intention_test_result.xls",
                                              "gynaecology_intention_target_test_result.xls")
    if industry == "不孕不育":
        file_name = GetRequests().get_request(url, "GET", "a_intent",
                                              "intent\\infertility\\test_target.txt",
                                              "intent\\infertility\\intention_to_test.csv", ["sentence"],
                                              "label",
                                              "infertility_intention_test_result.xls",
                                              "infertility_intention_target_test_result.xls")
    time.sleep(2)
    test_data = ChangeDataType.excel_to_dict(file_name,
                                             sheet_name="统计结果")

    for idx, temp in test_data.iterrows():
        data = {"col1": temp["target"], "col2": temp["人工标注数量"], "col3": temp["接口结果数量"],
                "col4": temp["一致数量"], "col5": temp["准确率"], "col6": temp["召回率"], "col7": temp["F1值"]}
        data_list.append(data)
        data = {}
    file_io_value = trans_record_data_to_io(data_list)
    file_name = time.strftime('%y_%m_%d-%H_%M_%S') + ".xlsx"
    return Response(
        file_io_value, mimetype="application/octet-stream",
        headers={"Content-Disposition": "attachment;filename={0}".format(file_name)}
    )


app.run(host='0.0.0.0', port=8987, debug=True)
