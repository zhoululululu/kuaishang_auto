# -*- coding: UTF-8 -*-
'''
Created on 2020/3/6
@File  : item_process.py
@author: ZL
@Desc  :
'''

from commonfunc.get_config import GetXpath
import time
from commonfunc.change_data_type import ChangeDataType
import os
from selenium import webdriver
import xlwt
import pandas as pd

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class ItemProcess:

    def __init__(self):
        '''
        定义部分初始化内容;
        output,input list,config等
        '''
        self.c = GetXpath().get_xpth()
        self.test_data, self.test_data2, self.inp_list = [], [], []
        self.robot_type, self.robot_dialog, self.robot_num = [], [], []
        self.server_type, self.server_dialog, self.server_num = [], [], []

    @staticmethod
    def open_chrome(url):
        '''
        初始化driver，打开页面
        '''
        # 适配chrome_driver
        chrome_driver = "E:/chromedriver/chromedriver"
        driver = webdriver.Chrome(chrome_driver)
        driver.set_window_size(500, 600)
        driver.get(url)
        return driver

    def get_style(self):
        '''
        设置高亮；以便后续输出excel中，针对client数据进行高亮效果
        '''
        style = xlwt.XFStyle()
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['light_green']
        style.pattern = pattern
        return style

    def get_test_data(self, file):
        # 获取excel中对话信息
        self.test_data = ChangeDataType.excel_to_dict(rootPath + "\\testdata\\uidata\\" + file, "评测集")
        # 定义client_list,server_list,以及no_list,sentence num
        client_list, client_no_list, c_list, c_no_list = [], [], [], []
        # 为了首句对齐
        for idx, temp in self.test_data.iterrows():
            # 读取client的话术
            if temp["type"] == "CLIENT":
                c_list.append(temp["sentence"])
                c_no_list.append(temp["num"])
            # Over时,标记做拼接
            if temp["type"] == "OVER":
                client_list.append(c_list)
                client_no_list.append(c_no_list)
                c_list, c_no_list = [], []
        return client_list, client_no_list

    def item_process(self, url, file, dialog_result_file, comp_result_file):
        '''
        :param url: UI 地址
        :param file: 测试集存放文件
        '''
        # 定义n,before_oup
        n, before_oup = 0, ""
        # 调用函数获取client_list(client对轮对话数据),及其对应的client_no_list(多轮对话的num信息)
        client_list, client_no_list = ItemProcess.get_test_data(self, file)
        # 循环每一段中client对话
        for j in range(0, len(client_list)):
            # 调用方法打开页面
            driver = ItemProcess.open_chrome(url)
            # 拆分各段的client对话信息
            c_list = client_list[j]
            c_no_list = client_no_list[j]
            # 循环每一段client对话的具体信息
            for i in range(0, len(c_list)):
                n = n + 1
                # client话术输入输入框，拼接在list中
                self.inp_list.append(c_list[i])
                # 定位输入框，输入对应信息
                driver.find_element_by_xpath(self.c["edit_input"]).send_keys(str(c_list[i]) + "\n")
                ItemProcess.get_robot_list_join(self, "CLIENT", str(c_list[i]), str(n))  # 拼接client信息，方便后期输出
                # 对话开始需要有一定时间获取客服对话
                if n == 1:
                    time.sleep(6)
                    wait_time = 6
                # 判断client是否连续发送
                elif i < len(c_list) - 1 and c_no_list[i] == c_no_list[i + 1] - 1:
                    time.sleep(2)
                    wait_time = 7
                else:  # 对话结尾预留一定空间，多次读取客服回复
                    time.sleep(2)
                    wait_time = 0

                # 通过wait_time变量控制循环读取last客服回复
                while wait_time <= 6:
                    wait_time += 1
                    time.sleep(1)
                    if driver.find_element_by_xpath(self.c["kf_output"]):
                        if driver.find_element_by_xpath(self.c["kf_output"]).text != before_oup:
                            oup = driver.find_element_by_xpath(self.c["kf_output"]).text
                            n = n + 1
                            ItemProcess.get_robot_list_join(self, "SERVER", oup, str(n))
                            before_oup = oup
            driver.quit()
            # 一段对话结束，拼接转行，重置sentence num
            ItemProcess.get_robot_list_join(self, "OVER", "##", "\n")
            n = 0
        ItemProcess.dialog_to_excel(self, dialog_result_file)
        ItemProcess.comp_to_excel(self, comp_result_file)

    def get_robot_list_join(self, robot_type, robot_dialog, robot_num):
        '''
        拼接robot list值：type,dialog,num等
        '''
        self.robot_type.append(robot_type)
        self.robot_dialog.append(robot_dialog)
        self.robot_num.append(robot_num)
        return self.robot_type, self.robot_dialog, self.robot_num

    def get_server_list_join(self):
        '''
        拼接server list值：type,dialog,num等
        '''
        self.server_type = self.test_data.type.tolist()
        self.server_dialog = self.test_data.sentence.tolist()
        self.server_num = self.test_data.num.tolist()

    def dialog_to_excel(self, dialog_result_file):
        '''
        输出excel格式的机器人对话效果
        '''
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        # 三列数据：num,type,sentence，使用pandas的Dataframe输出excel
        result_data = pd.DataFrame({"num": self.robot_num, "type": self.robot_type, "sentence": self.robot_dialog},
                                   columns=["num", "type", "sentence"])
        result_data.to_excel(rootPath + '\\testresults\\resultfile\\' + now + dialog_result_file)

    def comp_to_excel(self, comp_result_file):
        '''
        输出excel格式的对话对比效果，使用#做对齐效果，根据client做高亮
        '''
        ItemProcess.get_server_list_join(self)
        m, n, num = 0, 0, 0
        while n < len(self.server_num):
            if m < len(self.robot_num):
                if self.server_type[n] == self.robot_type[m]:
                    pass
                else:
                    if self.server_type[n] in ["SERVER", "CLIENT", "OVER"]:
                        self.robot_num.insert(m, "##")
                        self.robot_type.insert(m, "##")
                        self.robot_dialog.insert(m, "##")
            else:
                self.robot_num.insert(m, "##")
                self.robot_type.insert(m, "##")
                self.robot_dialog.insert(m, "##")
            m = m + 1
            n = n + 1

        now = time.strftime('%y_%m_%d-%H_%M_%S')
        workbook = xlwt.Workbook()
        sheet1 = workbook.add_sheet('对比结果', cell_overwrite_ok=True)
        sheet1.write(0, 0, "num")
        sheet1.write(0, 1, "server_role")
        sheet1.write(0, 2, "server_sentence")
        sheet1.write(0, 3, "robot_role")
        sheet1.write(0, 4, "robot_sentence")
        for l in range(0, len(self.server_num)):
            if self.server_type[l] != "OVER" and self.robot_type[l] != "OVER":
                num += 1
            else:
                num = 0
            if self.server_type[l] != "CLIENT":
                sheet1.write(l + 1, 0, num)
                sheet1.write(l + 1, 1, self.server_type[l])
                sheet1.write(l + 1, 2, self.server_dialog[l])
                sheet1.write(l + 1, 3, self.robot_type[l])
                sheet1.write(l + 1, 4, self.robot_dialog[l])
            else:
                sheet1.write(l + 1, 0, num)
                sheet1.write(l + 1, 1, self.server_type[l], style=ItemProcess.get_style(self))
                sheet1.write(l + 1, 2, self.server_dialog[l], style=ItemProcess.get_style(self))
                sheet1.write(l + 1, 3, self.robot_type[l], style=ItemProcess.get_style(self))
                sheet1.write(l + 1, 4, self.robot_dialog[l], style=ItemProcess.get_style(self))
        workbook.save(rootPath + '\\testresults\\resultfile\\' + now + comp_result_file)
