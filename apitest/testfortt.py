# -*- coding: UTF-8 -*-
'''
Created on 2020/6/2
@File  : testfortt.py
@author: ZL
@Desc  :
'''
def Multiplication(args):
    num = 1
    for item in args:
        num *= item
    print('这是def里的num',num)
    return num

if __name__ == '__main__':
    str1 = input('请输入一窜数字：')
    list1 = str1.split(',')
    list2 = []
    #把字符串转成数字
    for item in list1:
        item2 = float(item)
        list2.append(item2)
    print('这是list2',list2)
    num = 1
    for item in list2:
        num *= item
        print(num)
    print('这是num',num)
    s = Multiplication(list2)
    print('这是s',s)