# _*_ coding:utf-8 _*_ //为了告诉python解释器，按照utf-8编码读取源代码，否则，你在源代码中写的中文输出可能会由乱码
from sqlalchemy import create_engine,Table,Column,Integer,String,MetaData,ForeignKey
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
#MySQL数据库连接字符串
CONSTR='mysql+pymysql://root:root@localhost:3306/alice?charset=utf8'
#初始化数据库连接对象
mysql_engine = create_engine(CONSTR,echo=True)
DB_Session = sessionmaker(bind=mysql_engine)
session = DB_Session()
result = session.execute("select name from user")
#onnection = mysql_engine.connect()
#result = connection.execute("select name from user")
for row in result:
 print "name: ", row['name']
#connection.close()# 5. 关闭连接

mysql_engine.execute("INSERT INTO alice.user(name,fullname) VALUES ('aa','bb');")
result = mysql_engine.execute('select * from user')
result.fetchall()
session.close()

