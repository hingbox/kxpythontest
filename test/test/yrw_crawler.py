 #_*_ coding:utf-8 _*_ //为了告诉python解释器，按照utf-8编码读取源代码，否则，你在源代码中写的中文输出可能会由乱码
#这个是抓取有融网信息 有融网url https://www.yrw.com/products/list-all-all-performance-1-createTimeDesc-1.html
#爬取对象：有融网理财项目列表页【履约中】状态下的前10页数据  地址：https://www.yrw.com/products/list-all-all-performance-1-createTimeDesc-1.html
from bs4 import BeautifulSoup
import requests
import sys
import re
import json
reload(sys)
sys.setdefaultencoding( "utf-8" )
#观察地址的变化规律，可以看到，每切换一页时，后面“createTimeDesc-1.html”中的数字1会随着页面的变动而变动，此时我们将地址存放进列表中，后面用format()和for循环来实现多个地址的存储。
#urls = ['https://www.yrw.com/products/list-direct-all-performance-1-createTimeDesc-{}.html'.format(str(i)) for i in range(1,11)]
#print(urls)


#get请求 不带参数demo
def get_titles(urls,data=None):
    req_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'gzip',
        'Connection': 'close',
        'Referer': None  # 注意如果依然不能抓取的话，这里可以设置抓取网站的host
    }
    r = requests.get(urls)# 最基本的GET请求
    r.encoding
    #print (r.status_code)# 获取返回状态
    #r = requests.get(url='http://dict.baidu.com/s', params={'wd': 'python'})  # 带参数的GET请求
    #print(r.url)
    #print(r.text)  # 打印解码后的返回数据
    soup = BeautifulSoup(r.text,'lxml')
    titles = soup.select(' h3 > a > em ')
    soup
    for title in titles:
        data = {
            'title': title.get_text()
        }
       # print(data)
        print (title.get_text())

#模拟登录
# s = requests.session()
# data = {'user':'用户名','passdw':'密码'}
# #post 换成登录的地址，
# res=s.post('http://www.xxx.net/index.php?action=login',data);
# #换成抓取的地址
# s.get('http://www.xxx.net/archives/155/');

# requests.get('https://github.com/timeline.json') #GET请求
# requests.post('http://httpbin.org/post') #POST请求
# requests.put('http://httpbin.org/put') #PUT请求
# requests.delete('http://httpbin.org/delete') #DELETE请求
# requests.head('http://httpbin.org/get') #HEAD请求
# requests.options('http://httpbin.org/get') #OPTIONS请求


#POST发送JSON数据
    # r = requests.post('https://api.github.com/some/endpoint', data=json.dumps({'some': 'data'}))
    # print(r.json())

def get_title():
    url = 'http://www.woshipm.com'
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text, 'lxml')
    titles = soup.select('h2.stream-list-title > a')
    pageviews = soup.select('footer > span.post-views')
    imgs = soup.select('div.stream-list-image > a > img')
    for title,img in zip(titles,imgs):
        title = title.get_text()
        img = img.get('src')
        data = {
            'title':title,
            'img':img
        }
        print(data)
    for title,pageview,img in zip(titles,pageviews,imgs):
        # data = {
        #     'title':title.get_text(),
        #     'pageview':pageview.get_text(),
        #     'img':img.get('src')
        # }
        # print(data)
        title = title.get_text()
        pageview = pageview.get_text()
        img = img.get('src')
        #print(title,pageview,img)

#属性匹配
def attrs_p():
    '''
        <tr class>
            <td class="count"></td>
            <td>111</td>
            <td>222</td>
        </tr>
        <tr class="odd"></tr>
        '''
    soup = BeautifulSoup()
    soup.read()
    # 匹配带有class属性的tr标签
    taglist = soup.find_all('tr', attrs={'class': re.compile("(odd)|()")})
    for trtag in taglist:
        tdlist = trtag.find_all('td')  #在每个tr标签下,查找所有的td标签
        print tdlist[1].string   #这里提取IP值
        print tdlist[2].string   #这里提取端口值

def demo():


 if __name__ == '__main__':
    #get请求不带参数测试
    # urls = ['https://www.yrw.com/products/list-direct-all-performance-1-createTimeDesc-{}.html'.format(str(i)) for i in range(1, 2)]
    # for titles in urls:
    #     get_titles(titles)
    get_title()





