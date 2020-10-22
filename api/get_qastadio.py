# -*- coding: UTF-8 -*-
'''
Created on 2020/8/7 14:43
@File  : get_qastadio.py
@author: ZL
@Desc  :
'''
from commonfunc.change_data_type import ChangeDataType
import os
import requests
import pandas
import codecs

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetQaStudio:
    def get_qa_studio_test_data(self, file):
        test_data = ChangeDataType.file_to_dict(rootPath + "\\testdata\\apidata\\similary\\psoriasis\\" + file)
        file = codecs.open(rootPath + "\\testdata\\apidata\\similary\\psoriasis\\" + "testdata.txt",'w', encoding='utf-8')
        sentence_list = test_data.sentence.tolist()
        n = 0
        for i in sentence_list:
            n += 1
            file.write('{"faqId":"' + str(n) + '","question":"' + i + '"},')

    def get_qastudio_result(self, file):
        test_data = GetQaStudio.get_qa_studio_test_data(self, file)
        score_list, sentence_list, question_list, answer_list = [], [], [], []
        sentence, question, answer, score = [], [], [], []
        for temp in test_data:
            params = {
                "org": "kst",
                "app": "marketing_robot_diy",
                "industry": "psoriasis",
                "kb_names": '["psoriasis"]',
                "question": temp,
                "init": 150,
                "final": 150
            }
            url = "http://192.168.26.105:30066/qastudio/v1/knowledgebases"
            r = requests.get(url, params=params)
            result = r.json()
            data = result["data"]
            # print(data)
            if data != []:
                for i in data:
                    if i["score"] < 0.85:
                        print(temp)
                    else:
                        sentence.append(temp)
                        question.append(i["question"])
                        answer.append(i["answer"])
                        score.append(i["score"])
                sentence_list.append(sentence)
                question_list.append(question)
                answer_list.append(answer)
                score_list.append(score)
                sentence, question, answer, score = [], [], [], []

        result_data = pandas.DataFrame(
            {"sentence": sentence_list, "question": question_list, "answer": answer_list, "score": score_list})
        result_data.to_excel(rootPath + "\\testresults\\resultfile" + "qastadio测试结果.xls")


if __name__ == '__main__':
    GetQaStudio().get_qa_studio_test_data("psoriasis_to_test.csv")
