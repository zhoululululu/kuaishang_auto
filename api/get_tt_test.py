# -*- coding: UTF-8 -*-
'''
Created on 2020/6/19 10:38
@File  : get_zp_test.py
@author: ZL
@Desc  :
'''

from requests_toolbelt import MultipartEncoder,multipart
import requests
from urllib import parse
import json

parameter = {
    "aaa": 1
}
file_name = r'"111.wav";opcode="transcribe_audio";sessionid="session:1";tmp_entry_id="2107512132";filename="111.wav";type="21";time="1528968385149";reqid="485969d2-0c93-42cd-bcd5-4f3c1ccabccb";latitude="-1";location="-1";language="chinese";uId="null";kId="102";aId="001";grammarname="";contentId="session:1";sceneId="-1";sr="1";isAddPunct="off";isTransDigit="on";isButterFly="off"'
print(file_name)
data = MultipartEncoder(
    fields=[(json.dumps(file_name),
             ("111.wav", open("C:/Users/huyx/Downloads/111.wav", "rb"), "audio/wav"))
            ])

print(data)
header = {
    "Content-Type": data.content_type,
    "apikey": "8e306cd0195da10795db96f911a3cf5411965941a54f634a5314e031b504193a80f1f5c50cf3f6225cc9fe63efa9f6bb51ba1ac2d82a2ab35c3e99dae2a8c6fc0a9eb647e01e6bb07e3eab48539df3a7b7e8cf6be74caf64ff5e28d94e973f7da48c5c38937f965080bdd28b64d72e52ddbd23cd260569777c4717e70f15cb06"
}

url = "http://10.0.220.240:8080/QianYuSrv/uploader"
print(data)
try:
    response = requests.post(url, params=parameter, data=data, headers=header, timeout=1000)
    print(response.text)
    response.close()

except Exception as e:
    print(e)
