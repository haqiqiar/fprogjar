# -*- coding: utf-8 -*-
"""
Created on Tue Jan 05 06:58:27 2016

@author: haqiqi
"""

import os

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
    try:
        f=open(dirc, 'rb')
        if dirc in blocked:
            return 403
        else:
            return 200, f
    except IOError:
        if os.path.isdir(dirc):
            return 301
            
    
  
def GET(data):
    return 'GET'

def HEAD(data):
    return 'HEAD'

def POST(data, source):
    parameter=extractor(source)
    print parameter
    
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
    
    
data="POST GET/index.html HTTP/1.1\r\nHost: 127.0.0.1:8000\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nUser=Peter%2BLee&pw=123456&action=login\r\n\r\n"

response=requesthandler(data)
print response