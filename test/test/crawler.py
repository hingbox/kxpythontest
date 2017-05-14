# _*_ coding:utf-8 _*_ //为了告诉python解释器，按照utf-8编码读取源代码，否则，你在源代码中写的中文输出可能会由乱码
import urllib2
from bs4 import BeautifulSoup

def runPage(pageIndex):
    pageUrl = "http://search.10jqka.com.cn/stockpick/category"
    req_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'gzip',
        'Connection': 'close',
        'Referer': None  # 注意如果依然不能抓取的话，这里可以设置抓取网站的host
        }
    try:
        webContent = urllib2.urlopen(pageUrl, timeout=5)
        data = webContent.read()
        #print "sdfasdfasdfs"+data
        # 利用BeautifulSoup读取视频列表网页数据
        soup = BeautifulSoup(data,"html.parser")
        tag_list = soup.find_all("dd","query_box")

        for item in tag_list :
            temphref = item.find_all('a')
            topic_url = temphref[0].get('href')
            topic_title = temphref[0].get('title')
            getDetail(topic_url,topic_title)
            #print topic_url,topic_title
    except Exception,e:
        print e

def getDetail(topic_url,topic_title):
    index1 = topic_url.find("&qs=")
    if index1 !=-1:
        index2 = topic_url.find("&",index1+4)
        if index2 !=-1:
            categoryname = topic_url[index1+4:index2]

    index1 = topic_url.find("&tid=")
    if index1 != -1:
        index2 = topic_url.find("&", index1 + 5)
        if index2 != -1:
            tid = topic_url[index1 + 5:index2]

    index1 = topic_url.find("&w=")
    if index1 != -1:
        words = topic_url[index1 + 3:]


    print categoryname,tid,words


if __name__ == '__main__':
    runPage(0)

