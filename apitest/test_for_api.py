# -*- coding: UTF-8 -*-
'''
Created on 2020/5/25
@File  : test_for_api.py
@author: ZL
@Desc  :
'''
from flask import Flask, jsonify, request

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


@app.route('/get_user', methods=['post'])  # 指定接口访问的路径，支持什么请求方式get，post
# key_values方式传参
def get_user():
    username = request.form.get('username')  # 获取接口请求中form-data的username参数传入的值
    if username in data:  # 判断请求传入的参数是否在字典里
        # 如果在的话，则返回data对应key的值转成的json串信息
        return jsonify(data[username])
    else:
        # 如果不在的话，返回err对应key的value转成的json串信息
        return jsonify(err[username])


app.run(host='0.0.0.0', port=8892, debug=True)
