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

#创建百科表
baike_table =Table("t_baike",metadata,
                   Column("id",Integer,primary_key=True),
                   Column("title",String(50)),
                   Column("url",String(100)),
                   Column("status",Integer))
#创建表
if not baike_table.exists():
    baike_table.create()

#保存百科数据
def save_baike(url,title):
    content_table =Table("t_baike",metadata,autoload=True)
    r = content_table.select(and_(content_table.c.title == title)).execute()
    testrow = r.fetchone()
    if testrow == None:
        i = content_table.insert()
        i.execute(
            url=url,
            title=title,
            status=1
        )
    else:
        print "itemexist:%s" % title

def runPage():

    page_url = "https://baike.baidu.com/"
    req_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'gzip',
        'Connection': 'close',
        'Referer': None  # 注意如果依然不能抓取的话，这里可以设置抓取网站的host
    }
    try:
        web_content = urllib2.urlopen(page_url, timeout=5)
        data = web_content.read()
        soup = BeautifulSoup(data,"html.parser")
        tag_list = soup.find_all("dl")
        for item in tag_list:
            tag_lists = item.find_all("dd")
            for i in tag_lists:
                temp_hrefs = i.findAll("a")
                for ii in temp_hrefs:
                    save_baike(ii.get("href"),ii.string)
                    #print("============="+ii.get("href"),ii.string)
    except Exception,e:
        print e

if __name__ == '__main__':
    runPage()
