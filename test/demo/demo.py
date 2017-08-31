#!/usr/bin/python
# _*_ coding:utf-8 _*_ //为了告诉python解释器，按照utf-8编码读取源代码，否则，你在源代码中写的中文输出可能会由乱码
import urllib2
import urllib
import cookielib
import re
url ="http://www.baidu.com"
req_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept':'text/html;q=0.9,*/*;q=0.8',
        'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding':'gzip',
        'Connection':'close',
        'Referer':None #注意如果依然不能抓取的话，这里可以设置抓取网站的host
        }
headers ={'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
request = urllib2.Request(url)
try:
    response = urllib2.urlopen(request)
    print response.read()
except urllib2.URLError,e:
    print e.reason
else:
    print "ok"

# 声明一个CookieJar对象实例来保存cookie
cookie = cookielib.CookieJar()
#利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
handler = urllib2.HTTPCookieProcessor(cookie)
#通过handler来构建opener
opener = urllib2.build_opener(handler)
#此处的open方法同urllib2的urlopen方法，也可以传入request
response = opener.open('http://www.baidu.com')
for item in cookie:
    print 'Name = '+item.name
    print 'Value = '+item.value


#正则表达式
pattern = re.compile(r'hello')
result = re.match(pattern,'hello wwewe')
if result:
    print result.group()
else:
    print '失败!'




