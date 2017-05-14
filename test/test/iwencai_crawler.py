# _*_ coding:utf-8 _*_ //为了告诉python解释器，按照utf-8编码读取源代码，否则，你在源代码中写的中文输出可能会由乱码
from sqlalchemy import *
from sqlalchemy.orm import *
import urllib2
from bs4 import BeautifulSoup
import re
import sys
#MySQL数据库连接字符串
CONSTR='mysql+pymysql://root:root@localhost:3306/alice?charset=utf8'

engine = create_engine(CONSTR, echo=True)
metadata = MetaData(engine)
#创建词条表
entry_table=Table('t_entry',metadata,
                Column('id',Integer,primary_key=True),
                Column('url', String(2048)),
                Column('title',String(2048)),
                Column('status',Integer))
if not entry_table.exists():#判断 表是否存在
    entry_table.create()

#创建词明细表
entry_detail_table=Table('t_entry_detail',metadata,
                Column('id',Integer,primary_key=True),
                Column('entry_id', Integer),
                Column('url', String(2048)),
                Column('title',String(2048)),
                Column('content', String(2048)),
                Column('status',Integer))
if not entry_detail_table.exists():#判断 表是否存在
    entry_detail_table.create()

#保存词条数据
def save_entry(url, title):
    content_table = Table('t_entry',metadata, autoload=True)
    r = content_table.select(and_(content_table.c.title == title)).execute()
    testrow = r.fetchone()
    if testrow == None:
        i = content_table.insert()
        i.execute(
            title=title,
            url=url,
            status=1)
        #print("======================"+content_table.select(and_(content_table.c.title == title)).execute())

    else:
        print "itemexist:%s" % title

        # 保存词条数据

#保存词条明细数据
def save_entry_detail(entry_id, title,url,content):
    content_table = Table('t_entry_detail', metadata, autoload=True)
    r = content_table.select(and_(content_table.c.title == title)).execute()
    testrow = r.fetchone()
    if testrow == None:
        i = content_table.insert()
        i.execute(
            entry_id=entry_id,
            url=url,
            title=title,
            content=content,
            status=1)
    else:
        print "itemexist:%s" % title

def runPage():
    page_url = "http://www.iwencai.com/yike/article-class"
    req_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'gzip',
        'Connection': 'close',
        'Referer': None  # 注意如果依然不能抓取的话，这里可以设置抓取网站的host
    }
    try:
        web_content = urllib2.urlopen(page_url,timeout=5)#得到页面内容
        data = web_content.read();
        #用beautifulsoup 进行解析
        soup = BeautifulSoup(data,"html.parser")
        tag_list = soup.find_all("div","fl")
        entry_id =1
        for item in tag_list:
            temp_href = item.find_all("a")
            detail_page_uri="http://www.iwencai.com/yike/"
            title_one = temp_href[0].string#得到第一个超链接的文字
            detail_url = detail_page_uri+temp_href[0].get('href')#得到子连接
            save_entry(detail_url,title_one)
            getdetailPage(entry_id,title_one,detail_url)
            entry_id +=1
            #print(detail_url)
    except Exception,e:
        print e

def getdetailPage(entry_id,title_one,detail_url):

    req_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'gzip',
        'Connection': 'close',
        'Referer': None  # 注意如果依然不能抓取的话，这里可以设置抓取网站的host
    }
    try:
        detail_content = urllib2.urlopen(detail_url,timeout=5)
        detail_data = detail_content.read()
        soup = BeautifulSoup(detail_data,"html.parser")
        tag_list = soup.find_all("div","term_top")
        for item in tag_list:
            temp_href = item.findAll("a")
            children_url ="http://www.iwencai.com/"+temp_href[0].get("href")

            #save_entry_detail(entry_id, temp_href[0].get("title"), children_url)
            getChildDetail(entry_id,temp_href[0].get("title"),children_url)
            #print(temp_href[0].get("href"),temp_href[0].get("title"))

    except Exception,e:
        print e

def getChildDetail(entry_id,title,children_url):
    try:
        children_content = urllib2.urlopen(children_url,timeout=5)
        children_data = children_content.read()
        soup = BeautifulSoup(children_data,"html.parser")
        tag_list = soup.find("p","term_summ_acl")
        save_entry_detail(entry_id, title, children_url,tag_list.string)
        #print("chilrdern"+tag_list.string)
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
    runPage()