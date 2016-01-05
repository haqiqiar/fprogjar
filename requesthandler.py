# -*- coding: utf-8 -*-
"""
Created on Tue Jan 05 06:58:27 2016

@author: haqiqi
"""
def GET(data):
    return 'GET'

def HEAD(data):
    return 'HEAD'

def POST(data):
    return 'POST'


def requesthandler(data):
    strr=data.split('\r\n')
    list1 = [x for x in strr if x]
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
        response=POST(dirc)
    return response
    
    
data="HEAD index.html HTTP/1.1\r\nHost: www.amazon.com\r\nConnection: Close\r\n\r\n"
response=requesthandler(data)
print response