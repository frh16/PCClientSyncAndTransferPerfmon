from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class WebUtils():
    __instance = None

    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = WebUtils()
        return cls.__instance

    def __init__(self):
        self.connect()

    def connect(self):
        chrome_opt = Options()  # 创建参数设置对象.
        chrome_opt.debugger_address = '127.0.0.1:9222'
        driver = webdriver.Chrome(options=chrome_opt)
        self.driver = driver

    def find_element(self, element):
        """
        Judge element positioning way, and returns the element.

        Usage:
        driver.find_element  此为元组(id,kw)，此方法为PageObject模式准备方法
        """
        by = element[0]
        value = element[1]

        if by == "id":
            return self.driver.find_element_by_id(value)
        elif by == "name":
            return self.driver.find_element_by_name(value)
        elif by == "class":
            return self.driver.find_element_by_class_name(value)
        elif by == "text":
            return self.driver.find_element_by_link_text(value)
        elif by == "text_part":
            return self.driver.find_element_by_partial_link_text(value)
        elif by == "xpath":
            return self.driver.find_element_by_xpath(value)
        elif by == "css":
            return self.driver.find_element_by_css_selector(value)
        else:
            raise NameError("Please enter the correct targeting elements,'id','name','class','text','xpath','css'.")

    def click(self, element):
        '''
        功能：点击
        :param element: 元素的定位表达式
        :return:
        '''
        self.wait_element(element)
        self.find_element(element).click()

    def wait_element(self, element, seconds=5):
        """
        等待元素在指定的时间类出现
        :param element:      元素的定位表达式
        :param seconds:      等待的时间
        :return:
        """
        by = element[0]
        value = element[1]

        if by == "id":
            WebDriverWait(self.driver, seconds, 1).until(EC.presence_of_element_located((By.ID, value)))
        elif by == "name":
            WebDriverWait(self.driver, seconds, 1).until(EC.presence_of_element_located((By.NAME, value)))
        elif by == "class":
            WebDriverWait(self.driver, seconds, 1).until(EC.presence_of_element_located((By.CLASS_NAME, value)))
        elif by == "text":
            WebDriverWait(self.driver, seconds, 1).until(EC.presence_of_element_located((By.LINK_TEXT, value)))
        elif by == "xpath":
            WebDriverWait(self.driver, seconds, 1).until(EC.presence_of_element_located((By.XPATH, value)))
        elif by == "css":
            WebDriverWait(self.driver, seconds, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, value)))
        else:
            raise NameError("Please enter the correct targeting elements,'id','name','class','text','xpaht','css'.")

    def move_to_element(self, element):
        '''
        功能：移动到元素
        :param element: 元素的定位表达式
        :return:
        '''
        self.wait_element(element)
        action = ActionChains(self.driver)
        action.move_to_element(self.find_element(element)).perform()

    def quit(self):
        '''
        :return:  退出浏览器
        '''
        self.driver.quit()

    def refresh(self):
        '''
        功能：刷新页面
        :return:
        '''
        self.driver.refresh()

if __name__ == '__main__':
    webutils = WebUtils.getInstance()
    webutils.refresh()
    webutils.click(['xpath', "//a[text()='1k']/../../../preceding-sibling::span"])
    webutils.quit()
