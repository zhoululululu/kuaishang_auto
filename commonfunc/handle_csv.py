# -*- coding: utf-8 -*-
"""
===========================
   File Name：     handle_csv_to_list
   Description :
   Author :       lintt
   date：          2020/7/29
===========================
"""
# from common.handle_path import datas_path
import os
import csv

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class HandleCsv:
    def __init__(self, file_path):
        self.file_path = file_path
        with open((self.file_path), 'r', encoding="utf-8") as self.csvFile:
            self.reader = csv.reader(self.csvFile)
            self.data = list(self.reader)

    def read_title(self):
        titles = []
        for title in self.data[0]:
            # title.strip(r"\ufeff")
            titles.append(title)
        return titles

    def read_all_data(self):
        all_data = []
        titles = self.read_title()
        for row in self.data[1:]:
            data = []
            for val in row:
                data.append(val)
            res = dict(zip(titles, data))
            all_data.append(res)
        return all_data

    # def csv_to_list(self):
    #     with open((self.file_path),encoding="utf-8") as csvFile:
    #         reader = csv.reader(csvFile)
    #         data = list(reader)
    #         title,dataList = [],[]
    #         for tit in data[0]:
    #             title.append(tit)
    #         for row in data[1:]:
    #             dataList.append(row[0])
    #         return dataList


if __name__ == '__main__':
    file_path = os.path.join(rootPath + "\\testdata\\apidata\\intent\\andrology\\", "andrology_intent.csv")
    data = HandleCsv(file_path)
    print(data.read_all_data())
