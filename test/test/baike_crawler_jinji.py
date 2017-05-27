# _*_ coding:utf-8 _*_ //为了告诉python解释器，按照utf-8编码读取源代码，否则，你在源代码中写的中文输出可能会由乱码
#这个是抓取百度百科经济页面信息
import urllib2
from bs4 import BeautifulSoup
from sqlalchemy import *
import sys
import re
reload(sys)
sys.setdefaultencoding( "utf-8" )
#MySQL数据库连接字符串
CONSTR='mysql+pymysql://root:root@localhost:3306/alice?charset=utf8'

engine = create_engine(CONSTR, echo=True)
metadata = MetaData(engine)
#创建百科经济表
baike_jingji_table =Table("t_baike_jingji",metadata,
                   Column("id",Integer,primary_key=True),
                   Column("title",String(50)),
                   Column("url",String(200)),
                   Column("status",Integer))
baike_jingji_d_table =Table("t_baike_jingji_d",metadata,
                   Column("id",Integer,primary_key=True),
                   Column("baike_id",Integer),
                   Column("title",String(50)),
                   Column('title_desc',String(500)),#标题描述
                   Column("url",String(200)),
                   Column('content',String(2000)),#正文内容
                   Column('tag',String(100)),#标签
                   Column("status",Integer))

#创建表
if not baike_jingji_table.exists():
    baike_jingji_table.create()
if not baike_jingji_d_table.exists():
    baike_jingji_d_table.create()

def save_baike_jingji_info(url,title):
    content_table = Table("t_baike_jingji", metadata, autoload=True)
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

def save_baike_jingji_d_info(url,title,baike_id,title_desc,tag):
    content_table = Table("t_baike_jingji_d", metadata, autoload=True)
    r = content_table.select(and_(content_table.c.title == title)).execute()
    testrow = r.fetchone()
    if testrow == None:
        i = content_table.insert()
        i.execute(
            baike_id=baike_id,
            url=url,
            title=title,
            title_desc=title_desc,
            content='',
            tag=tag,
            status=1
        )
    else:
        print "itemexist:%s" % title


#首先得到经济
def runPage():
    page_url = "http://baike.baidu.com/jingji" #经济
    req_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'gzip',
        'Connection': 'close',
        'Referer': None  # 注意如果依然不能抓取的话，这里可以设置抓取网站的host
    }
    try:
        response = urllib2.urlopen(page_url,timeout=5)
        html = response.read()
        soup = BeautifulSoup(html,"html.parser")
        tag_list = soup.find_all("li","column")
        baike_id =1
        for item in tag_list:
            tag_lists = item.find_all("a")# 得到经济,金融的第一条数据  及进入到详情页面
            save_baike_jingji_info(tag_lists[0].get('href'),tag_lists[0].get_text())
            #这个地方需要保存主表
            page_index =1
            for i in range(1,18):
                print('==========================='+format(i))
                jingji_page(tag_lists[0].get('href')+'?limit=30&index={}&offset=30#gotoList'.format(str(i)),baike_id)#得到详情页的url 这个地方分页
                print(tag_lists[0].get('href'))#得到经济学url
           # print(tag_lists[0].contents[1])
                baike_id +=1

        #print()
    except Exception,e:
        print e
def jingji_page(jingji_page_url,baike_id):
    req_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'gzip',
        'Connection': 'close',
        'Referer': None  # 注意如果依然不能抓取的话，这里可以设置抓取网站的host
    }
    try:
        response = urllib2.urlopen(jingji_page_url,timeout=5)
        html = response.read()
        soup = BeautifulSoup(html,"html.parser")
        tag_list = soup.find_all("div","grid-list grid-list-spot",'li')#得到所有的li标签
        #for ii in tag_list:
            #cc = ii.find('div','photo','a')
            #for iii in cc:
                #href_url = iii.get('href')
                #title = iii.get('title')

                # jing_ji_d_page(href_url,desc,baike_id)
                # save_baike_jingji_d_info(href_url,desc,baike_id)
                #print(href_url,title)

        for item in tag_list:
            '''得到每个li下面的a标签'''
            tag_a = item.find_all('a')
            for items in tag_a:
                href_url = items.get('href')
                desc = items.get('title')
                href_url = 'http://baike.baidu.com'+href_url
                jing_ji_d_page(baike_id,href_url,desc)
                #save_baike_jingji_d_info(href_url,desc,baike_id)

    except Exception,e:
        print e

def jing_ji_d_page(baike_id,href_url,desc):
    req_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'gzip',
        'Connection': 'close',
        'Referer': None  # 注意如果依然不能抓取的话，这里可以设置抓取网站的host
    }
    try:
        response = urllib2.urlopen(href_url,timeout=5)
        html = response.read()
        soup = BeautifulSoup(html,'html.parser')
        title_desc = soup.find('div',"lemma-summary")#得到title描述
        descs = title_desc.find('div', 'para').get_text()#
        #print(title_desc.find('div','para').get_text())

        #content = soup.findAll(attrs={"class": "lemma-summary"})
        #print(content[0].string)
        #s = """
        #</span><span style= 'font-size:12.0pt;color:#CC3399'>714659079qqcom    2014/09/10 10:14</span></p></div>
        #"""
        #dr = re.compile(r'<[^>]+>', re.S)
        #dd = dr.sub('', s)
        #print dd
        #print('++++++++++++++++++++++++++++++++++++++'+title_desc.find('a'))
        cc= soup.select('#open-tag-item')
        for item in cc:
            a = item.findAll('span')
            tag =''
            for items in a:
                tag = tag + items.get_text()+','#得到tag
            #print (content)


        #print(href_url,desc,baike_id,title_desc,tag)
        save_baike_jingji_d_info(href_url,desc,baike_id,descs,tag)
    except Exception,e:
        print e


if __name__ == '__main__':
    runPage()
    print('结束')