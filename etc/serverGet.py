# -*- coding: utf-8 -*-
"""
Created on Tue Jan 05 06:58:27 2016

@author: haqiqi
"""

import os
def readPhp(filename):
    #files=''
    filess=open(filename,'rb')
    files=filess.read(1024)   
    if files[0:5]=='<?php' and files[-2:-1]=='?':
        data=files[6:-2]
    return data
    
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
    internalServerError=['']
    redirected={}
    try:
        f=open(dirc, 'rb')
        if dirc in blocked:
            f=open('page/403.html', 'rb')
            status=403
        elif dirc in internalServerError:
            f=open('page/500.html', 'rb')
            status=500
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
    #if a[0]=='$_GET':    
    #print files.read(1000)
    #print status
    #return _gen_headers(status, source[0])

def HEAD(data):
    status, response_content = readfile(data)
    temp = _gen_headers(status, data)

    return temp

def POST(data, source):
    parameter=extractor(source)
    #print parameter
    status, files = readfile(data)
    print files.read(1000)
    
    return 'POST'


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
    
    
#<<<<<<< HEAD
data="GET sum.php?what=Progjar_kudu_dapet_A HTTP/1.1\r\nHost: 127.0.0.1:8000\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nUser=Peter%2BLee&pw=123456&action=login\r\n\r\n"
#=======
#data="POST index.html HTTP/1.1\r\nHost: 127.0.0.1:8000\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nUser=Peter%2BLee&pw=123456&action=login\r\n\r\n"
#>>>>>>> 4d2658185f64c5e903277af15a536b01485e6a1d

response=requesthandler(data)
print response