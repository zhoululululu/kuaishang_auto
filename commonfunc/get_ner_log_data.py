# -*- coding: UTF-8 -*-
'''
Created on 2020/9/17 11:48
@File  : get_ner_log_data.py
@author: ZL
@Desc  :
'''
import os
import codecs

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetNerTestData:

    def get_ner_data(self, file,file2):
        raw_data = codecs.open(rootPath + "\\testdata\\apidata\\ner\\" + file, encoding='utf-8')
        result_data = codecs.open(rootPath + "\\testdata\\apidata\\ner\\" + file2, 'w', encoding='utf-8')
        for line in raw_data.readlines():
            if '"sentence": ' in line:
                data = "".join(eval(line)["extract"].get("sentence"))
                result_data.write(data.strip() + "\n")


if __name__ == '__main__':
    GetNerTestData().get_ner_data("ner_log.txt","ner_sentence.txt")