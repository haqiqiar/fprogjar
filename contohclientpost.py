__author__ = 'zq'

import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("localhost",5000))


s.send("POST GET/index.html HTTP/1.1\r\nHost: 127.0.0.1:8000\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nUser=Peter%2BLee&pw=123456&action=login\r\n\r\n")
content = ""
while True:
        resp = s.recv(1024)
        if resp == "": break
        #print resp
        content += resp
        #file.write(resp)

s.close()
<<<<<<< HEAD

print "Content : " + content
temporarySplit = content.split('\r\n\r\n')
responseHeader = temporarySplit[0]
response=temporarySplit[1]
#print responseHeader
#print response
=======
print content
#print "Content : " + content
temporarySplit = content.split('\r\n\r\n')
responseHeader = temporarySplit[0]

#print responseHeader
>>>>>>> cf190ff6917b95f031dabf77a165f0516e610142
