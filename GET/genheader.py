import os.path
import socket
import signal
import time 

namefile='index.html'

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
            
def _gen_headers(code):
    h=''
    
    if (code == 200):
        h = 'HTTP/1.1 200 OK\n'
    elif(code == 404):
        h = 'HTTP/1.1 404 Not Found\n'
    elif(code == 301):
        h = 'HTTP/1.1 301 Moved Permanently\n'
    elif(code == 403):
        h = 'HTTP/1.1 403 Forbidden\n'
    elif(code == 400):
        h = 'HTTP/1.1 403 Forbidden\n'

    current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())

    lastmodified = time.ctime(os.path.getmtime(namefile))
    
    h += 'Date: ' + current_date +'\n'
    h += 'Server: Simple-Python-HTTP-Server\n'
    h += 'Last-Modified: ' + lastmodified +'\n'
    h += 'Content-Length: ' + str(_content_length(namefile)) +'\n'
    h += 'Connection: close'

    print h

_gen_headers(200)
