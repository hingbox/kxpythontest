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

