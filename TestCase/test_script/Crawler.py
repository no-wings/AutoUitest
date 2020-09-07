# coding=utf-8
from common.pub.browser_engine import BrowserEngine
from common.bus.login import Login
from common.bus.selectconfig import High_way_display, Timedate_select
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from common.bus.screen_shot import Screenshot
from common.pub.excelconfig import export
from common.pub.readconfig import proDir
import os


class test():
    def __init__(self):
        browser = BrowserEngine()
        self.driver = browser.open_browser()
        # self.driver = webdriver.Chrome()

    def run(self):
        driver = self.driver
        Login(driver).login_chrome()
        highway = High_way_display(driver)
        highway.select('拥堵')  # 勾选
        highway.select('施工')  # 勾选
        highway.select('占道行驶')  # 勾选
        # tm_selector = Timedate_select(driver)
        getattr = Screenshot(driver)
        date = []
        # for i in range(1,8):
        #     tm_selector.select_time(i)  # 选择主界面下方的第n天
        #     time.sleep(2)
        clist = driver.find_elements_by_id('highway_list')[0].find_elements_by_tag_name('tr')
        n = len(clist)
        collect_time = ""
        if n == 0:
            # print(date+"无采集数据")
            pass
        try:
            for index in range(1, n + 1):
                cl = driver.find_element_by_xpath('//*[@id="highway_list"]/tr[' + str(index) + ']')
                time_suffix = cl.find_elements_by_tag_name('td')[2].text
                driver.execute_script("arguments[0].scrollIntoView();", cl)
                cl.click()
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="highway_list"]/tr'))
                )
                time.sleep(2)
                if driver.find_element_by_xpath('//*[@id="small-info-dlg"]/div[1]/div[3]/div[1]').text == collect_time:
                    cl.click()
                    time.sleep(5)
                title = getattr.get_title()
                location = getattr.get_location()
                caiji = getattr.get_caiji()
                recogintion = getattr.get_recognition()
                tmp = (title, location, caiji, recogintion)
                date.append(tmp)
        except Exception as e:
            print('str(e)')
        finally:
            fields = ['title', 'location', 'caiji', 'recogintion']
            output_path = os.path.join(proDir, 'test.xls')
            export(fields, date, 'db', output_path)


if __name__ == '__main__':
    A = test()
    A.run()