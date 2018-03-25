from selenium import webdriver  #导入Selenium的webdriver
from selenium.webdriver.common.keys import Keys  #导入Keys
import os


chromedriver = "/Users/LiweiHE/anaconda3/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)  #指定使用的浏览器，初始化webdriver
print(type(driver))
driver.get("http://www.python.org")  #请求网页地址
assert "Python" in driver.title  #看看Python关键字是否在网页title中，如果在则继续，如果不在，程序跳出。
elem = driver.find_element_by_name("q")  #找到name为q的元素，这里是个搜索框
elem.clear()  #清空搜索框中的内容
elem.send_keys("pycon")  #在搜索框中输入pycon
elem.send_keys(Keys.RETURN)  #相当于回车键，提交
assert "No results found." not in driver.page_source  #如果当前页面文本中有“No results found.”则程序跳出
driver.close()  #关闭webdriver

