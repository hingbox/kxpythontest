#!/usr/bin/python
# _*_ coding:utf-8 _*_ //为了告诉python解释器，按照utf-8编码读取源代码，否则，你在源代码中写的中文输出可能会由乱码
print 300
print '100+200=',100+200
#name = raw_input('请输入name')
#print name
a=3<2
print a
c ='hi %s,age %d' %('kuang',10)
print c

sum=0
for x in range(101):
    sum=sum+x
    print sum

d={'a':66,'b':77,'c':88}
for k,v in d.iteritems():
    print k,v
d.pop('a')
print d.get('a',-1)

a = abs(-10)
print a

def my_abs(x):
    if not isinstance(x,(int,float)):
        raise TypeError('bad type')
    if x>0:
        return x
    else :
        return -x
print my_abs(100)

l = range(100)
t = l[1:5]
print t

