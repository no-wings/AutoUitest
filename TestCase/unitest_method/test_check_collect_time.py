# coding=utf-8
import unittest
import os
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from common.pub.browser_engine import BrowserEngine
from common.bus.selectconfig import High_way_display, Timedate_select
from common.bus.login import Login

from common.pub.dbconfig import DbManipulate

from common.bus.screen_shot import Screenshot
import run1
import datetime
from common.pub import readconfig
from common.pub.excelconfig import export
from common.pub.Log import MyLog as Log
from common.pub import selenium_rewrite

localReadConfig = readconfig.ReadConfig()

result_path = run1.log_path


class CheckCollectTime(unittest.TestCase):

    def setUp(self):
        browser = BrowserEngine()
        self.driver = browser.open_browser()
        # self.driver = webdriver.Chrome()
        Login(self.driver).login_chrome()
        highway = High_way_display(self.driver)
        highway.select('拥堵')  # 勾选
        highway.select('施工')  # 勾选
        highway.select('占道行驶')  # 勾选
        log = Log.get_log()
        self.logger = log.get_logger()

    def test_case1(self):
        self.assertTrue(selenium_rewrite.is_visible(self.driver, "//div[@class='title']"))

    # @unittest.skip('n')
    def test_case2(self):
        driver = self.driver
        tm_selector = Timedate_select(driver)
        for i in range(1, 8):
            tm_selector.select_time(i)  # 选择主界面下方的第n天
            time.sleep(2)
            clist = driver.find_elements_by_id('highway_list')[0].find_elements_by_tag_name('tr')
            n = len(clist)
            collect_time = ""
            if n == 0:
                # print(date+"无采集数据")
                pass
            else:
                for index in range(1, n + 1):
                    cl = driver.find_element_by_xpath('//*[@id="highway_list"]/tr[' + str(index) + ']')
                    time_suffix = cl.find_elements_by_tag_name('td')[2].text
                    driver.execute_script("arguments[0].scrollIntoView();", cl)
                    cl.click()
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="highway_list"]/tr'))
                    )
                    time.sleep(2)
                    if driver.find_element_by_xpath(
                            '//*[@id="small-info-dlg"]/div[1]/div[3]/div[1]').text == collect_time:
                        cl.click()
                        time.sleep(5)
                    collect_time = driver.find_element_by_xpath('//*[@id="small-info-dlg"]/div[1]/div[3]/div[1]').text
                    print(time_suffix, collect_time)
                    self.assertTrue(time_suffix in collect_time, msg='失败原因：采集时间与列表事件时间不一致')
                    time.sleep(1)

    # 数据流转对比测试用例
    def test_case_2(self):
        driver = self.driver
        tm_selector = Timedate_select(driver)
        now_time = datetime.datetime.now()
        db = DbManipulate()
        pol_code = localReadConfig.get_db('polygon_code')
        for i in range(7):
            tm_selector.select_time(i + 1)
            time.sleep(4)
            nowadays = str(driver.find_element_by_xpath("//ul[@id='dates_x']/li[" + str(i + 1) + ']').text)
            midpath = os.path.join(result_path, 'excel')
            if not os.path.exists(midpath):
                os.mkdir(midpath)
            innerpath = os.path.join(midpath, str(nowadays))
            os.mkdir(innerpath)
            day1 = (now_time + datetime.timedelta(days=-i)).strftime("%Y-%m-%d")
            day1 = '\'' + day1 + ' 00:00:00' + '\''
            day2 = (now_time + datetime.timedelta(days=-(i - 1))).strftime("%Y-%m-%d")
            day2 = '\'' + day2 + ' 00:00:00' + '\''
            results = db.query(
                "select b.id,FROM_UNIXTIME(floor(SUBSTRING(pic_file,-17,13)/1000)) a,t.polygon_code,check_block,check_traffic,check_work,check_blur,check_barrier,check_lowspeed,check_barrier,check_walk from pic_task t inner join pic_boxes_task b on b.pic_id = t.id where t.polygon_code=%s and check_rescue=-1 and check_repeat=1 and b.id not in (select id from(select b.id,FROM_UNIXTIME(round(SUBSTRING(pic_file,-17,13)/1000)) a,audit_time,t.polygon_code\
                from pic_task t inner join pic_boxes_task b on b.pic_id = t.id where t.polygon_code=%s and check_block=-1 and check_traffic=-1 and check_work=-1 and check_blur=-1 and check_barrier and check_lowspeed=-1 and check_barrier=-1 and check_walk=-1 and audit_result=-1\
                having a>%s and a<%s) a) having a>%s and a<%s" % (pol_code, pol_code, day1, day2, day1, day2))
            fields = db.get_fields()
            caiji_list = Screenshot(driver).get_caiji_list()
            self.excp_export(fields, results, caiji_list, innerpath, nowadays)

    # 差值比较并导出excel
    def excp_export(self, fields, results, caiji_list, outputdir, nowadays):
        results = list(results)
        # day=caiji_list[0].split(' ')[0].encode('utf-8')
        # outputdir = os.path.join(Prodir,'outputs')
        if not os.path.exists(outputdir):
            os.mkdir(outputdir)
        # day_output=os.path.join(outputdir,str(datetime.now().strftime('%Y%m%d%H%M%S')))
        # if not os.path.exists(day_output):
        #     os.mkdir(day_output)
        outputpath1 = os.path.join(outputdir, nowadays + 'db.xls')
        outputpath2 = os.path.join(outputdir, nowadays + 'plat.xls')
        pic = []
        res = []
        for i in range(len(results)):
            time = str(results[i][1])
            if caiji_list:
                if time in caiji_list:
                    pic.append(results[i])
                    # results.remove(results[i])
                    caiji_list.remove(time)
                else:
                    res.append(results[i])
            else:
                res.append(results[i])
        try:
            self.assertIsNotNone(caiji_list, '展示平台数据异常')
        finally:
            export(fields, res, 'db', outputpath1)
            export(fields, pic, 'plat', outputpath2)

    def tearDown(self):
        self.driver.quit()
        self.logger.info("Now, Close and quit the browser.")