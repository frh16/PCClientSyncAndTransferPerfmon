from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time


chrome_opt = Options()      # 创建参数设置对象.
chrome_opt.debugger_address = '127.0.0.1:9222'
# chrome_opt.add_argument('--headless')   # 无界面化.
# chrome_opt.add_argument('--disable-gpu')    # 配合上面的无界面化.
# chrome_opt.add_argument('--window-size=1366,768')   # 设置窗口大小, 窗口大小会有影响.

# 创建Chrome对象并传入设置信息.
driver = webdriver.Chrome(options=chrome_opt)
# driver.get(r'https://test39.tj.com')
# time.sleep(3)
# abc = driver.find_element_by_id('tab_m_personal')
# print(abc)

# foldermore = driver.find_elements_by_class_name("foldermore")
# print(target)

# target = driver.find_element_by_xpath(r'/html/body/div[5]/div[3]/div/div/div[2]/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div/p[2]/span[2]')

# print(target.text)

# target = driver.find_elements_by_class_name("icon i-arrow2")
# /html/body/div[5]/div[3]/div/div/div[2]/div[1]/div/div/div/div[2]/div/div[2]/div[1]/p[6]/a/i

try:
    time.sleep(0.5)

    # aaaa = driver.find_element(By.XPATH, "//a[text()='1k']/../../../preceding-sibling::span").click()

    arrow = driver.find_element_by_xpath('//*[@id="file-attr-wraper"]/div/div[2]/div/div[2]/div[1]/p[6]/a/i')
    arrow.click()

    time.sleep(0.5)
    num = driver.find_element_by_xpath('//*[@id="file-attr-wraper"]/div/div[2]/div/div[2]/div[1]/div/p[2]/span[2]')
    # num.text
    arrow.click()

    print(num.text)
    # time.sleep(2)
    driver.quit()  # 使用完, 记得关闭浏览器, 不然chromedriver.exe进程为一直在内存中.
except Exception as e:
    print(e)
    driver.quit()  # 使用完, 记得关闭浏览器, 不然chromedriver.exe进程为一直在内存中.

# html = driver.page_source
# print(html)
# 操作这个对象.
# driver.get('https://test39.tj.com')     # get方式访问百度.
# time.sleep(2)
# print(driver.page_source)       # 打印加载的page code, 证明(prove) program is right.
