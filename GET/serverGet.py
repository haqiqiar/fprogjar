import socket
import sys
import time
import os

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
            
def _gen_headers(code,namefile):
    h=''
    
    current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())

    if (code != 301):
             
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
                h += 'Connection: close\r\n'
            elif(code == 403):
                h = 'HTTP/1.1 403 Forbidden\r\n'
                h += 'Date: ' + current_date +'\r\n'
                h += 'Server: Simple-Python-HTTP-Server\r\n'
                h += 'Connection: Keep-Alive\r\n'
            elif(code == 400):
                h = 'HTTP/1.1 400 Bad Request\r\n'
                h += 'Date: ' + current_date +'\r\n'
                h += 'Server: Simple-Python-HTTP-Server\r\n'
                h += 'Content-Length: ' + str(_content_length(namefile)) +'\r\n'
                h += 'Connection: close\r\n'
    else:
        if(code == 301):
            h = 'HTTP/1.1 301 Moved Permanently\r\n'
            h += 'Date: ' + current_date +'\r\n'
            h += 'Server: Simple-Python-HTTP-Server\r\n'
            h += 'Location: http://' + server_address[0] + ':' + str(server_address[1]) + namefile + '/'+'\r\n'

    return h

def GET(uri):
    messages=''
    try:
        type=uri.split('.')[1]    
        file = open(filename,'rb')
        data = file.read(1024)
        print 'you did it'
    except IndexError:
        messages+=_gen_headers(301,'')
        
    
    #except IOError:
       # messages+=_gen_headers(404,filename)
        #content="""\r\n<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
#<html><head>
#<title>404 Not Found</title>
#</head><body>
#<h1>Not Found</h1>
#<p>The requested URL """+uri+""" was not found on this server.</p>
#</body></html>"""
    #messages+=content
    return messages
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
		
	
    if cmd=='GET':
        response=GET(dirc)
    #elif cmd=='HEAD':
        #response=HEAD(dirc)
    #elif cmd=='POST':
        #response=POST(dirc)
    return response
    
    
data="GET /Folder/index.html HTTP/1.1\r\nHost: www.amazon.com\r\nConnection: Close\r\n\r\n"
response=requesthandler(data)
print response