# coding=utf-8
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# 判断元素是否可见
def is_visible(driver, locator, timeout=10):
    '''
    :param driver:
    :param locator: xpath路径
    :param timeout:
    :return:bool
    '''
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, locator)))  # visibility...参数为元组形式
        return True
    except TimeoutException:
        return False


# 判断元素是否存在
def isElementExist(method, element):
    '''
    :param method: 寻找原始使用方法，不要实例化
    :param element: 对应方法所对应的元素
    :return:bool
    '''
    flag = True
    try:
        method(element)
    except:
        flag = False
    finally:
        return flag