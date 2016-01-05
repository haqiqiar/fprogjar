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
            
def _gen_headers(code, namefile):
    h=''
    
    current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())

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
        h += 'Content-Length: ' + str(_content_length(namefile)) +'\r\n'
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
        h += 'Location: http://' + server_address[0] + ':' + str(server_address[1]) + namefile + '/' + '\r\n'

    print h

_gen_headers(500, namefile)
