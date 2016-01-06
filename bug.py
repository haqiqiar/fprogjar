#!/usr/bin/env python
#http://ilab.cs.byu.edu/python/threadingmodule.html 
import select
import socket
import sys
import threading
import os
import signal
import sys
import time

class Server:
    def __init__(self):
        self.host = 'localhost'
        self.port = 5000
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []

    def open_socket(self):        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host,self.port))
        self.server.listen(5)
        
    def run(self):
        self.open_socket()
        input = [self.server, sys.stdin]
        running = 1
        while running:
            inputready,outputready,exceptready = select.select(input,[],[])

            for s in inputready:

                if s == self.server:
                    # handle the server socket
                    c = Client(self.server.accept())
                    c.start()
                    self.threads.append(c)

                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0

        # close all threads

        self.server.close()
        for c in self.threads:
            c.join()
    
   

class Client(threading.Thread):
    def __init__(self,(client,address)):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024

    
                
    def _content_length(self, namefile):
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
                
    def _gen_headers(self, code, namefile):
        h=''
        current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    
        if (code == 200):
            h = 'HTTP/1.1 200 OK\n'
            h += 'Date: ' + current_date +'\r\n'
            h += 'Server: Simple-Python-HTTP-Server\r\n'
            h += 'Last-Modified: ' + time.ctime(os.path.getmtime(namefile)) +'\r\n'
            h += 'Content-Length: ' + str(self._content_length(namefile)) +'\r\n'
            h += 'Connection: close\r\n'
        elif(code == 404):
            h = 'HTTP/1.1 404 Not Found\r\n'
            h += 'Date: ' + current_date +'\r\n'
            h += 'Server: Simple-Python-HTTP-Server\r\n'
            #h += 'Content-Length: ' + str(self._content_length(namefile)) +'\r\n'
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
            h += 'Location: http://' + 'localhost' + ':' + str(5000) +'/' + namefile + '/' + '\r\n'
    
        return h
    	
    def extractor(self, strr):
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
    
    def readfile(self, dirc):
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
    
    def GET(self, data):
        source=data.split('?')
        try:
            parameter=self.extractor(source[1])
        except:
            parameter=0
        #print parameter
        status, files = self.readfile(source[0])
        resp= files.read(1000)
        header=self._gen_headers(status, source[0])
        return header+'\r\n'+resp
    
    def HEAD(self, data):
        status, response_content = self.readfile(data)
        resp = self._gen_headers(status, data)
        return resp
    
    def POST(self, data, source):
        parameter=self.extractor(source)
        #print parameter
        status, files = self.readfile(data)
        resp=files.read(1000)
        header=self._gen_headers(status, data)
        print parameter
        return header+'\r\n'+resp
    
    
    def requesthandler(self,data):
        try:
            if data[:4]=='POST':
                strr=data.split('\r\n\r\n')
                
                postsource=strr[1]
                strr=strr[0].split('\r\n')
                
            else:
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
                response=self.GET(dirc)
            elif cmd=='HEAD':
                response=self.HEAD(dirc)
            elif cmd=='POST':
                response=self.POST(dirc, postsource)
            return response
        except:
            response_header=self._gen_headers(500, '')
            f=open('page/500.html', 'rb')
            return response_header+'\r\n'+f.read(10000)
        
    def run(self):
        running = 1
        while running:
            
            data= self.client.recv(self.size)
            
            la=self.requesthandler(data)
            
            self.client.send(la)
            
            self.client.close()
            running = 0
if __name__ == "__main__":
    s = Server()
    s.run()