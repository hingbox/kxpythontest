#!/usr/bin/env python # -*- coding: utf-8 -*-
#version1.1.0.2013070801
#history #  2013070801 add md5 in json #  Priority intable

#导入ftplib扩展库
import shutil
import bsddb
import ftplib
from ftplib import FTP
import ConfigParser
import urlparse
import optparse
import logging
import urllib,urllib2,re, base64
import Queue, threading, sys
from threading import Thread
from threading import Timer
import time
import os.path
import traceback
import subprocess
import socket
import time
import string
from datetime import datetime, timedelta
from xml2dict import XML2Dict
from object_dict import object_dict
import json
import hashlib

# Import CherryPy global namespace
import cherrypy
from sqlalchemy import *

# working thread
g_stopPool = False
g_wm = None
g_db = None
#指定IP地址和端口，连接到FTP服务，上面显示的是FTP服务器的Welcome信息 
config = ConfigParser.ConfigParser()
config.read("config.ini")
g_localpath=config.get('ftp','localpath')
g_ftpPassive  =config.get('ftp','ftppassive')
g_retrynum= int(config.get('ftp','retrys'))
g_retrysleep=int(config.get('ftp','retrysleep'))
#task
g_checktimer=config.get('task','checktimer')
g_notifyURL= config.get('task','notifyURL')
#db
g_DatbaseType = config.get('db','type')
g_DatabaseUser=config.get('db','user')
g_DatabasePwd=config.get('db','password')
g_DatabaseHost =config.get('db','host')
g_DatabaseName=config.get('db','name')
g_DatabasePath=config.get('db','path')

def getFileMd5(strFile):  
        file = None 
        bRet = False
        strMd5 = ""
        try:  
                file = open(strFile, "rb")
                md5 = hashlib.md5()
                strRead = ""
                while True:  
                        strRead = file.read(8096);  
                        if not strRead:  
                                break
                        md5.update(strRead)
                #read file finish  
                bRet = True
                strMd5 = md5.hexdigest()
        except:  
                bRet = False
        finally:  
                if file:  
                        file.close()
        return {"result":bRet,"md5":strMd5}

def ensure_dir(f):
        d = os.path.dirname(f)
        if len(d)>0 and not os.path.exists(d):
                os.makedirs(d)   
def parseurl(url):
        urlparts = urlparse.urlparse(url)
        username =""
        password =""
        host     =""
        port     =""
        fullpath     = urlparts.path
        path =""
        filename =""
        parts = urlparts.netloc.split("@")
        #print parts
        if len(parts)==2:
                userpwdparts = parts[0].split(":")
                if len(userpwdparts)==2:
                        username = userpwdparts[0]
                        password = userpwdparts[1]
                ipportparts  = parts[1].split(":")
                if len(ipportparts)==2:
                        host = ipportparts[0]
                        port = ipportparts[1]
                elif len(ipportparts)==1:
                        host = ipportparts[0]
                        port = "21"
        elif len(parts)==1:
                ipportparts  = parts[0].split(":")
                if len(ipportparts)==2:
                        host = ipportparts[0]
                        port = ipportparts[1]
                elif len(ipportparts)==1:
                        host = ipportparts[0]
                        port = "21"
        if len(fullpath)>0 and fullpath[0]=='/':
                        fullpath = fullpath[1:]
        index = fullpath.rfind("/")
        if index!=-1:
                path = fullpath[0:index]
                filename = fullpath[index+1:]
        else:
                path = ""
                filename = fullpath
        return {"username":username,"password":password,"host":host,"port":port,"path":path,"filename":filename}
def get_filesuffix(filename):
        index = filename.rfind(".")
        if index!=-1:
                return filename[index:]
        else:
                return ""
def get_downloadfilename(url,pathroot):
        urlelemdict =  parseurl(url)
        filename = urlelemdict.get("path")      
        if filename!="":                
                filename = "%s/%s" % (pathroot,filename)
        return filename
def getHttpFileSize(url): 
    length = 0 
    try: 
        conn = urllib.urlopen(url) 
        headers = conn.info().headers
        print headers
        for header in headers: 
            if header.find('Content-Length') != -1: 
                length = header.split(':')[-1].strip() 
                length = int(length) 
    except Exception, err:
        print err
        pass 
    return length
def httpdownload(url,localfile,taskid):
        tmpresult = 0
        tmpresultdesc=''
        try:
                bufferSize=8192
                lsize=0L
                fsize = getHttpFileSize(url)
                print 'remote file size:%d' % fsize
                if os.path.exists(localfile):    
                        lsize=os.stat(localfile).st_size
                if lsize >= fsize:    
                        #print 'local file is bigger or equal remote file'    
                        return {"result":0,"resultdesc":'already exists'}
                print 'local file size:%d' % lsize
                ensure_dir(localfile)
                f = open(localfile, 'ab')
                try:                        
                        request = urllib2.Request(url)
                        #fsize = lsize+8192-1  #only for test patial download
                        request.add_header('Range', 'bytes=%d-%d' % (lsize,fsize)) 
                        conn = urllib2.urlopen(request) 
                        startTime = time.time()
                        data = conn.read(bufferSize)
                        while data:
                                f.write(data)
                                data = conn.read(bufferSize)
                        conn.close()
                except Exception,e:
                        print e
                        tmpresult = -1
                        tmpresultdesc ='%s' % e
                f.close()
        except Exception ,e2:
                print e2
                tmpresult = -1
                tmpresultdesc ='%s' % e2
                
        return {"result":tmpresult,"resultdesc":tmpresultdesc}


class MyFTP(FTP):#对FTP的继承  
        #继承父类中的方法,在子类中可以直接调用  
        #重载父类中retrbinary的方法
        def retrbinary(self, cmd, callback, fsize=0,rest=0):  
                blocksize=1024  
                cmpsize=rest  
                self.voidcmd('TYPE I')  
                conn = self.transfercmd(cmd, rest)#此命令实现从指定位置开始下载,以达到续传的目的
                while 1:  
                        if fsize:  
                                print '\b'*30,'%.2f%%'%(float(cmpsize)/fsize*100),
                                #print fsize
                        data = conn.recv(blocksize)  
                        if not data:
                                break
                        callback(data)  
                        cmpsize+=blocksize  
                conn.close()  
                return self.voidresp()  
    
def ftpdownload(url,localfile,taskid):
        tmppath=url
        tmpresult = 0
        tmpresultdesc=''
        DownLocalFilename =""
#创建ftp对象实例 
        ftp = MyFTP()  
        try:
                urlelemdict =  parseurl(url)
                tmpftpip = urlelemdict.get("host")
                tmpftpport = urlelemdict.get("port")
                tmpusername= urlelemdict.get("username")
                tmpuserpwd= urlelemdict.get("password")
                tmppath = urlelemdict.get("path")
                tmpfilename = urlelemdict.get("filename")
                tmpfilesuffix = get_filesuffix(tmpfilename)
                ftp.connect(tmpftpip, tmpftpport)  
#通过账号和密码登录FTP服务器 
                ftp.login(tmpusername,tmpuserpwd)
        
#如果参数 pasv 为真，打开被动模式传输 (PASV MODE) ，
#否则，如果参数 pasv 为假则关闭被动传输模式。
#在被动模式打开的情况下，数据的传送由客户机启动，而不是由服务器开始。
#这里要根据不同的服务器配置
                if g_ftpPassive=='False':
                        ftp.set_pasv(False)
                        print "Set Passive False"
                else:
                        ftp.set_pasv(True)
                        print "Set Passive True"
#在FTP连接中切换当前目录
                if tmppath:
                    ftp.cwd(tmppath)  
#为准备下载到本地的文件，创建文件对象                    
                fsize=ftp.size(tmpfilename)    
                if fsize==0 :
                        #print 'remote filesize is 0'
                        return {"result":-1,"resultdesc":'remote filesize is '}
                lsize=0L    
                if os.path.exists(localfile):    
                        lsize=os.stat(localfile).st_size
                if lsize >= fsize:    
                        #print 'local file is bigger or equal remote file'    
                        return {"result":0,"resultdesc":'already exists'}
                #f = open(localfile, 'wb')
                ensure_dir(localfile)
                f = open(localfile, 'ab')
                try:
#从FTP服务器下载文件到前一步创建的文件对象，其中写对象为f.write，1024是缓冲区大小  
                        ftp.retrbinary('RETR ' + tmpfilename , f.write,fsize,lsize)  
#关闭下载到本地的文件  
#提醒：虽然Python可以自动关闭文件，但实践证明，如果想下载完后立即读该文件，最好关闭后重新打开一次
                except ftplib.error_perm:
                        tmpresult = -1
                f.close()  
#关闭FTP客户端连接
                ftp.close()
        except ftplib.error_perm,error:
                #print 'ERROR: cannot CD to  "%s"' %tmppath
                print error
                tmpresultdesc = '%s' % error
                tmpresult = -1
        #if tmpresult==0:
        #        print 'download success: %s' % DownLocalFilename        
        return {"result":tmpresult,"resultdesc":tmpresultdesc}
def postNotify(taskid,relpath,ftpurl,filesize,result,resultdesc):
        tmpstate="Complete"
        tmpprogress=0
        tmpnotifyresult =0
        tmpnotifyresultdesc=''
        if result==0:
                tmpprogress =100
                tmpstate="Complete"
        else:
                tmpprogress=0
                tmpstate="Failed"
        #下载完成：{"serviceName":"DownloadFinishNoticeClient","args":{"result":"-1","filesize":"0","ftpaddress":"BESTVIMSP/201307/16022167022479_20130705155220.ts","did":"16022167022479","resultdesc":"ftp download error!ftp://imspftp:imspftp@61.8.169.228:21/f/H264/20130705/2730248.ts"}}     
        tmpjsonobj = {"serviceName":"DownloadFinishNoticeClient","args":{"result":result,"filesize":filesize,"ftpaddress":relpath,"did":taskid,"resultdesc":resultdesc}}                
        try:
                print g_notifyURL
                tmpjsonstr = json.dumps(tmpjsonobj)
                print tmpjsonstr
                req = urllib2.Request(g_notifyURL, data=tmpjsonstr)
                req.add_header('Content-Type', 'text/json')
                fp = urllib2.urlopen(req)
                response =  fp.read();
                print response
        except Exception,err:                
                print "Reponse %s Send Error\n" % g_notifyURL
                tmpnotifyresult = -1
                tmpnotifyresultdesc ='%s' % err
        return {"result":tmpnotifyresult,"resultdesc":tmpnotifyresultdesc}
                

class Worker(Thread):
        worker_count = 0
        timeout = 1
        sleep = 0.5
        def __init__( self, workQueue, resultQueue, **kwds):
                Thread.__init__( self, **kwds )
                self.id = Worker.worker_count
                Worker.worker_count += 1
                self.setDaemon( True )
                self.workQueue = workQueue
                self.resultQueue = resultQueue
                self.start( )

        def run( self ):
                global g_stopPool
                ''' the get-some-work, do-some-work main loop of worker threads '''
                while not g_stopPool:
                        try:
                                if not self.workQueue.empty():
                                        callable, args, kwds = self.workQueue.get(timeout=Worker.timeout)
                                        res = callable(*args, **kwds)
                                        print "worker[%2d]: %s" % (self.id, str(res) )
                                        #self.resultQueue.put( res )
                                time.sleep(Worker.sleep)
                        except Queue.Empty:     
                                print "Queue empty"             
                                time.sleep(Worker.sleep)
                                continue;
                        except :
                                print 'worker[%2d]' % self.id, sys.exc_info()[:2]
                                raise
                print "End of Worker Thread\r\n"
class WorkerManager:
        def __init__( self, num_of_workers=10, timeout = 2):
                self.workQueue = Queue.Queue()
                self.resultQueue = Queue.Queue()
                self.workers = []
                self.timeout = timeout
                self._recruitThreads( num_of_workers )

        def _recruitThreads( self, num_of_workers ):
                for i in range( num_of_workers ):
                        worker = Worker( self.workQueue, self.resultQueue )
                        self.workers.append(worker)

        def wait_for_complete( self):
                # ...then, wait for each of them to terminate:
                while len(self.workers):
                        worker = self.workers.pop()
                        worker.join( )
                        if worker.isAlive() and not self.workQueue.empty():
                                self.workers.append( worker )
                print "All jobs are are completed."
        def isqueuefull(self):
                return self.workQueue.full()
        def add_job( self, callable, *args, **kwds ):
                self.workQueue.put( (callable, args, kwds) )

        def get_result( self, *args, **kwds ):
                return self.resultQueue.get( *args, **kwds )

#Begin of Tread job

class HelloWorld:
        def index(self):
        # CherryPy will call this method for the root URI ("/") and send
        # its return value to the client. Because this is tutorial
        # lesson number 01, we'll just send something really simple.
        # How about...
#        print cherrypy.serving.request.body.read()
        #str = cherrypy.request.body.readlines()
                global g_wm
                if cherrypy.request.method.upper()=="POST":
                        postdata =  cherrypy.request.body.read()
                        print postdata
                        try:
                                tmpjsonobj = json.loads(postdata)
                                tmpdid = tmpjsonobj["args"]["did"]
                                tmpcspid = tmpjsonobj["args"]["cspid"]
                                tmpftpaddress = tmpjsonobj["args"]["ftpaddress"]
                                tmpmd5 = ''
                                if tmpjsonobj["args"].has_key("md5"):
                                        tmpmd5 = tmpjsonobj["args"]["md5"]
                                
                                tmppriority = 0
                                if tmpjsonobj["args"].has_key("priority"):
                                        tmppriority = tmpjsonobj["args"]["priority"]

                                
                                g_db.save_task(tmpdid,tmpcspid,tmpftpaddress,tmpmd5,int(tmppriority),postdata)
                                #treatCommand(postdata) #for test
                        except Exception,e:
                                #print "can not analyse command,ignored"
                                print e
                                return '{"code":-1,"message":"%s"}' % e
                return '{"code":0,"message":"ok"}'
        def PVRCallback(self):
                print "PVR callback"            
                return "success"
        PVRCallback.exposed = True
        index.exposed = True

def getsubstr(summary,lenmax):
        if len(summary)>lenmax:
                summary = summary.decode('utf-8')[:lenmax].encode('utf-8')
        return summary
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
                schedule_table=Table('t_agent_dq',self.metadata,
                Column('PKID',Integer,primary_key=True),
                Column('TaskID',String(64),unique=True),
                Column('FileURL',String(2048)),
                Column('FileMD5',String(64)),
                Column('Priority',Integer),    
                Column('CSPID',String(64)),
                Column('ElementID',String(64)),
                Column('RelPath',String(1024)),
                Column('AbsPath',String(1024)),
                Column('CreateTime',Integer),
                Column('ExecuteTime',Integer),
                Column('FinishTime',Integer),                
                Column('Retrys',Integer),
                Column('Cmd',String(4096)),
                Column('ResultCode',Integer),
                Column('ResultDesc',String(128)),
                Column('NotifyTime',Integer),
                Column('NotifyResult',Integer),
                Column('NotifyResultDesc',String(128)),
                Column('MD5Result',Integer),
                Column('MD5ResultDesc',String(128)),
                Column('State',Integer))

                if not schedule_table.exists():
                        schedule_table.create()
        def update_inprogresstask(self):
                print "update_inprogresstask"
                schedule_table=Table('t_agent_dq',self.metadata,autoload=True)
                schedule_table.update(
                schedule_table.c.State==1,values={
                schedule_table.c.State:0}).execute()

        def save_task(self,taskid,cpid,fileurl,filemd5,priority,cmd):
                print "Save downloadtask"
                schedule_table=Table('t_agent_dq',self.metadata,autoload=True)
                r=schedule_table.select(schedule_table.c.TaskID==taskid).execute()
                testrow = r.fetchone()
                if testrow==None:
                        i=schedule_table.insert()
                        i.execute(
                        TaskID=taskid,
                        FileURL=fileurl,
                        FileMD5=filemd5,
                        Priority=priority,
                        CSPID=cpid,
                        Cmd=cmd,
                        State=0,
                        CreateTime=time.time())
                else:
                        #更新状态为0,重新触发下载
                        if testrow["State"]==0 or testrow["State"]==1:
                                print "%s Exist already inqueue:" % taskid
                        else:
                                print "%s Exist restart:" % taskid
                                #这儿要判断是否删除已经下载的文件
                                schedule_table.update(
                                        schedule_table.c.PKID==testrow["PKID"],values={
                                        schedule_table.c.FileURL:fileurl,
                                        schedule_table.c.FileMD5:filemd5,
                                        schedule_table.c.Priority:priority,
                                        schedule_table.c.CSPID:cpid,
                                        schedule_table.c.Cmd:cmd,
                                        schedule_table.c.State:0}).execute()
                                
        def getnexttask(self):
                schedule_table=Table('t_agent_dq',self.metadata,autoload=True)
                r=schedule_table.select(schedule_table.c.State==0).execute()
                testrow = r.fetchone()
                return testrow
        def updatetaskstate(self,pkid,state):
                schedule_table=Table('t_agent_dq',self.metadata,autoload=True)
                schedule_table.update(
                schedule_table.c.PKID==pkid,values={
                schedule_table.c.ExecuteTime:time.time(),
                schedule_table.c.State:state}).execute()
        def gettask(self,taskid):
                schedule_table=Table('t_agent_dq',self.metadata,autoload=True)
                r=schedule_table.select(schedule_table.c.TaskID==taskid).execute()
                return r.fetchone()
        def deletetask(self,taskid):
                print "delete task"
                schedule_table=Table('t_agent_dq',self.metadata,autoload=True)
                schedule_table.delete(schedule_table.c.TaskID == taskid).execute()
        def savenotifyresult(self,taskid,notifyresult,notifyresultdesc):
                print "notify result save %s %s\n" % (taskid,notifyresult)
                schedule_table=Table('t_agent_dq',self.metadata,autoload=True)
                r=schedule_table.select(schedule_table.c.TaskID==taskid).execute()
                tmpdeststate = 10#载任务表 STATUS {0:'等待下载',10:'通知成功',20:'通知失败',30:'下载成功',40:'下载失败'}
                notifyresultdesc = getsubstr(notifyresultdesc,128)
                if notifyresult!=0:
                        tmpdeststate = 20
                row = r.fetchone()
                if row!=None:
                        print 'task find update:%s' % taskid
                        schedule_table.update(
                        schedule_table.c.PKID==row["PKID"],values={
                        schedule_table.c.NotifyTime:time.time(),
                        schedule_table.c.NotifyResult:notifyresult,
                        schedule_table.c.NotifyResultDesc:notifyresultdesc}).execute()
                else:
                        print 'not found task:%s' % taskid
                        
        def savedownloadresult(self,taskid,relpath,abspath,retrynum,result,resultdesc,md5result,md5resultdesc):#下载完成，更新
                print "download result save %s %s\n" % (taskid,result)
                schedule_table=Table('t_agent_dq',self.metadata,autoload=True)
                r=schedule_table.select(schedule_table.c.TaskID==taskid).execute()
                tmpdeststate = 30#载任务表 STATUS {0:'等待下载',10:'通知成功',20:'通知失败',30:'下载成功',40:'下载失败'}
                resultdesc = getsubstr(resultdesc,128)
                if result!=0:
                        tmpdeststate = 40
                row = r.fetchone()
                if row!=None:
                        print 'task find update:%s' % taskid
                        schedule_table.update(
                        schedule_table.c.PKID==row["PKID"],values={
                        schedule_table.c.RelPath:relpath,
                        schedule_table.c.AbsPath:abspath,
                        schedule_table.c.Retrys:retrynum,
                        schedule_table.c.FinishTime:time.time(),
                        schedule_table.c.ResultCode:result,
                        schedule_table.c.ResultDesc:resultdesc,
                        schedule_table.c.MD5Result:md5result,
                        schedule_table.c.MD5ResultDesc:md5resultdesc,
                        schedule_table.c.State:tmpdeststate}).execute()
                else:
                        print 'not found task:%s' % taskid

def treatCommand(data,sleep = 0.001):
        print 'thread job [%s]' % data
        #{"serviceName":"DownloadMovieFile","args":{"cspid":"BESTVIMSP","ftpaddress":"ftp://imspftpclient:imspftpclient@61.8.169.233:21/storage1/20130216/1949618.ts","did":"15954975414338"}}
        try:
                tmpjsonobj = json.loads(data)
                print tmpjsonobj
                #print tmpjsonobj["args"]["cspid"]
                #print tmpjsonobj["args"]["ftpaddress"]
                #print
                tmpretrynum = 0
                tmpcspid = tmpjsonobj["args"]["cspid"]
                tmpurl = tmpjsonobj["args"]["ftpaddress"]
                tmpmd5 = ''
                if tmpjsonobj["args"].has_key('md5'):
                        tmpmd5 = tmpjsonobj["args"]["md5"]
                tmptaskid = tmpjsonobj["args"]["did"]
                tmplocalfile= g_localpath
                urlelemdict =  parseurl(tmpurl)
                filename = urlelemdict.get("filename")
                remotepath = urlelemdict.get("path")    
                relpath = tmpcspid+"/"+remotepath+"/"+filename
                if g_localpath.endswith("/"):
                        tmplocalfile = g_localpath + relpath
                else:
                        tmplocalfile = g_localpath +"/"+relpath                                
                print tmplocalfile
                if tmpurl.startswith("http://") or tmpurl.startswith("HTTP://"):
                        for i in range(g_retrynum):                                
                                tmpdownresult = httpdownload(tmpurl,tmplocalfile,tmptaskid)
                                if tmpdownresult["result"]==0:
                                        break
                                else:
                                        time.sleep(g_retrysleep)
                elif tmpurl.startswith("ftp://") or tmpurl.startswith("FTP://"):
                        for i in range(g_retrynum):
                                print 'loop:%d' % i
                                tmpdownresult = ftpdownload(tmpurl,tmplocalfile,tmptaskid)
                                if tmpdownresult["result"]==0:
                                        break
                                else:
                                        time.sleep(g_retrysleep)
                else:
                        tmpdownresult = {"result":-1,"resultdesc":"Not supported protocol"}
                tmpretrynum = i
                print tmpdownresult
                print 'retrys:%d' % tmpretrynum
                filesize=0L
                tmpmd5result =0
                tmpmd5resultdesc=''
                if tmpdownresult["result"]==0:
                        if os.path.exists(tmplocalfile):    
                                filesize=os.stat(tmplocalfile).st_size
                                if tmpmd5!='':
                                        tmpmd5row = getFileMd5(tmplocalfile)
                                        if tmpmd5row["result"]==True:
                                                if tmpmd5row["md5"]==tmpmd5:                                                        
                                                        tmpmd5result=0
                                                        tmpmd5resultdesc= 'Md5 is the same,file ok'
                                                else:
                                                        tmpmd5result = -1
                                                        tmpmd5resultdesc='Md5 check fail,file nok,md5:%s current:%s' % (tmpmd5,tmpmd5row["md5"])
                                        else:                                                
                                                tmpmd5result = -1
                                                tmpmd5resultdesc= 'can not caculate md5'
                                        
                                else:
                                        tmpmd5result = 0
                                        tmpmd5resultdesc= 'No md5 defined ,skip validation'

                g_db.savedownloadresult(tmptaskid,relpath,tmplocalfile,tmpretrynum+1,tmpdownresult["result"],tmpdownresult["resultdesc"],tmpmd5result,tmpmd5resultdesc)
                tmpnotifyresult = postNotify(tmptaskid,relpath,tmpurl,filesize,tmpdownresult["result"],tmpdownresult["resultdesc"])
                g_db.savenotifyresult(tmptaskid,tmpnotifyresult["result"],tmpnotifyresult["resultdesc"])
        except Exception,e:
                #print "can not analyse command,ignored"
                print e
        
        




class checktasktimer(threading.Thread): #The timer class is derived from the class threading.Thread  
        def __init__(self, num, interval):  
                threading.Thread.__init__(self)  
                self.thread_num = num  
                self.interval = interval  
                self.thread_stop = False

        def run(self): #Overwrite run() method, put what you want the thread do here
                global g_wm
                while not self.thread_stop:  
                         #print 'Thread Object(%d), Time:%s\n' %(self.thread_num, time.ctime())
                        if not g_wm.isqueuefull():
                                taskrow = g_db.getnexttask()
                                if taskrow:
                                        g_db.updatetaskstate(taskrow["PKID"],1)                              
                                        g_wm.add_job( treatCommand, taskrow["Cmd"], 1*0.001 )
                                else:
                                        time.sleep(self.interval)
                        else:
                                time.sleep(self.interval)  
        def stop(self):  
                self.thread_stop = True  
def getcnname(myname):
           type = sys.getfilesystemencoding()
           return myname.decode('UTF-8').encode(type)

agentconf = "./agent.conf" #os.path.join(os.path.dirname(__file__), 'agent.conf')               
def main():
        #postNotify('12312','csp001/test.ts','ftp://localhost:21/test.ts',54354,0,'ok')
        #print(getFileMd5('d:/pvr/test.ts'))
        g_db.update_inprogresstask()#将所有上次还没执行完的任务设置为0，重新触发下载
        checktaskthread = checktasktimer(1, float(g_checktimer))
        checktaskthread.setDaemon(True)#设置子线程是否随主线程一起结束
        checktaskthread.start()
        cherrypy.quickstart(HelloWorld(), config=agentconf)
        g_stopPool = True
        g_wm.wait_for_complete()
        checktaskthread.stop()

try:
        import signal
        from signal import SIGPIPE, SIG_IGN
        signal.signal(signal.SIGPIPE, signal.SIG_IGN)
except ImportError:         
        pass
        
if __name__ == "__main__":
        g_db = DBManager()
        g_wm = WorkerManager(10)
        main()  

