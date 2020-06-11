# -*- coding: UTF-8 -*-
'''
Created on 2020/5/25
@File  : test_for_api.py
@author: ZL
@Desc  :
'''
import os
from api.get_requests import GetRequests
from flask import Flask, jsonify, request, Response
import pandas as pd
from io import BytesIO  # 内存管理器(excel存入内存)

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]

data = {"周璐": {"周璐": "中级测试工程师"},
        "贺聪": {"贺聪": "初级测试工程师"}, "蔡津津": {"蔡津津": "中级测试工程师"},
        "林瑞卿": {"林瑞卿": "中级测试工程师"}, "林婷婷": {"林婷婷": "初级测试工程师"},
        "马钰承": {"马钰承": "初级测试工程师"}, "朱朋": {"朱朋": "初级测试工程师"},
        "吴建清": {"吴建清": "测试经理"}
        }

err = {"Test": "查无此人",
       123: "参数错误"
       }

app = Flask(__name__)  # 创建一个服务，赋值给APP


# @app.route('/get_user', methods=['post'])  # 指定接口访问的路径，支持什么请求方式get，post
# # key_values方式传参
# def get_user():
#     username = request.form.get('username')  # 获取接口请求中form-data的username参数传入的值
#     if username in data:  # 判断请求传入的参数是否在字典里
#         # 如果在的话，则返回data对应key的值转成的json串信息
#         return jsonify(data[username])
#     else:
#         # 如果不在的话，返回err对应key的value转成的json串信息
#         return jsonify(err[username])


@app.route('/pro_test_result/download', methods=['get'])
def download():
    # GetRequests().get_request("http://192.168.1.74:8900/fuke_intention/v1_42", "GET", "intent",
    #                           "intent\\gynaecology\\线上target.txt",
    #                           "intent\\gynaecology\\妇科-总测试数据-线上线下.csv", ["sentence"], "label",
    #                           "gynaecology_intention_test_result.xls",
    #                           "gynaecology_intention_target_test_result.xls")
    # excel = pd.read_excel(rootPath+"gynaecology_intention_target_test_result.xls")
    list = [{"test1", "test2"}, {"test1", "test2"}]
    excel = pd.DataFrame(list)  # 二维数组，对应表头的相应数据
    excel.columns = ["test1", "test2"]  # 表头 [xx,xx,xx,xx]
    file = BytesIO()
    excel.to_excel(file, index=False)
    response = Response(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    execl_name = 'target_test_result.xlsx'
    response.headers["Content-disposition"] = 'attachment; filename=%s' % execl_name.encode().decode('ASCII')
    response.data = file.getvalue()
    return response


app.run(host='0.0.0.0', port=8892, debug=True)
