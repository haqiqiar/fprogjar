# -*- coding: utf-8 -*-
"""
Created on Tue Jan 05 01:09:02 2016

@author: haqiqi
"""

def extractor(strr):
    strr=strr.replace('+', ' ')                #replacing + as ' '
    temp=strr.split('%')                       #replacing hexa
    for i in temp[1:]:
        num=i[:2]
        nam=int('0x'+num, 16)
        strr=strr.replace('%'+num, chr(nam))
    strr=strr.split('&')                      #split parameter
    data={}                                   #dictionary nampung semua data yang ada di parameter
    for i in strr:
        tmp=i.split('=')
        data[tmp[0]]=tmp[1]
    print data                                #dictionary
    
    
string='POST /bin/login HTTP/1.1\r\nHost: 127.0.0.1:8000\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nUser=Peter%2BLee&pw=123456&action=login\r\n\r\n'
string1=string.split('\r\n')                  #get end data
string = [x for x in string1 if x]            #delete empty list
final=string[-1]                              #get parameter
extractor(final)


