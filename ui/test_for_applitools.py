# -*- coding: UTF-8 -*-
'''
Created on 2020/6/15 9:26
@File  : test_for_applitools.py
@author: ZL
@Desc  :
'''

from selenium import webdriver
from applitools.selenium import Eyes, Target
from selenium.webdriver.common.by import By


class HelloWorld:
    global driver
    eyes = Eyes()

    # Initialize the eyes SDK and set your private API key.
    eyes.api_key = 'apjAXfjEtWmBcj6GW3zRxbVMFvifZh7OCvfwlUs71E8110'

    try:

        # Open a Chrome browser.
        chrome_driver = "E:/chromedriver/chromedriver"
        driver = webdriver.Chrome(chrome_driver)

        # Start the test and set the browser's viewport size to 800x600.
        eyes.open(driver, "Test", "kst test", {'width': 800, 'height': 600})

        # 访问百度首页
        driver.get('http://tkfk.kuaishang.cn/bs/im.htm?cas=117576___665228&fi=120040')

        # Visual checkpoint #1.

        # eyes.check("Baidu Homepage Test", Target.window())
        eyes.check("kst Homepage Test", Target.window())
        # eyes.check("Baidu Homepage Test", Target.region(By.CSS_SELECTOR.CSS_SELECTOR("ScrollableElement")).fully())
        # End the test.
        results = eyes.close(False)

        print(results)

    finally:

        # Close the browser.
        driver.quit()

        # If the test was aborted before eyes.close was called, ends the test as aborted.
        eyes.abort()
