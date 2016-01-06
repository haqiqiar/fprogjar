# -*- coding: utf-8 -*-
"""
Created on Tue Jan 05 06:58:27 2016

@author: haqiqi
"""

import os
import signal
import sys
import time

def _content_length(namefile):
    num_lines = 0
    num_words = 0
    num_chars=0
    with open(namefile, 'r') as f:
        for line in f:
            words = line.split()

            num_lines += 1
            num_words += len(words)
            num_chars += len(line)

            return num_chars
            
def _gen_headers(code, namefile):
    h=''
    current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())

    if (code == 200):
        h = 'HTTP/1.1 200 OK\n'
        h += 'Date: ' + current_date +'\r\n'
        h += 'Server: Simple-Python-HTTP-Server\r\n'
        h += 'Last-Modified: ' + time.ctime(os.path.getmtime(namefile)) +'\r\n'
        h += 'Content-Length: ' + str(_content_length(namefile)) +'\r\n'
        h += 'Connection: close\r\n'
    elif(code == 404):
        h = 'HTTP/1.1 404 Not Found\r\n'
        h += 'Date: ' + current_date +'\r\n'
        h += 'Server: Simple-Python-HTTP-Server\r\n'
        h += 'Content-Length: ' + str(_content_length(namefile)) +'\r\n'
        h += 'Connection: close\r\n'
    elif(code == 403):
        h = 'HTTP/1.1 403 Forbidden\r\n'
        h += 'Date: ' + current_date +'\r\n'
        h += 'Server: Simple-Python-HTTP-Server\r\n'
        h += 'Connection: Keep-Alive\r\n'
    elif(code == 500):
        h = 'HTTP/1.1 500 Internal Server Error\r\n'
        h += 'Date: ' + current_date +'\r\n'
        h += 'Server: Simple-Python-HTTP-Server\r\n'
        h += 'Connection: close\r\n'
    elif(code == 301):
        h = 'HTTP/1.1 301 Moved Permanently\r\n'
        h += 'Date: ' + current_date +'\r\n'
        h += 'Server: Simple-Python-HTTP-Server\r\n'
        h += 'Location: http://' + server_address[0] + ':' + str(server_address[1]) + namefile + '/' + '\r\n'

    return h
	
def extractor(strr):
    strr=strr.replace('+', ' ')                #replacing + as ' '
    temp=strr.split('%')                       #replacing hexa
    for i in temp[1:]:
        num=i[:2]
        nam=int('0x'+num, 16)
        strr=strr.replace('%'+num, chr(nam))
    strr=strr.split('&')                      #split parameter
    parameter={}                                   #dictionary nampung semua data yang ada di parameter 
    for i in strr:
        tmp=i.split('=')
        parameter[tmp[0]]=tmp[1]
    return parameter   

def readfile(dirc):
    blocked=['']
    
    redirected={}
    try:
        f=open(dirc, 'rb')
        if dirc in blocked:
            f=open('page/403.html', 'rb')
            status=403
        
        else:
            status=200
    except IOError:
        if os.path.isdir(dirc):
            f=open('page/301.html', 'rb')
            status=301
        else:
            f=open('page/404.html', 'rb')
            status=404
    return status, f
def readPhp(filename):
    #files=''
    filess=open(filename,'rb')
    files=filess.read(1024)   
    if files[0:5]=='<?php' and files[-2:-1]=='?':
        data=files[6:-2]
    return data
    
    
def GET(data):
    source=data.split('?')
    parameter=extractor(source[1])
    #print parameter
        
    status, files = readfile(source[0])
    data=readPhp(source[0])
    datas=data.split(' ')
    get=datas[1].split("'")
    #print datas
    if datas[0]=='echo':
        if get[0]=='$_GET[':
            #a=2
            print parameter[get[1]]
    #print files.read(1000)
    #print status
    #return _gen_headers(status, source[0])
#=======
    resp= files.read(1000)
    header=_gen_headers(status, source[0])
    return header+'\r\n'+parameter[get[1]]
#>>>>>>> b8d674f59b26508ff3c37a6b90bce063774dcad5

def HEAD(data):
    status, response_content = readfile(data)
    resp = _gen_headers(status, data)
    return resp

def POST(data, source):
    parameter=extractor(source)
    #print parameter
    status, files = readfile(data)
    resp=files.read(1000)
    header=_gen_headers(status, data)
    return header+'\r\n'+resp


def requesthandler(data):
    strr=data.split('\r\n\r\n')
    strlist=strr[0].split('\r\n')
    postsource=strr[1]
    list1 = [x for x in strlist if x]
    req=list1[0]
    req=req.split(' ')

    cmd=req[0]
    dirc=req[1]
    ver=req[2]
    
    strr=list1[1:]
    detail={}
    for i in strr:
        tmp=i.split(': ')
        detail[tmp[0]]=tmp[1]
    #print detail 
    if cmd=='GET':
        response=GET(dirc)
    elif cmd=='HEAD':
        response=HEAD(dirc)
    elif cmd=='POST':
        response=POST(dirc, postsource)
    return response
    
    

data="GET sum.php?what=Progjar_kudu_dapet_A HTTP/1.1\r\nHost: 127.0.0.1:8000\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nUser=Peter%2BLee&pw=123456&action=login\r\n\r\n"


response=requesthandler(data)
print response