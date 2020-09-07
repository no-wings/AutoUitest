# coding=utf-8
import time
from selenium.common.exceptions import NoSuchElementException
from common.pub.selenium_rewrite import is_visible


class LocationSelect():
    def __init__(self, driver, province, city):
        self.driver = driver
        self.city = standardinput(city)
        self.province= standardinput(province)
        self.baseelem = "//*[@id='IIInsomnia_province_wrap']/li[@data-name=%s]" % (self.province)

    def act(self):
        self.act_kuang()
        self.select_province()
        self.select_city()

    def act_kuang(self):
        element = '完成'
        try:
            self.driver.find_elements_by_link_text(element)[0].click()
        except Exception:
            print('完成框已经消失/n输入框已唤醒')
        time.sleep(2)
        select_city = self.driver.find_element_by_class_name('location-c')
        select_city.click()

    def select_province(self):
        try:
            pro = self.get_province()
            pro.click()
        except NoSuchElementException:
            print("请重新输入省份（规范）：/'**省/'")

    def select_city(self):
        try:
            cit = self.get_city()
            cit.click()
            time.sleep(2)
        except NoSuchElementException:
            print("请重新输入市名（规范）：/'**市/'")

    def get_province(self):
        prov = self.driver.find_element_by_xpath(self.baseelem)
        return prov

    def get_city(self):
        elem = self.baseelem + "/ul/li[@title=%s]" % (self.city)
        cit = self.driver.find_element_by_xpath(elem)
        return cit


# #定位到对应城市（采用鼠标点击方式来唤出）


class MapDisplay():
    def __init__(self, driver):
        self.driver = driver
        self.dic = {'道路实景': ["//div[@id='layerbox-street']/input", "//div[@id='layerbox-street']/div[3]"],
                    '高速': ["//div[@id='layerbox-high-road']/input", "//div[@id='layerbox-high-road']/div[3]"],
                    '路径规划': ["//div[@id='layerbox-route']/input", "//div[@id='layerbox-route']/div[3]"],
                    '街面事件': ["//div[@id='layerbox-street-event']/input", "//div[@id='layerbox-street-event']/div[3]"],
                    '城管事件': ["//div[@id='layerbox-urban-event']/input", "//div[@id='layerbox-urban-event']/div[3]"],
                    '交管事件': ["//div[@id='layerbox-traffic-event']/input", "//div[@id='layerbox-traffic-event']/div[3]"],
                    '覆盖频次': ["//div[@id='layerbox-override-count']/input",
                             "//div[@id='layerbox-override-count']/div[3]"],
                    '车辆位置': ["//div[@id='layerbox-car-locate']/input", "//div[@id='layerbox-car-locate']/div[3]"],
                    '道路标牌': ["//div[@id='layerbox-road-signs']/input", "//div[@id='layerbox-road-signs']/div[3]"],
                    'POI': ["//div[@id='layerbox-road-poi']/input", "//div[@id='layerbox-road-poi']/div[3]"],
                    '新建道路': ["//div[@id='layerbox-new-roads']/input", "//div[@id='layerbox-new-roads']/div[3]"],
                    '路况': ["//div[@id='layerbox-road-condition']/input", "//div[@id='layerbox-road-condition']/div[3]"],
                    '交通事件': ["//div[@id='layerbox-traffic-incident']/input",
                             "//div[@id='layerbox-traffic-incident']/div[3]"],
                    }

    def select(self, name):
        xpath = self.dic[name]
        try:
            element_judge = self.driver.find_element_by_xpath(xpath[0])
            if not element_judge.is_enabled():
                raise SelectWarning(name)
            elif not element_judge.is_selected():
                # WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath[1])))
                if is_visible(self.driver, xpath[1]):
                    self.driver.find_element_by_xpath(xpath[1]).click()  # 这里有点奇怪，元素已存在还需要等待
        except KeyError:
            print('选项不存在')

    def cancel(self, name):
        try:
            xpath = self.dic[name]
            element_judge = self.driver.find_element_by_xpath(xpath[0])
            element = self.driver.find_element_by_xpath(xpath[1])
            if element_judge.is_selected():
                element.click()
        except KeyError:
            print('%s选项不存在' % name)


class SelectWarning(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        print('%s 不可选' % (self.name))


def isElementExist(method, element):
    flag = True
    try:
        method(element)
    except:
        flag = False
    finally:
        return flag


def standardinput(s):
    if not s.startswith("'"):
        s = "'" + s + "'"
    return s


class High_way_display(MapDisplay):
    def __init__(self, driver):
        # super(High_way_display, self).__init__(driver
        self.driver = driver
        locator = "//div[@class='introjs-tooltipbuttons']/a"
        if is_visible(self.driver, locator):
            self.driver.find_element_by_xpath(locator).click()
        time.sleep(2)
        self.dic = {'事故': ["//div[@class='layui-form']/div[1]/input", "//div[@class='layui-form']/div[1]/div[1]"],
                    '团雾': ["//div[@class='layui-form']/div[2]/input", "//div[@class='layui-form']/div[2]/div[1]"],
                    '行人': ["//div[@class='layui-form']/div[3]/input", "//div[@class='layui-form']/div[3]/div[1]"],
                    '低速': ["//div[@class='layui-form']/div[4]/input", "//div[@class='layui-form']/div[4]/div[1]"],
                    '抛洒': ["//div[@class='layui-form']/div[5]/input", "//div[@class='layui-form']/div[5]/div[1]"],
                    '施工': ["//div[@class='layui-form']/div[6]/input", "//div[@class='layui-form']/div[6]/div[1]"],
                    '占道违停': ["//div[@class='layui-form']/div[7]/input", "//div[@class='layui-form']/div[7]/div[1]"],
                    '占道行驶': ["//div[@class='layui-form']/div[8]/input", "//div[@class='layui-form']/div[8]/div[1]"],
                    '拥堵': ["//div[@class='layui-form']/div[9]/input", "//div[@class='layui-form']/div[9]/div[1]/i"],
                    }


class Timedate_select:
    '''
        :param num:'代表是第几天'
        :return: 返回对应天的元素
    '''

    def __init__(self, driver):
        self.driver = driver

    def select_time(self, num):
        xpath = self.__get_element(num)
        if is_visible(self.driver, xpath):
            self.driver.find_element_by_xpath(xpath).click()
        else:
            raise ValueError
        return self.driver.find_element_by_xpath(xpath).text

    def __get_element(self, num):
        num = str(num)
        xpath = "//ul[@id='dates_x']/li[%s]" % num
        return xpath