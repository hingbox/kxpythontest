# _*_ coding:utf-8 _*_ //为了告诉python解释器，按照utf-8编码读取源代码，否则，你在源代码中写的中文输出可能会由乱码
from sqlalchemy import create_engine,Table,Column,Integer,String,MetaData,ForeignKey
#创建一个连接引擎
engine = create_engine("mysql+pymysql://root:root@localhost:3306/alice",echo=True)
#创建元数据
metadata=MetaData(engine)
#添加表结构
user=Table('user',metadata,
    Column('id',Integer,primary_key=True),
    Column('name',String(20)),
    Column('fullname',String(40)),
    )
address_table = Table('address', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', None, ForeignKey('user.id')),
    Column('email', String(128), nullable=False)
    )
#执行创建
metadata.create_all()


