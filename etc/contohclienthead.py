__author__ = 'zq'

import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("localhost",5000))



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
=======
print content
#print "Content : " + content
>>>>>>> cf190ff6917b95f031dabf77a165f0516e610142
temporarySplit = content.split('\r\n\r\n')
responseHeader = temporarySplit[0]

#print responseHeader
