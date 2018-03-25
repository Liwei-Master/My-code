from bs4 import BeautifulSoup,element
# http://www.cnblogs.com/Albert-Lee/p/6232745.html
html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title">The Dormouse's story</p>
<b><!--Hey, buddy. Want to buy a used parser?--></b>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, 'lxml')
find = soup.find_all('a')
comment = soup.b.string

title_tag = soup.body #查找第一个p标签
#对标签的直接子节点进行循环
for child in title_tag.children:
    print(child)


print("find's return type is ", type(find))  #输出返回值类型
print("find's content is", find)  #输出find获取的值

print(type(comment))
if type(comment) == element.Comment:
    print('该字符是注释')
else:
    print('该字符不是注释')

for parent in soup.a.next_siblings:
    if parent is None:
        print(parent)
    else:
        print(parent.name)

import re
sis = soup.find(string=re.compile("sisters"))
print(sis)

import requests
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:59.0) Gecko/20100101 Firefox/59.0'}  #给请求指定一个请求头来模拟chrome浏览器
web_url = 'http://www.sohu.com/a/225997512_267106?pvid=ab2a3f3fa09b29b9'
r = requests.get(web_url, headers=headers) #像目标url地址发送get请求，返回一个response对象
text = BeautifulSoup(r.text, 'lxml')

all_image = text.find_all('img')  #获取网页中的class为cV68d的所有a标签
print(type(all_image))
for image in all_image[:2]:
    print(image['src']) #循环获取a标签中的style