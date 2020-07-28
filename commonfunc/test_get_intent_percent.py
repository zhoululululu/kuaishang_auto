# -*- coding: UTF-8 -*-
'''
Created on 2020/5/15
@File  : test_get_intent_percent.py
@author: ZL
@Desc  :
'''

from api.get_intent import GetIntent
from common.change_data_type import ChangeDataType
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetPercent:
    common_intent = ["描述就诊史", "描述生理现象", "描述症状", "确定联系意愿", "无", "咨询QQ", "咨询病因", "咨询传染", "咨询地址", "咨询电话", "咨询副作用",
                     "咨询公立私立", "咨询公司介绍", "咨询恢复期", "咨询价格", "咨询检查方式", "咨询检查价格", "咨询检查时长", "咨询疗程", "咨询疗效", "咨询留疤",
                     "咨询路线", "咨询麻醉", "咨询上班时间", "咨询食疗", "咨询疼痛程度", "咨询危害", "咨询微信", "咨询项目介绍", "咨询药物", "咨询遗传", "咨询优惠活动",
                     "咨询支付方式", "咨询治疗方式", "咨询住院", "咨询注意事项", "咨询专家"]

    beauty_intent = ["咨询术后注意事项", "描述就诊史", "描述症状", "确定预约时间", "退款", "无", "咨询QQ", "咨询不住院", "咨询材料", "咨询成功案例", "咨询成功率",
                     "咨询地址", "咨询电话", "咨询动刀", "咨询二次消费", "咨询副作用", "咨询公立私立", "咨询公司介绍", "咨询贵不贵", "咨询后遗症", "咨询恢复期",
                     "咨询会不会肿胀", "咨询技术", "咨询价格", "咨询疗程", "咨询疗效", "咨询留疤", "咨询路线", "咨询麻药", "咨询区别", "咨询上班时间", "咨询手术时长",
                     "咨询术前准备", "咨询疼痛程度", "咨询微信", "咨询维持时间", "咨询项目介绍", "咨询仪器", "咨询优惠活动", "咨询优势", "咨询支付方式", "咨询治疗方式",
                     "咨询治疗时长", "咨询住院", "咨询专家"]

    ebh_intent = ["描述就诊史", "描述症状", "确定预约时间", "无", "咨询QQ", "咨询病因", "咨询地址", "咨询电话", "咨询动刀", "咨询公立私立", "咨询公司介绍", "咨询价格",
                  "咨询检查方式", "咨询检查费用", "咨询疗程", "咨询疗效", "咨询路线", "咨询上班时间", "咨询食疗", "咨询危害", "咨询微信", "咨询项目介绍", "咨询药物",
                  "咨询治疗方式", "咨询住院", "咨询专家"]

    rxk_intent = ["咨询专家", "咨询药物", "咨询治疗方式", "咨询检查方式", "咨询价格", "咨询食疗", "咨询危害", "咨询副作用", "咨询动刀", "咨询项目介绍", "咨询病因",
                  "咨询疗效", "咨询疼痛程度", "咨询术后注意事项", "咨询术前准备", "咨询住院", "咨询疗程", "咨询症状", "描述症状", "咨询公司介绍", "咨询电话", "咨询微信",
                  "咨询QQ", "咨询路线", "咨询公立私立", "咨询地址", "咨询上班时间", "无", "确定预约时间", "描述就诊史"]

    def get_ebh_intent_percent(self):
        n = 0
        m = 0
        else_list1, else_list2 = [], []
        acount = len(self.ebh_intent)
        for i in range(0, len(self.ebh_intent)):
            if self.ebh_intent[i] in self.common_intent:
                n = n + 1
            else:
                else_list1.append(self.rxk_intent[i])
        for i in range(0, len(self.ebh_intent)):
            if self.ebh_intent[i] in self.beauty_intent:
                m = m + 1
            else:
                else_list2.append(self.rxk_intent[i])

        print("--------耳鼻喉科室-------")
        print("耳鼻喉科室总意图数量：", acount)
        print("通用意图覆盖耳鼻喉的意图比例：", '{:.2f}%'.format(n / len(self.ebh_intent)))
        print("不在范围内意图：", else_list1)
        print("医美意图覆盖耳鼻喉的意图比例", '{:.2f}%'.format(m / len(self.ebh_intent)))
        print("不在范围内意图：", else_list2)

    def get_rxk_intent_percent(self):

        n = 0
        m = 0
        else_list1, else_list2 = [], []
        acount = len(self.rxk_intent)
        for i in range(0, len(self.rxk_intent)):
            if self.rxk_intent[i] in self.common_intent:
                n = n + 1
            else:
                else_list1.append(self.rxk_intent[i])

        for i in range(0, len(self.rxk_intent)):
            if self.rxk_intent[i] in self.beauty_intent:
                m = m + 1
            else:
                else_list2.append(self.rxk_intent[i])

        print("--------乳腺科室-------")
        print("乳腺科室总意图数量：", acount)
        print("通用意图覆盖乳腺科的意图比例：", '{:.2f}%'.format(n / len(self.rxk_intent)))
        print("不在范围内意图：", else_list1)
        print("医美意图覆盖乳腺科的意图比例", '{:.2f}%'.format(m / len(self.rxk_intent)))
        print("不在范围内意图：", else_list2)

    def get_ebh_all_about_intent(self):
        n = 0
        all_list = []
        else_list = []
        for i in range(0, len(self.ebh_intent)):
            if self.ebh_intent[i] in self.common_intent:
                if self.ebh_intent[i] in self.beauty_intent:
                    n = n + 1
                    all_list.append(self.ebh_intent[i])
                else:
                    else_list.append(self.ebh_intent[i])
            else:
                else_list.append(self.ebh_intent[i])
        print("--------耳鼻喉科室-------")
        print("通用意图/医美意图共同覆盖耳鼻喉的意图比例：", '{:.2f}%'.format(n / len(self.ebh_intent)))
        print(all_list)
        print(else_list)
        return all_list

    def get_rxk_all_about_intent(self):
        n = 0
        all_list = []
        else_list = []
        for i in range(0, len(self.rxk_intent)):
            if self.rxk_intent[i] in self.common_intent:
                if self.rxk_intent[i] in self.beauty_intent:
                    n = n + 1
                    all_list.append(self.rxk_intent[i])
                else:
                    else_list.append(self.rxk_intent[i])
            else:
                else_list.append(self.rxk_intent[i])
        print("--------乳腺科室-------")
        print("通用意图/医美意图共同覆盖乳腺科的意图比例：", '{:.2f}%'.format(n / len(self.rxk_intent)))
        print(all_list)
        print(else_list)
        return all_list

    def get_test_env_request(self):
        # 乳腺科意图测试
        GetIntent.get_intent(self, "http://192.168.1.79:8900/intention/v2/tcnn?utterance={}",
                             "intent\\galactophore_about_two_target.txt",
                             "galactophore_case_all.csv",
                             "galactophore_all_test_result.xls", "galactophore_test_target_result.xls")

        # 耳鼻喉意图测试
        GetIntent.get_intent(self, "http://192.168.1.79:8900/intention/v2/tcnn?utterance={}",
                             "intent\\otolaryngology\\otolaryngology_about_two_target.txt",
                             "otolaryngology\\otolaryngology_case_all.csv",
                             "otolaryngology_all_test_result.xls", "otolaryngology_test_target_result.xls")

    def get_beauty_request(self):
        # 意图测试-医美
        GetIntent.get_pro_intent(self, "http://10.14.250.101:10000/x/identify/v1/ner/slot/identify",
                                 "beauty_intent.txt",
                                 "galactophore_case_all.csv",
                                 "galactophore_all_test_result.xls")

    def get_intention_target(target_file):
        target_list = ChangeDataType.txt_to_dict(rootPath + "\\testdata\\apidata\\intent\\" + target_file)
        return target_list

    def get_percent(self, str1, str2, before_intent, after_intent):
        n = 0
        m = 0
        else_list = []
        acount = len(before_intent)
        for i in range(0, len(before_intent)):
            if before_intent[i] in after_intent:
                n = n + 1
            else:
                else_list.append(before_intent[i])
        print("--------" + str1 + "科室-------")
        print(str1 + "总意图数量：", len(before_intent))
        print(str2 + "总意图数量：", len(after_intent))
        print("共同意图数量：", n)
        print(str2 + "意图覆盖" + str1 + "的意图比例：", '{:.2f}%'.format(n / len(before_intent) * 100))
        print(str1 + "不在范围内意图：", else_list)

    def get_pro_request(self, api_url, target_file, test_data_file, test_result_file):
        # 意图测试
        GetIntent.get_pro_intent(self,
                                 api_url,
                                 target_file,
                                 test_data_file,
                                 test_result_file)

    def get_test_request(self, api_url, target_file, test_data_file, test_result_file):
        # 意图测试
        GetIntent.get_intent(self,
                             api_url,
                             target_file,
                             test_data_file,
                             test_result_file)

if __name__ == '__main__':

    test = GetPercent()
    test.get_test_env_request()
    # test.get_ebh_intent_percent()
    # test.get_rxk_intent_percent()
    # test.get_ebh_all_about_intent()
    # test.get_rxk_all_about_intent()
    # test.get_request()
    # test.get_beauty_request()
    # psoriasis_intention_list = GetPercent.get_intention_target("psoriasis\\target.txt")
    # dermatology_intention_list = GetPercent.get_intention_target("dermatology\\target.txt")
    # leucoderma_intention_list = GetPercent.get_intention_target("leucoderma\\target.txt")
    # test.get_percent("银屑病", "皮肤科", psoriasis_intention_list, dermatology_intention_list)
    # test.get_percent("白癜风", "皮肤科", leucoderma_intention_list, dermatology_intention_list)
    # test.get_pro_request("http://robotchat.kuaishangkf.com/x/identify/v1/re_unify/identify",
    #                      "intent\\dermatology\\andpsorasis.txt", "psoriasis\\psoriasis_test_data.csv",
    #                      "psoriasis_test_result.xls")
    # test.get_test_request("http://192.168.1.79:8900/intention/v2/tcnn?utterance={}",
    #                       "intent\\dermatology\\andpsorasis.txt",
    #                       "psoriasis\\psoriasis_test_500.csv",
    #                       "psoriasis_test_result.xls")
    # test.get_test_request("http://192.168.1.79:8900/intention/v2/tcnn?utterance={}",
    #                       "intent\\dermatology\\andleucoderma.txt",
    #                       "leucoderma\\leucoderma_test_500.csv",
    #                       "leucoderma_test_result.xls")
    # test.get_pro_request("intent\\dermatology\\andpsorasis.txt", "leucoderma\\leucoderma_test_data.csv", "leucoderma_test_result.xls",
    #                      "leucoderma")
