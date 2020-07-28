# -*- coding: UTF-8 -*-
'''
Created on 2020/7/28 10:39
@File  : test_for_jieba.py
@author: ZL
@Desc  :
'''

import os
import jieba
from commonfunc.change_data_type import ChangeDataType

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class JieBaTest:

    def get_frequency(self, file):
        frequency_dict = {1: 0}
        test_data = ChangeDataType.csv_to_dict(rootPath + "\\testdata\\estest\\" + file)
        sentence_list = test_data.sentence.tolist()

        for i in sentence_list:
            try:
                if len(i) != 0:
                    words = set(list(jieba.cut(str(i))))
                    lengh = len(words)
                    if lengh in frequency_dict.keys():
                        frequency_dict[lengh] = frequency_dict[lengh] + 1
                    else:
                        frequency_dict[lengh] = 1
            except Exception as e:
                print(e,i)
        print(frequency_dict)
        print(frequency_dict.values())
        print(frequency_dict.keys())


if __name__ == '__main__':
    JieBaTest().get_frequency("男科随机10万句.csv")

# str1 = "是尿不尽是吧睡觉用手碰了下尿道口有湿湿的湿润的潮湿的"
# words = set(list(jieba.cut(str1)))
# print(len(words))
#
# str2 = "照着敲了一下，报错了！加上-f 成功了，但却发现，没办法安装任何包了，总是报这样的错误信息,这我就很纳闷了，应该没敲错吧，上网找了一下资料，于是开始修正。不要忘记前面的点 打开，在- default 前面加上镜像地址,啊哈，大功告成，随便下一个包试试速度吧。飞咯"
# words1 = list(jieba.cut(str2))
# print(len(words1))
#
# str3 = "是尿不尽是吧睡觉用手碰了下尿道口有湿湿的湿润的潮湿的是尿不尽是吧睡觉用手碰了下尿道口有湿湿的湿润的潮湿的是尿不尽是吧睡觉用手碰了下尿道口有湿湿的湿润的潮湿的是尿不尽是吧睡觉用手碰了下尿道口有湿湿的湿润的潮湿的是尿不尽是吧睡觉用手碰了下尿道口有湿湿的湿润的潮湿的"
# words2 = list(jieba.cut(str3))
# print(len(words2))
