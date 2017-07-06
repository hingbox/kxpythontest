#!/usr/bin/python
# _*_ coding:utf-8 _*_ //为了告诉python解释器，按照utf-8编码读取源代码，否则，你在源代码中写的中文输出可能会由乱码
import struct
import sys
import urllib
import os
import requests
reload(sys)
sys.setdefaultencoding('utf-8')
#方法一 使用 urllib 模块提供的 urlretrieve() 函数。urlretrieve() 方法直接将远程数据下载到本地。
#参数 finename 指定了保存本地路径（如果参数未指定，urllib会生成一个临时文件保存数据。）
#参数 reporthook 是一个回调函数，当连接上服务器、以及相应的数据块传输完毕时会触发该回调，我们可以利用这个回调函数来显示当前的下载进度。
#参数 data 指 post 到服务器的数据，该方法返回一个包含两个元素的(filename, headers)元组，filename 表示保存到本地的路径，header 表示服务器的响应头。
# def Schedule(a,b,c):
#     '''''
#     a:已经下载的数据块
#     b:数据块的大小
#     c:远程文件的大小
#    '''
#     per = 100.0 * a * b / c
#     if per > 100 :
#         per = 100
#     print '%.2f%%' % per
# url = 'http://download.pinyin.sogou.com/dict/download_cell.php?id=15202&name=数学词汇大全【官方推荐】&f=detail'
# #local = url.split('/')[-1]
# local = os.path.join('E:\\ciku\\download','数学词典.scel')
# urllib.urlretrieve(url,local,Schedule)

#方法二  使用urllib的urlopen()函数
# import urllib2
# print "downloading with urllib2"
# url = 'http://download.pinyin.sogou.com/dict/download_cell.php?id=15202&name=数学词汇大全【官方推荐】&f=detail'
# f = urllib2.urlopen(url)
# data = f.read()
# with open(unicode("E:\\ciku\\download\\数学词汇大全【官方推荐】.scel" , "utf8"), "wb") as code:
#     code.write(data)


#方法三 使用requests模块
# import requests
# print 'downloading with requests'
# url = 'http://download.pinyin.sogou.com/dict/download_cell.php?id=11313&name=%E6%95%B0%E5%AD%A6%E4%B8%93%E4%B8%9A%E8%AF%8D%E5%BA%93'
# r = requests.get(url)
# with open(unicode('E:\\ciku\\download\\数学专业词库.scel','utf8'),'wb')as code:
#     code.write(r.content)

from bs4 import BeautifulSoup
import urllib2
import re
def runPage():
    page_url = "http://pinyin.sogou.com/dict/cate/index/1"  # 自然科学
    req_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'gzip',
        'Connection': 'close',
        'Referer': None  # 注意如果依然不能抓取的话，这里可以设置抓取网站的host
    }
    try:
        web_content = urllib2.urlopen(page_url,timeout=5)
        data = web_content.read()
        soup = BeautifulSoup(data, "html.parser")


        #div_list = soup.find_all("a")
        div_list = soup.find_all(re.compile('^a'))#正则表达式
        # for tag in soup.find_all(True):
        #     print(tag.name)
        # for tags in div_list:
        #     print('----'+tags.attrs)
            #keywork参数
        #使用id进行过滤
        keyword = soup.find_all(id='dict_nav_list')
        print ('keyword---',keyword)
        #使用属性过滤
        href = soup.find_all(href=re.compile('http://shouji.sogou.com/'))
        for hrefs in href:
            print ('href----', hrefs)
        #使用class过滤
        classs = soup.find_all("div",class_="topnav_name",limit=1)
        print ('class----',classs)

        #text参数
        # text = soup.find_all(text="输入法手机版")
        # print('text---'+text)

        #limit
        limit = soup.find_all("a",limit=2)
        print('limit----',limit)

        titleDiv = soup.find_all("div",re.compile("^a"),class_="detail_title",limit=2,recursive=True)#得到标题 下载文件的时候用在文件名称
        downloadDiv = soup.find_all("div", re.compile("^a"), class_="dict_dl_btn",limit=2, recursive=True)#这个地方得到立即下载的div
        for divs in titleDiv:
            a = divs.find_all("a")
            for aa in a:
               href = aa.get("href")
               for temps in downloadDiv:
                   ac = temps.find_all("a")
                   for acc in ac:
                       hrefs = acc.get("href")
                       print 'soup---', href,'string--',aa.string,'hrefs--', hrefs, 'stringcc-', acc.string
                       # 开始下载文件
                       print 'downloading with requests'
                       url = hrefs
                       r = requests.get(url)
                       with open('E:\\ciku\\download\\' + aa.string + '.scel', 'wb')as code:
                           code.write(r.content)

    except Exception,e:
        print e

#得到自然科学信息
def runOtherPage(url,i):
    page_url = url+format(i)  # 自然科学
    req_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'gzip',
        'Connection': 'close',
        'Referer': None  # 注意如果依然不能抓取的话，这里可以设置抓取网站的host
    }
    try:
        web_content = urllib2.urlopen(page_url,timeout=5)
        data = web_content.read()
        soup = BeautifulSoup(data, "html.parser")
        div = soup.find_all("",re.compile("^a"),class_="dict_detail_block")
        for divs in div:
            title = divs.findAll("",class_="detail_title")
            for titles in title:
                print 'title',titles.string
            href = divs.findAll("", class_="dict_dl_btn")
            for hrefs in href:
                print 'href', hrefs.find("a").get("href")
            url = hrefs.find("a").get("href")
            r = requests.get(url)
            with open('E:\\ciku\\download\\' + titles.string + '.scel', 'wb')as code:
                code.write(r.content)
    except Exception,e:
        print e
if __name__ == '__main__':
    stdout = sys.stdout
    stdin = sys.stdin
    stderr = sys.stderr
    reload(sys)
    sys.stdout = stdout
    sys.stdin = stdin
    sys.stderr = stderr
    sys.setdefaultencoding('utf8')
    #runPage()

    # 城市信息
    for i in range(1, 10):
       runOtherPage("http://pinyin.sogou.com/dict/cate/index/167/default/",i)
    #自然科学
    # for i in range(1, 32):
    #   runOtherPage("http://pinyin.sogou.com/dict/cate/index/1/default/",i)
    #社会科学
    # for i in range(1, 51):
    #   runOtherPage("http://pinyin.sogou.com/dict/cate/index/76/default/",i)
    #工程应用
    # for i in range(1, 83):
    #   runOtherPage("http://pinyin.sogou.com/dict/cate/index/96/default/", i)
    #农林应用
    # for i in range(1, 10):
    #   runOtherPage("http://pinyin.sogou.com/dict/cate/index/127/default/", i)
    #医学医药
    # for i in range(1, 32):
    #   runOtherPage("http://pinyin.sogou.com/dict/cate/index/132/default/", i)
    #电子游戏
    # for i in range(1, 114):
    #     runOtherPage("http://pinyin.sogou.com/dict/cate/index/436/default/", i)
    #艺术设计
    # for i in range(1, 20):
    #     runOtherPage("http://pinyin.sogou.com/dict/cate/index/154/default/", i)
    #生活百科
    # for i in range(1, 85):
    #     runOtherPage("http://pinyin.sogou.com/dict/cate/index/389/default/", i)
    # 运动休闲
    # for i in range(1, 18):
    #     runOtherPage("http://pinyin.sogou.com/dict/cate/index/367/default/", i)
    # 人文科学
    # for i in range(1, 108):
    #     runOtherPage("http://pinyin.sogou.com/dict/cate/index/367/default/", i)
    # 娱乐休闲
    # for i in range(1, 162):
    #     runOtherPage("http://pinyin.sogou.com/dict/cate/index/403/default/", i)
