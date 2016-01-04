# -*- coding: utf-8 -*-
"""
Created on Tue Jan 05 01:09:02 2016

@author: haqiqi
"""

data='POST /bin/login HTTP/1.1\r\nHost: 127.0.0.1:8000\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nUser=Peter+Lee&pw=123456&action=login\r\n\r\n'
#print data
string=data.split('\r\n')               #get end data
list1 = [x for x in string if x]        #delete empty list
list2=list1[-1].replace('+', ' ')       #replacing character
                                        #belum nge replace hexa
list3=list2.split('&')                  #split parameter
data={}                                 #dictionary nampung semua data yang ada di parameter
for i in list3:
    tmp=i.split('=')
    data[tmp[0]]=tmp[1]

print data['action']
