# BeautifulSoup模块来从HTML文本中提取我们想要的数据
# https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/#keyword
# r.text is the content of the response in unicode, and r.content is the content of the response in bytes.
# http://selenium-python.readthedocs.io/index.html

# Purpose: code here is used to pick up urls and pictures which related to topics I'm interested in
# the target website is an Adult website based in Taiwan: https://wuso.me/forum-jsav-1.html

import requests
from bs4 import BeautifulSoup, re
from selenium import webdriver  #导入Selenium的webdriver
from selenium.webdriver.common.keys import Keys  #导入Keys
import os
import time


class BeautifulPicture():
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:59.0) Gecko/20100101 Firefox/59.0'}  #给请求指定一个请求头来模拟chrome浏览器
        self.web_url = 'https://wuso.me/forum-jsav-1.html' # target website
        self.folder_path = '/Users/LiweiHE/acquisition'  # where to store
        self.driver = None


    def requests(self,url):
        r = requests.get(url)
        return r


    def create_folder(self,path):
        path = path.strip()
        is_valid = os.path.exists(path)
        if not is_valid:
            print('Create a file called ', path)
            os.makedirs(path)
        else:
            print('This folder is already existed.')

    def next_page(self):
        start = self.web_url[:-6]
        page = int(self.web_url[-6]) + 1
        end = self.web_url[-5:]

        self.web_url = start + str(page) + end


    def save(self, url, name):  ##保存url
        print('start to store url')
        # https://docs.python.org/3/library/functions.html?highlight=open#open
        f = open(name, 'w')
        f.write(url)
        print(name, 'url received！')
        f.close()

    def save_img(self, url, name):  ##保存图片
        print('Start to pull the pic...')
        img = self.requests(url)
        time.sleep(5)
        file_name = name + '.jpg'
        # https://docs.python.org/3/library/functions.html?highlight=open#open

        f = open(file_name, 'ab')
        f.write(img.content)
        print(file_name, 'pulled！')
        f.close()

    def get_url(self):
        print('start the GET ')
        self.driver.get(self.web_url)  # 请求网页地址
        print('Start to find all <a>')
        all_a = BeautifulSoup(self.driver.page_source, 'lxml').find_all('a', class_='z', title=re.compile("巨乳"))

        # print('开始创建文件夹')
        # self.create_folder(self.folder_path)
        # print('开始切换文件夹')
        # os.chdir(self.folder_path)  # 切换路径至上面创建的文件夹
        print("The number of <a> is：", len(all_a))  # 这里添加一个查询图片标签的数量，来检查我们下拉操作是否有误

        old_urls = self.get_files(self.folder_path)

        for url in all_a:
            name = url['title']

            if name in old_urls:
                print("this url is already existing")
                continue
            else:
                self.save(url['href'], name)


    def get_pic_request(self):
        print('Start the GET')
        r = self.requests(self.web_url)
        print('Start to find all the <img>')
        text = BeautifulSoup(r.text, 'lxml')
        all_images = text.find_all('img', alt=re.compile("大胸"))  # 获取网页中的alt_为""的所有img标签
        print('create file')
        self.create_folder(self.folder_path)
        print('change the current file to it')
        os.chdir(self.folder_path)  # 切换路径至上面创建的文件夹
        i = 0
        all_pics = self.get_files(self.folder_path)
        for img in all_images:
            name_start_pos = img.index('photo')
            name_end_pos = img.index('?')
            name = img[name_start_pos:name_end_pos] + '.jpg'

            if name in all_pics:
                print("this pic is already existing")
                continue
            else:
                print(img)
                self.save_img(img['src'], name)
                i +=1

    def scroll_down(self, driver, times):
        for i in range(times):
            print("开始执行第", str(i + 1), "次下拉操作")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  #执行JavaScript实现网页下拉倒底部
            print("第", str(i + 1), "次下拉操作执行完毕")
            print("第", str(i + 1), "次等待网页加载......")
            time.sleep(20)  # 等待20秒（时间可以根据自己的网速而定），页面加载出来再执行下拉操作

    def get_files(self, path):
        pic_names = os.listdir(path)
        return pic_names

    def init_broswer(self):
        print('开始网页get请求')
        chromedriver = "/Users/LiweiHE/anaconda3/chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)  # 指定使用的浏览器，初始化webdriver

    def close(self):
        self.driver.close()  #关闭webdriver

    def get_pic_Selenium(self):
        self.driver.get(self.web_url)  # 请求网页地址
        # if there is iframe in the page
        # driver.switch_to.frame("g_iframe")
        # self.scroll_down(driver=driver, times=1)
        print('开始获取所有a标签')
        # css labels need '_' to identify
        all_a = BeautifulSoup(self.driver.page_source, 'lxml').find_all('a', class_='z', title=re.compile('巨乳'))
        print("a标签的数量是：", len(all_a))  #这里查询标签的数量

        pic_names = self.get_files(self.folder_path)
        i = 1
        for a in all_a:
            img = a.find('img')
            url = a['href']
            img_url = 'https://wuso.me/' + img['src']
            print('a标签的src内容是：', img_url)
            #first_pos = img_str.index('"') + 1  # 获取第一个双引号的位置，然后加1就是url的起始位置
            #second_pos = img_str.index('"', first_pos)  # 获取第二个双引号的位置
            #img_url = img_str[first_pos: second_pos]  # 使用Python的切片功能截取双引号之间的内容

            # 截取url中参数前面、网址后面的字符串为图片名
            # name_start_pos = img_url.index('photo')
            # name_end_pos = img_url.index('?')
            # img_name = img_url[name_start_pos: name_end_pos]
            img_name = str(i) + "."+ a['title']
            i +=1
            img_name = img_name.replace('/', '')  # 把图片名字中的斜杠都去掉

            if img_name not in pic_names:
                self.save_img(img_url, img_name)  # 调用save_img方法来保存图片
                self.save(url, img_name)
            else:
                print("该图片已经存在：", img_name, "，不再重新下载。")



spider = BeautifulPicture()

spider.init_broswer()

print('Creating file')
spider.create_folder(spider.folder_path)
print('Change the current file to it')
os.chdir(spider.folder_path)  # 切换路径至上面创建的文件夹

# go through 20 pages
for i in range(0, 20):
    print('Moving to ', i + 1, ' page')
    spider.get_pic_Selenium()
    spider.next_page()
    print('page ', i + 1, ' finished')

spider.close()

# Note: code here is used to pick up urls and pictures which related to topics I'm interested in
# the target website is an Adult website based in Taiwan: https://wuso.me/forum-jsav-1.html
