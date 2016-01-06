__author__ = 'zq'

import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect(("localhost",5000))

get="GET /page/index.html?q=5 HTTP/1.0\r\nHost: localhost:5000\r\n\r\n"; s.send(get)
#head="HEAD /page/index.html HTTP/1.0\r\nHost: localhost:5000\r\n\r\n"; s.send(head)
#post="POST /page/index.html HTTP/1.1\r\nHost: 127.0.0.1:8000\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nUser=Peter%2BLee&pw=123456&action=login\r\n\r\n"; s.send(post)
#get404="GET /page/andex.html HTTP/1.0\r\nHost: localhost:5000\r\n\r\n"; s.send(get404)
#get301="GET /page HTTP/1.0\r\nHost: localhost:5000\r\n\r\n"; s.send(get301)
#get500="\r\nHost: localhost:5000\r\n\r\n"; s.send(get500)
#get403="GET /page/500.html HTTP/1.0\r\nHost: localhost:5000\r\n\r\n"; s.send(get403)

content = ""

while True:
        resp = s.recv(1024)
        if resp == "": break
        
        content += resp
        

s.close()

#print content
try:
        temporarySplit = content.split('\r\n\r\n')
        responseHeader = temporarySplit[0]
        print responseHeader
        response=temporarySplit[1]
        print
        word=response.split('<h1>')
        word=word[1].split('</h1>')
        print word[0]
except:
        print ''

