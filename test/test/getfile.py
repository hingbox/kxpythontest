#!/usr/bin/python
# _*_ coding:utf-8 _*_ //为了告诉python解释器，按照utf-8编码读取源代码，否则，你在源代码中写的中文输出可能会由乱码
import struct
import sys
import os
def GetFileFromThisRootDir(dir,ext = None):
  allfiles = []
  needExtFilter = (ext != None)
  for root,dirs,files in os.walk(dir):
    for filespath in files:
      filepath = os.path.join(root, filespath)
      extension = os.path.splitext(filepath)[1][1:]
      if needExtFilter and extension in ext:
        allfiles.append(filepath)
      elif not needExtFilter:
        allfiles.append(filepath)
  return allfiles
'''
1、读取指定目录下的所有文件
2、读取指定文件，输出文件内容
3、创建一个文件并保存到指定目录
'''
def eachFile(filepath):
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s%s' % (filepath, allDir))
        print child.decode('gbk') # .decode('gbk')是解决中文显示乱码问题

# 读取文件内容并打印
def readFile(filename):
    fopen = open(filename, 'r') # r 代表read
    for eachLine in fopen:
        print "读取到得内容如下：",eachLine
    fopen.close()


# 输入多行文字，写入指定文件并保存到指定文件夹
def writeFile(filename):
    fopen = open(filename, 'w')
    print "\r请任意输入多行文字"," ( 输入 .号回车保存)"
    while True:
        aLine = raw_input()
        if aLine != ".":
            fopen.write('%s%s' % (aLine, os.linesep))
        else:
            print "文件已保存!"
            break
    fopen.close()
# 在读文件的时候往往需要遍历文件夹，python的os.path包含了很多文件、文件夹操作的方法。下面列出：
#
# os.path.abspath(path) #返回绝对路径
# os.path.basename(path) #返回文件名
# os.path.commonprefix(list) #返回多个路径中，所有path共有的最长的路径。
# os.path.dirname(path) #返回文件路径
# os.path.exists(path)  #路径存在则返回True,路径损坏返回False
# os.path.lexists  #路径存在则返回True,路径损坏也返回True
# os.path.expanduser(path)  #把path中包含的"~"和"~user"转换成用户目录
# os.path.expandvars(path)  #根据环境变量的值替换path中包含的”$name”和”${name}”
# os.path.getatime(path)  #返回最后一次进入此path的时间。
# os.path.getmtime(path)  #返回在此path下最后一次修改的时间。
# os.path.getctime(path)  #返回path的大小
# os.path.getsize(path)  #返回文件大小，如果文件不存在就返回错误
# os.path.isabs(path)  #判断是否为绝对路径
# os.path.isfile(path)  #判断路径是否为文件
# os.path.isdir(path)  #判断路径是否为目录
# os.path.islink(path)  #判断路径是否为链接
# os.path.ismount(path)  #判断路径是否为挂载点（）
# os.path.join(path1[, path2[, ...]])  #把目录和文件名合成一个路径
# os.path.normcase(path)  #转换path的大小写和斜杠
# os.path.normpath(path)  #规范path字符串形式
# os.path.realpath(path)  #返回path的真实路径
# os.path.relpath(path[, start])  #从start开始计算相对路径
# os.path.samefile(path1, path2)  #判断目录或文件是否相同
# os.path.sameopenfile(fp1, fp2)  #判断fp1和fp2是否指向同一文件
# os.path.samestat(stat1, stat2)  #判断stat tuple stat1和stat2是否指向同一个文件
# os.path.split(path)  #把路径分割成dirname和basename，返回一个元组
# os.path.splitdrive(path)   #一般用在windows下，返回驱动器名和路径组成的元组
# os.path.splitext(path)  #分割路径，返回路径名和文件扩展名的元组
# os.path.splitunc(path)  #把路径分割为加载点与文件
# os.path.walk(path, visit, arg)  #遍历path，进入每个目录都调用visit函数，visit函数必须有3个参数(arg, dirname, names)，dirname表示当前目录的目录名，names代表当前目录下的所有文件名，args则为walk的第三个参数
# os.path.supports_unicode_filenames  #设置是否支持unicode路径名
# rootdir = 'F:\data'
#  list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
#  for i in range(0,len(list)):
#       path = os.path.join(rootdir,list[i])
#         if os.path.isfile(path):
#                #你想对文件的操作

if __name__ == '__main__':
    #GetFileFromThisRootDir("E:\\ciku\\test\\",None)
    filePathC = "E:\\ciku\\download"
    filePath = "D:\\FileDemo\\Java\\myJava.txt"
    filePathI = "D:\\FileDemo\\Python\\pt.py"
    eachFile(filePathC)
    #readFile(filePath)
    #writeFile(filePathI)