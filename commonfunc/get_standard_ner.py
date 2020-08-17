# -*- coding: UTF-8 -*-
'''
Created on 2020/8/13 10:13
@File  : get_standard_ner.py
@author: ZL
@Desc  :
'''
import os
from commonfunc.change_data_type import ChangeDataType
import codecs

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetStandardNer:
    def get_tab_to_space(self, file1, file2):
        raw_data = codecs.open(rootPath + "\\testdata\\apidata\\" + file1, encoding='utf-8')
        result_data = codecs.open(rootPath + "\\testdata\\apidata\\" + file2, 'w', encoding='utf-8')
        for line in raw_data.readlines():
            if len(line.strip()) == 0:
                result_data.write(line.strip())
            line = line.replace("\t\t", " ")
            line = line.strip()
            if line == "O":
                line = "， O"
            if line.startswith("B_") or line.startswith("I_"):
                continue
            result_data.write(line.strip() + "\n")


if __name__ == '__main__':
    GetStandardNer().get_tab_to_space("ner\\gynaecology\\bio_char.txt", "ner\\gynaecology\\new_bio_char.txt")
