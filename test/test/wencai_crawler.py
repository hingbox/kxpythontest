#!/usr/bin/env python
#-*- coding: utf-8 -*-
#encoding:  utf-8
#version1.1.0.20150824
import urllib,urllib2,sys,os
import urlparse
from urllib import unquote
import optparse
import random
import time
import re
from BeautifulSoup import BeautifulSoup
import itertools,re
import ConfigParser
from sqlalchemy import *

url_i =1
pic_num = 1

g_localfilepath = 'd:/PycharmProjects/test/img/'
g_db = None
#指定IP地址和端口，连接到FTP服务，上面显示的是FTP服务器的Welcome信息 
config = ConfigParser.ConfigParser()
config.read("config.ini")
#db
g_DatbaseType = config.get('db','type')
g_DatabaseUser=config.get('db','user')
g_DatabasePwd=config.get('db','password')
g_DatabaseHost =config.get('db','host')
g_DatabaseName=config.get('db','name')
g_DatabasePath=config.get('db','path')

class DBManager:
        db = None
        metadata = None 
        def __init__( self):            
                if g_DatbaseType=="mysql":
                        dburl="mysql://%s:%s@%s/%s?charset=utf8" % (g_DatabaseUser,g_DatabasePwd,g_DatabaseHost,g_DatabaseName)
                        self.db = create_engine(dburl,pool_recycle=3600)
                else:
                        dburl =  'sqlite:///%s' % g_DatabasePath #'sqlite:///:memory:'
                        self.db = create_engine(dburl)

                self.metadata = MetaData(self.db)
                self.metadata.echo=True
                content_table=Table('t_news',self.metadata,
                Column('id',Integer,primary_key=True),
                Column('categoryid',Integer),
                Column('categoryname',String(64)),
                Column('tid',String(64)),
                Column('word',String(256)),
                Column('title',String(2048)),
                Column('url',String(2048)),
                Column('status',Integer))
                if not content_table.exists():
                        content_table.create()       
        def save_news(self,categoryid2,tid2,categoryname2,word2,title2,url2):
                content_table=Table('t_news',self.metadata,autoload=True)
                r=content_table.select(and_(content_table.c.categoryid==categoryid2,content_table.c.title==title2)).execute()
                testrow = r.fetchone()
                if testrow==None:
                        i=content_table.insert()
                        i.execute(
                        categoryid=categoryid2,
                        tid=tid2,
                        categoryname=categoryname2,
                        word=word2,
                        title=title2,
                        url=url2,
                        status=1)
                else:
                    print "itemexist:%s" % title2


                                
#自己定义的引号格式转换函数
def _en_to_cn(str):
    obj = itertools.cycle(['“','”'])
    _obj = lambda x: obj.next()
    return re.sub(r"['\"]",_obj,str)
def ensure_dir(f):
        d = os.path.dirname(f)
        if len(d)>0 and not os.path.exists(d):
                os.makedirs(d)  
def get_filesuffix(filename):
        index = filename.rfind(".")
        if index!=-1:
                return filename[index:]
        else:
                return ""
            
def parseurl(url):
        urlparts = urlparse.urlparse(url)
        
def downloadImage(url,relpath):
    print "download "+url+ " to "+relpath
    try:
        name = g_localfilepath+relpath
        ensure_dir(name)
        print 'save '+url+' to file: '+name
        conn = urllib2.urlopen(url,timeout=5)
        req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept':'text/html;q=0.9,*/*;q=0.8',
    'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding':'gzip',
    'Connection':'close',
    'Referer':None #注意如果依然不能抓取的话，这里可以设置抓取网站的host
    }
        #req_timeout = 5
        #req = urllib2.Request(url,None,req_header)
        #conn = urllib2.urlopen(req,None,req_timeout)


        f = open(name,'wb')  
        f.write(conn.read())  
        f.close()  
    except Exception,e: 
        print e

            
def getDetail(categoryid,topic_title,topic_url):
    print topic_url
    #print topic_url
    url =  topic_url
    categoryname=''
    tid =''
    words = ''
    index1 = topic_url.find("&qs=")
    if index1 !=-1:
        index2 = topic_url.find("&",index1+4)
        if index2 !=-1:
            categoryname = topic_url[index1+4:index2]

    index1 = topic_url.find("&tid=")
    if index1 !=-1:
        index2 = topic_url.find("&",index1+5)
        if index2 !=-1:
            tid = topic_url[index1+5:index2]

    index1 = topic_url.find("&w=")
    if index1 !=-1:
        words = topic_url[index1+3:]

    url = 'http://search.10jqka.com.cn/asyn/search?q=%s&queryType=stock&app=qnas&qid=' % words
    #http://search.10jqka.com.cn/asyn/search?q=macd%E9%87%91%E5%8F%89&queryType=stock&app=qnas&qid=
    print 'real retrieve:' + url
    #webDetailContent = urllib2.urlopen(url)
    req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept':'text/html;q=0.9,*/*;q=0.8',
    'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding':'gzip',
    'Connection':'close', 
    'Referer':None #注意如果依然不能抓取的话，这里可以设置抓取网站的host
    }
    #req_timeout = 5
    #req = urllib2.Request(url,None,req_header)
    #webDetailContent = urllib2.urlopen(req,None,req_timeout)

    try:
        webDetailContent = urllib2.urlopen(url,timeout=5)
        detailData = webDetailContent.read()
        #print detailData
        index2 = detailData.find('<ul class=')
        index3 = detailData.find('/ul>"}')
        detailData = detailData[index2:index3+4]
        #print detailData
        detailData = detailData.replace('\\"','"')
        detailData = detailData.replace('\\/','/')
        detailsoup = BeautifulSoup(detailData)
        div_listmain = detailsoup.findAll('ul','r_list r_d_rem')
        #print div_listmain
        for liitem in div_listmain:
            tag_list = liitem.findAll("a")
            #print tag_list
            for item in tag_list:
                item_url =  item.get('href')
                item_title = item.get('title')
                if item_title !=None:
                    s1="u'"+item_title+"'"
                    try:
                        ss=eval(s1)
                        print "title:%s" % ss
                    except:
                        print "err"
                    g_db.save_news(categoryid,tid,categoryname,topic_title,ss,item_url)
    except Exception,e: 
        print e

    print 'end of analyse ：'+ url


def trimhtmlstring(str):
    str = str.replace('&nbsp;','')
    return str


def runpage(pageindex):
        pageurl = "http://search.10jqka.com.cn/stockpick/category"
        print "-------------------------Page " + pageurl + "-------------------------"

        req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept':'text/html;q=0.9,*/*;q=0.8',
        'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding':'gzip',
        'Connection':'close',
        'Referer':None #注意如果依然不能抓取的话，这里可以设置抓取网站的host
        }
        #req_timeout = 30
        #req = urllib2.Request(pageurl,None,req_header)
        #webContent = urllib2.urlopen(req,None,req_timeout)
        try:
            pattern = re.compile("^([0-9]+)*记录")
            webContent = urllib2.urlopen(pageurl,timeout=5)
            data = webContent.read()
            #print data
            #利用BeautifulSoup读取视频列表网页数据
            soup = BeautifulSoup(data)

            tmpIsStartAnalyse = 0
            tag_list = soup.findAll("dd","query_box")
            #print tag_list
            news_categoryid=1
            for item in tag_list:
                news_title=''
                news_img=''
                news_date=''
                news_url=''

                tmphref = item.findAll('a')
                topic_url=tmphref[0].get('href')
                topic_title = tmphref[0].get('title')
                if topic_url <>'':
                    getDetail(news_categoryid,topic_title,topic_url)
                time.sleep(random.randint(12, 50)/100.0)
                #break
        except Exception,e:
            print e
        print "--------------------------------------------------------------"
        print "--------Page " + pageurl + "'analysed !"


def runpage(pageindex):
        pageurl = "http://search.10jqka.com.cn/stockpick/category"
        print "-------------------------Page " + pageurl + "-------------------------"

        req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept':'text/html;q=0.9,*/*;q=0.8',
        'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding':'gzip',
        'Connection':'close',
        'Referer':None #注意如果依然不能抓取的话，这里可以设置抓取网站的host
        }
        #req_timeout = 30
        #req = urllib2.Request(pageurl,None,req_header)
        #webContent = urllib2.urlopen(req,None,req_timeout)
        try:
            pattern = re.compile("^([0-9]+)*记录")
            webContent = urllib2.urlopen(pageurl,timeout=5)
            data = webContent.read()
            #print data
            #利用BeautifulSoup读取视频列表网页数据
            soup = BeautifulSoup(data)

            tmpIsStartAnalyse = 0
            news_categoryid=1
            '''
            tag_list = soup.findAll("dd","query_box")
            for item in tag_list:
                news_title=''
                news_img=''
                news_date=''
                news_url=''

                tmphref = item.findAll('a')
                topic_url=tmphref[0].get('href')
                topic_title = tmphref[0].get('title')
                if topic_url <>'':
                    getDetail(news_categoryid,topic_title,topic_url)
                time.sleep(random.randint(12, 50)/100.0)
                #break
            '''
            tag_list = soup.findAll("div","pro_block")
            for item in tag_list:
                news_title=''
                news_img=''
                news_date=''
                news_url=''

                tmphref = item.findAll('a')
                topic_url=tmphref[0].get('href')
                topic_title = tmphref[0].get('title')
                if topic_url <>'':
                    getDetail(news_categoryid,topic_title,topic_url)
                time.sleep(random.randint(12, 50)/100.0)

        except Exception,e:
            print e



        print "--------------------------------------------------------------"
        print "--------Page " + pageurl + "'analysed !"


if __name__ == '__main__':
    print sys.getdefaultencoding()
    stdout = sys.stdout
    stdin  = sys.stdin
    stderr  = sys.stderr
    reload(sys)
    sys.stdout = stdout
    sys.stdin = stdin
    sys.stderr = stderr
    sys.setdefaultencoding('utf8')
    g_db = DBManager()
    runpage(0)
    time.sleep(2)
