#!/usr/bin/python
# _*_ coding:utf-8 _*_ //为了告诉python解释器，按照utf-8编码读取源代码，否则，你在源代码中写的中文输出可能会由乱码
import urllib2
def downhtml(url):
    html = urllib2.urlopen(url).read()
    return html