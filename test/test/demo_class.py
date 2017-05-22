#!/usr/bin/env python
#  -*- coding: utf-8 -*-
class myClass:
    """ a simple class"""
    def __init__(self,name,age):
        self.name=name
        self.age=age

    i=12345
    def f(self):
        return 'hello word'
print(myClass.i)
print(myClass.__doc__)
x= myClass('张','1')
print(x.name,x.age)
print(x.f())


