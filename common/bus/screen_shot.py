# coding=utf-8
import time

from selenium import webdriver
# driver = webdriver.Chrome() #打开浏览器
from common.pub import readconfig
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from common.pub.selenium_rewrite import isElementExist
from common.pub.readconfig import ReadConfig

Prodir = readconfig.proDir


class Login():
    def __init__(self, driver):
        localreadconfig = ReadConfig()
        self.name = localreadconfig.get_login('username')
        self.passwd = localreadconfig.get_login('password')
        self.url = localreadconfig.get_login('url')
        self.driver = driver

    def login_chrome(self):
        driver = self.driver
        driver.implicitly_wait(10)
        driver.maximize_window()
        driver.get(self.url)  # 进入url
        user_name = driver.find_element_by_name('username')
        password = driver.find_element_by_name('password')

        login_but = driver.find_element_by_tag_name('button')
        time.sleep(1)
        user_name.send_keys(self.name)  # 输入账号
        password.send_keys(self.passwd)  # 密码

        try:
            move_block = driver.find_element_by_class_name('verify-move-block')  # 验证码为滑动模块
            print("验证为滑动模块")
            while True:
                action = ActionChains(driver)
                action.click_and_hold(move_block)
                action.move_by_offset(300, 0)
                action.release()
                action.perform()
                login_but.click()
                time.sleep(2)
                flag = isElementExist(driver.find_element_by_class_name, 'location')
                if flag:
                    break
        except NoSuchElementException as e:
            code = driver.find_element_by_name('code')  # 验证码
            print("验证为验证码输入")
            code.send_keys("_unlock")  # 输入万能验证码_unlock
            login_but.click()
            for i in range(10):  # 最多等待20s
                time.sleep(2)
                flag = isElementExist(driver.find_element_by_class_name, 'location')
                if flag:
                    break
                if i == 9:
                    print("等待20s还未正常进入主界面")