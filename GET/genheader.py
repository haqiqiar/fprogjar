import os.path
import socket
import signal
import sys
import time 

server_address = ('localhost', 8080)

#server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#server_socket.bind(server_address)
#server_socket.listen(5)

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
    
    current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())

    if (code != 301):
            lastmodified = time.ctime(os.path.getmtime(namefile))
            if (code == 200):
                h = 'HTTP/1.1 200 OK\n'
                h += 'Date: ' + current_date +'\n'
                h += 'Server: Simple-Python-HTTP-Server\n'
                h += 'Last-Modified: ' + lastmodified +'\n'
                h += 'Content-Length: ' + str(_content_length(namefile)) +'\n'
                h += 'Connection: close'
            elif(code == 404):
                h = 'HTTP/1.1 404 Not Found\n'
                h += 'Date: ' + current_date +'\n'
                h += 'Server: Simple-Python-HTTP-Server\n'
                h += 'Content-Length: ' + str(_content_length(namefile)) +'\n'
                h += 'Connection: close'
            elif(code == 403):
                h = 'HTTP/1.1 403 Forbidden\n'
                h += 'Date: ' + current_date +'\n'
                h += 'Server: Simple-Python-HTTP-Server\n'
                h += 'Connection: Keep-Alive'
            elif(code == 400):
                h = 'HTTP/1.1 400 Bad Request\n'
                h += 'Date: ' + current_date +'\n'
                h += 'Server: Simple-Python-HTTP-Server\n'
                h += 'Content-Length: ' + str(_content_length(namefile)) +'\n'
                h += 'Connection: close'
    else:
        if(code == 301):
            h = 'HTTP/1.1 301 Moved Permanently\n'
            h += 'Date: ' + current_date +'\n'
            h += 'Server: Simple-Python-HTTP-Server\n'
            h += 'Location: http://' + server_address[0] + ':' + str(server_address[1]) + namefile + '/'

    print h

_gen_headers(400)
