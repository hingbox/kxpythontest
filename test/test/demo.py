# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>你好</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""
soup = BeautifulSoup(html)
print '=============='+soup.name
print '=============='+soup.head.name

print soup.p.attrs
print soup.p['class']
print '====='+soup.p.string
print type(soup.p.string)


print('======================BeautifulSoup====================')
print type(soup.name)
#<type 'unicode'>
print soup.name
# [document]
print soup.attrs
#{} 空字典



#遍历文档树  1.直接子节点 .contents  .children  属性
print('======打印子节点=====')
print soup.head.contents
print soup.head.children

for children in soup.body.children:
    print children

print('======打印所有子孙节点=====')
#所有子孙节点
for child in soup.descendants :
    print child

print ('===html====', soup.html.string)
for string in soup.strings:
    print(repr(string))

print('父节点  .parent 属性')
p = soup.p
print p.parent.name


print('全部父节点 .parents 属性')
content = soup.head.title.string
for  parent in content.parents:
    print parent.name


print('兄弟节点 .next_sibling  .previous_sibling 属性')
print soup.p.next_sibling
#       实际该处为空白
print soup.p.prev_sibling
#None   没有前一个兄弟节点，返回 None
print soup.p.next_sibling.next_sibling
#<p class="story">Once upon a time there were three little sisters; and their names were
#<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>,
#<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
#<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;
#and they lived at the bottom of a well.</p>
#下一个节点的下一个兄弟节点是我们可以看到的节点



print('全部兄弟节点.next_siblings  .previous_siblings 属性')
for sibling in soup.a.next_siblings:
    print(repr(sibling))
    # u',\n'
    # <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
    # u' and\n'
    # <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
    # u'; and they lived at the bottom of a well.'
    # None


print('前后节点 .next_element  .previous_element 属性')
print soup.head.next_element



print('所有前后节点 .next_elements  .previous_elements 属性')

for tag in soup.find_all(re.compile("^b")):
    print(tag.name)

# def has_class_but_no_id(tag):
#     return tag.has_attr('class') and not tag.has_attr("id")
# soup.find_all(has_class_but_no_id("p"))

print (soup.find_all(id='link1'))
print (soup.find_all(href=re.compile("elsie")))

print('css选择器 直接找标签 ')
print (soup.select('a'))

print('css选择器 通过类名查找')
print(soup.select('.title'))
print('css选择器 通过id查找')
print(soup.select('#link1'))


print('属性查找')
print(soup.select('a[class="sister"]'))


def _const_1(name):
    print "Hello,%s" % name
def _const_2(name):
    print "Hi,%s" % name
def greet(name):
    if len(name) > 3:
        print _const_1(name)
    else:
        print _const_2(name)
greet("nininini")

print('========start=======')
'''
print('sdfsfasfsadfs')
'''
print('=========end=======')




'''
用情况语句比较好，如果第一个字母一样，则判断用情况语句或if语句判断第二个字母
'''
letter = raw_input("please input:")
# while letter  != 'Y':
if letter == 'S':
    print ('please input second letter:')
    letter = raw_input("please input:")
    if letter == 'a':
        print ('Saturday')
    elif letter == 'u':
        print ('Sunday')
    else:
        print ('data error')

elif letter == 'F':
    print ('Friday')

elif letter == 'M':
    print ('Monday')

elif letter == 'T':
    print ('please input second letter')
    letter = raw_input("please input:")

    if letter == 'u':
        print ('Tuesday')
    elif letter == 'h':
        print ('Thursday')
    else:
        print ('data error')

elif letter == 'W':
    print ('Wednesday')
else:
    print ('data error')