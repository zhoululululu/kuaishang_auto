# -*- coding: UTF-8 -*-
'''
Created on 2020/5/14
@File  : Qamatcher_Qastudio_comp.py
@author: ZL
@Desc  : 临时测试脚本，qamatcher与qastudio的对比效果
'''
import os
import time
import requests
import xlwt

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class Comp:

    def get_qamatcher_result(self):  # , test_data
        si_questions_list, question_list = [], []
        n = 1000
        i = 0
        while i < n:
            # for temp in test_data:
            params = {
                "org": "kst",
                "app": "marketing_robot",
                "industry": "gynaecology",
                "kb_names": ["gynaecology"],
                "question": "阴道炎严重吗"
            }
            url = "http://10.14.250.220:8086/qastudio/v2/qamatch"
            r = requests.post(url, data=params)
            result = r.json()
            print(result)
            if result["hit_question"] != "阴道炎严重吗":
                print("出错了")

            i += 1
        #     questions = result["question_list"]
        #     n = 0
        #     if len(questions) == 5:
        #         for i in questions:
        #             if i != None:
        #                 si_questions_list.append(i)
        #             else:
        #                 si_questions_list.append("\n")
        #             # question_list.append(temp[4])
        #     else:
        #         for i in questions:
        #             n = n + 1
        #             if i != None:
        #                 si_questions_list.append(i)
        #             else:
        #                 si_questions_list.append("\n")
        #         while n < 5:
        #             si_questions_list.append("\n")
        #             # question_list.append(temp[4])
        #             n = n + 1
        #     si_questions_list.append("\n")
        #     question_list.append("\n")
        # n = 0
        # return si_questions_list, question_list

    def get_qastudio_result(self, test_data):
        si_questions_list, question_list = [], []
        for temp in test_data:
            url = "http://192.168.26.105:30066/qastudio/v1/knowledgebases?org={}&app={}&kb_names={}&question={}&init=150&final=5".format(
                temp[0], temp[1], temp[3], temp[4])
            r = requests.get(url)
            result = r.json()
            data = result["data"]
            n = 0
            for i in data:
                n = n + 1
                if i["question"] != None:
                    si_questions_list.append(i["question"])
                else:
                    si_questions_list.append("\n")
                question_list.append(temp[4])
            si_questions_list.append("\n")
            question_list.append("\n")
        return si_questions_list, question_list

    def get_comp(self, data):
        now = time.strftime('%y_%m_%d-%H_%M_%S')
        s1_questionlist1, question_list = Comp.get_qamatcher_result(self, data)
        s2_questionlist2, question_list_1 = Comp.get_qastudio_result(self, data)
        print(question_list)
        print(question_list_1)
        print(s1_questionlist1)
        print(s2_questionlist2)
        workbook = xlwt.Workbook()
        sheet1 = workbook.add_sheet('结果', cell_overwrite_ok=True)
        sheet1.write(0, 0, "question")
        sheet1.write(0, 1, "similary question-qamatcher")
        sheet1.write(0, 2, "similary question-qastatudio")
        for i in range(0, len(s1_questionlist1)):
            sheet1.write(i + 1, 0, question_list_1[i])
            sheet1.write(i + 1, 1, s1_questionlist1[i])
        for i in range(0, len(s2_questionlist2)):
            sheet1.write(i + 1, 2, s2_questionlist2[i])
        workbook.save(rootPath + '\\testresults\\resultfile\\' + now + "qa_comp_result22.xls")


if __name__ == '__main__':
    # data = [["kst", "marketing_robot", "andrology", '["andrology"]', "包皮过长怎么办啊"],  # 男科
    #         ["kst", "marketing_robot", "andrology", '["andrology"]', "尿频尿急怎么治"],
    #         ["kst", "marketing_robot", "andrology", '["andrology"]', "早射怎么回事"],
    #         ["kst", "marketing_robot", "andrology", '["andrology"]', "阳痿是什么情况呢"],
    #         ["kst", "marketing_robot", "andrology", '["andrology"]', "早泄是什么情况呢"],
    #         ["kst", "marketing_robot", "andrology", '["andrology"]', "包皮炎啊"],
    #         ["kst", "marketing_robot", "andrology", '["andrology"]', "附睾炎是什么呀"],
    #         ["kst", "marketing_robot", "andrology", '["andrology"]', "阴囊炎呢"],
    #         ["kst", "marketing_robot", "andrology", '["andrology"]', "包茎治疗多少钱啊"],
    #         ["kst", "marketing_robot", "andrology", '["andrology"]', "包皮 有疙瘩"],
    #         ["kst", "marketing_robot", "andrology", '["andrology"]', "早泄 这个严重吗"],
    #         ["kst", "marketing_robot_diy", "psoriasis", '["psoriasis"]', "能治好吗"],  # 银屑病
    #         ["kst", "marketing_robot_diy", "psoriasis", '["psoriasis"]', "脓疱病 这病能根治吗"],
    #         ["kst", "marketing_robot_diy", "psoriasis", '["psoriasis"]', "头癣咋治疗"],
    #         ["kst", "marketing_robot_diy", "psoriasis", '["psoriasis"]', "牛皮癣好治吗"],
    #         ["kst", "marketing_robot_diy", "psoriasis", '["psoriasis"]', "斑秃能治么"],
    #         ["kst", "marketing_robot_diy", "psoriasis", '["psoriasis"]', "牛皮癣传染吗"],
    #         ["kst", "marketing_robot_diy", "psoriasis", '["psoriasis"]', "银屑病 这病能治好吗？"],
    #         ["kst", "marketing_robot_diy", "psoriasis", '["psoriasis"]', "头皮癣能除根吗"],
    #         ["kst", "marketing_robot_diy", "psoriasis", '["psoriasis"]', "银屑病和牛皮癣是一样的吗"],
    #         ["kst", "marketing_robot_diy", "psoriasis", '["psoriasis"]', "牛皮癣和银屑病的区别"],
    #         ["kst", "marketing_robot_diy", "psoriasis", '["psoriasis"]', "冬季牛皮癣复发吗"],
    #         ["kst", "marketing_robot_diy", "vitiligo", '["vitiligo"]', "白斑会扩散吗"],  # 白癜风
    #         ["kst", "marketing_robot_diy", "vitiligo", '["vitiligo"]', "白癜风能完全医好吗"],
    #         ["kst", "marketing_robot_diy", "vitiligo", '["vitiligo"]', "白癜风会传染吗"],
    #         ["kst", "marketing_robot_diy", "vitiligo", '["vitiligo"]', "请问遗传性白癫风病能治好吗"],
    #         ["kst", "marketing_robot_diy", "vitiligo", '["vitiligo"]', "白癜风有什么危害呢"],
    #         ["kst", "marketing_robot_diy", "vitiligo", '["vitiligo"]', "白癜风会遗传么"],
    #         ["kst", "marketing_robot_diy", "vitiligo", '["vitiligo"]', "为什么会得白癜风"],
    #         ["kst", "marketing_robot_diy", "vitiligo", '["vitiligo"]', "白斑吃什么药好"],
    #         ["kst", "marketing_robot_diy", "vitiligo", '["vitiligo"]', "白斑这是什么原因造成的"],
    #         ["kst", "marketing_robot_diy", "vitiligo", '["vitiligo"]', "怎么确诊是不是白癜风"],
    #         ["kst", "marketing_robot_diy", "vitiligo", '["vitiligo"]', "白癜风早期症状是什么"],
    #         ["kst", "marketing_robot_diy", "vitiligo", '["vitiligo"]', "白斑和白癜风有啥区别"]
    #         ]
    # test = Comp()
    # test.get_comp(data)
    Comp().get_qamatcher_result()
