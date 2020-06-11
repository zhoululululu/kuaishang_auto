# -*- coding: UTF-8 -*-
'''
Created on 2020/3/26
@File  : Test.py
@author: ZL
@Desc  :廖老师兴趣题：字符串全排列
'''
import itertools
import operator
import pandas


class Test:
    def __init__(self):
        self.count = 0
        self.s_result = []

    def test1(self, str, i):
        s_begin = list(str)
        if i == len(s_begin):
            self.count = self.count + 1
            self.s_result.append(str)
        else:
            for j in range(i, len(s_begin)):
                s_begin[j], s_begin[i] = s_begin[i], s_begin[j]
                Test.test1(self, s_begin, i + 1)

        return self.s_result

    def test2(self, str):
        n = 0
        s_result = []
        s_begin = list(str)
        for x in itertools.permutations(s_begin, len(s_begin)):
            s_result.append(x)
            n = n + 1
        print(s_result)
        print(n)

    def test3(self):
        i = 6
        j = 6.0
        if i == j:
            result = "true"
        else:
            result = "false"
        print(result)

    def test4(self, i, j):
        if i == j:
            result = "true"
        else:
            result = "false"
        print(result)
        return result

    # test = Test()
    # test.test3()
    # test.test2("abcdef")
    # print(test.test1("abcdef", 0))

    def com_list(self):
        l1 = ["A", "B", "C"]
        l2 = ["A", "C", "B"]
        l1.sort()
        l2.sort()
        print(l1)
        print(l2)
        print(operator.eq(l1, l2))


test = Test()
test.com_list()

# label_list = ['无', '假体隆鼻', '玻尿酸丰泪沟', '鼻部软骨取出', '牙齿矫正', '祛增生性疤痕', '口腔整形', '鼻头缩小',
#               '祛嘴角纹', '瘦腿', '鼻部塑形', '腋下脱毛', '唇裂手术', '私密漂红', '嫩肤', '植发', '阴道紧缩',
#               '鼻部假体取出', '微笑唇整形', '祛疣', '腰腹部吸脂', '鼻中隔整形', '牙齿种植', '比基尼脱毛',
#               '洗美瞳线', '眼尾下垂矫正', '纹眼线', '私密整形', '丰太阳穴', '鼻孔缩小', '皮肤美白', '祛鱼尾纹',
#               '乳头整形', '男士脱毛', '祛疤', '祛晒斑', '祛红血丝', '私密修复', '根管治疗', '鼻部填充', '自体丰下巴',
#               '补牙', '发际线种植', '祛妊娠斑', '大小眼矫正', '祛法令纹', '臀部脱毛', '漂唇', '牙齿美白', '自体脂肪填充',
#               '打瘦脸针', '乳头缩小', '祛胎记', '提眉', '私密保养', '纹眉', '祛痘坑', '腿部吸脂', '祛黑眼圈', '假体取出',
#               '眼睑调整', '祛黑头', '鼻翼缩小', '人中整形', '打除皱针', '手臂脱毛', '打水光针', '大小脸矫正', '乳晕整形',
#               'M唇成型', '胸部提升', '纹美瞳线', '脸部吸脂', '射频紧肤', '祛颈纹', '祛汗管瘤', '玻尿酸祛川字纹', '胸部缩小',
#               '处女膜修复', '丰苹果肌', '注射卧蚕', '私密脱毛', '丰脸颊', '鼻尖整形', '眼部整形', '线雕', '丰臀', '脱毛',
#               '唇部脱毛', '阴唇缩小', '洗纹身', '打瘦腿针', '祛额区皱纹', '臀部吸脂', '祛抬头纹', '手臂吸脂', '洁牙', '祛鼻背纹',
#               '胸部整形', '丰额头', '打V脸针', '自体脂肪隆鼻', '丰胸', '鼻部修复', '下巴整形', '鼻梁矫正', '祛川字纹', '多点双眼皮',
#               '全身脱毛', '嘟嘟唇', '吸脂', '瘦双下巴', '玻尿酸丰苹果肌', '颈部脱毛', '祛面部皱纹', '双眼皮修复', '紧肤除皱', '附乳切除',
#               '假体丰下巴', '面部塑形', '割双眼皮', '耳朵矫正', '面部填充', '丰下巴', '补水', '颌面整形', '祛蝴蝶斑', '自体丰臀', '祛黄褐斑',
#               '疤痕未拆线', '隆鼻', '假体丰胸', '毛孔收缩', '祛色斑', '纹唇', '自体软骨隆鼻', '线雕隆鼻', '祛痘印', '脱发际线鬓角', '耳部整形',
#               '吸脂瘦身', '洗眉', '祛腋臭', '下巴假体取出', '丰唇', '点痣', '玻尿酸隆鼻', '皮肤过敏修复', '祛妊娠纹', '面部脱毛', '玻尿酸丰唇',
#               '眼窝凹陷填充', '祛眼袋', '附耳切除', '面部整形', '祛褐青斑', '祛老年斑', '祛雀斑', '厚唇改薄', '祛真皮斑', '唇部整形',
#               '面部提升', '上睑下垂矫正', '鼻部整形', '注射溶解酶', '祛色沉', '自体丰胸', '祛斑', '乳头内陷矫正', '鼻部缩小', '拔牙', '双眼皮',
#               '祛眉间纹', '面部美白', '自体丰太阳穴', '腿部脱毛', '洗眼线', '祛痤疮', '酒糟鼻', '玻尿酸祛法令纹', '眉部整形', '毛周角化',
#               '眼部吸脂', '祛痘疤', '埋线双眼皮', '玻尿酸丰太阳穴', '纹纹绣', '埋线减肥', '打瘦肩针', '祛痘', '瘦脸', '自体丰唇',
#               '皮肤美容', '眼睑凹陷填充', '睫毛种植', '乳晕缩小', '狐臭整形', '丰眉弓',
#               '祛烧烫伤疤痕', '祛眼周皱纹', '磨骨', '洗纹绣', '玻尿酸丰下巴', '漂乳晕', '开眼角', '丰泪沟']
# print(len(label_list))

test111 = "咨询价格".split("、")
test222 = "咨询地址、咨询价格、咨询项目介绍".split("、")
print(test111, test222)
test111.sort()
test222.sort()
print(test111, test222)

nums = [0.2342342, 0.321342, 0.98329423, 0.83732, 0.6737423, 1.1599987601584871e-06]
print(max(nums))
print(nums.index(max(nums)))
test_1 = 0.1
test = 1.1599987601584871e-06
print(float(test))

if float(test_1) >= float(test):
    re_score = 0
else:
    re_score = 1
print(re_score)


