import socket
import sys

# define server address, create socket, bind, and listen
server_address = ('localhost', 8080)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)
print 'Serving HTTP on port %s ...' % server_address[1]
# infinite loop accepting client
try:
    while True:
        client_socket, client_address = server_socket.accept()
        #print client_socket, client_address
        
        # receive data from client and print
        data = client_socket.recv(1024)
        print data
        http_response = """\
HTTP/1.1 200 OK

Hello, World!
"""
        client_socket.sendall(http_response)
        # close socket client
        client_socket.close()        

# if user press ctrl + c, close socket client and exit    
except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)