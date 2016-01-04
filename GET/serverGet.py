import socket
import sys
import time

def GET(uri,http):
    message=""
    date= 'Date: '+time.strftime("%a, %d %b %Y %H:%M:%S")+'\r\n'
    server='Server: '++'\r\n'
    lastModified='Last Modified: '++'\r\n'    
    contentLength='Content-Length: '++'\r\n'
    contentType='Content-Type:'+'text/html\r\n'
    if :
        statusCode= "HTTP/1.1 200 OK\r\n" #status 200 ok
        eTag='ETag: '++'\r\n'
        acceptRanges= 'Accept-Ranges: '++'\r\n'
        connection='Connection: close \r\n'
        content='\r\n'++'\r\n'
        
        message=statusCode+date+server+lastModified+eTag+acceptRanges+contentLength+connection+contentType+content
    elif :
        statusCode="HTTP/1.1 301 Move Permanently\r\n" #status 301 Move Permanently
        location='Location: '++'\r\n'
        content='\r\n'++'\r\n'
        
        message=statusCode+date+server+location+contentLength+contentType+content
    elif :
        statusCode="HTTP/1.1 403 Forbidden\r\n" #status 403 Forbidden
        keepAlive='Keep-Alive: '+'timeout='+timeout+', max='+max+'\r\n'
        connection='Connection: Keep-Alive\r\n'
        content='\r\n'++'\r\n'
        
        message=statusCode+date+server+contentLength+keepAlive+connection+contentType+content
    elif :
        statusCode="HTTP/1.1 404 Not Found\r\n" #status 404 Not Found
        connection='Connection: close\r\n'
        content='\r\n'++'\r\n'
        
        message=statusCode+date+server+connection+contentType+content
    elif :
        statusCode="HTTP/1.1 500 Internal Server Error\r\n" #status 500 Internal Server Error
        
        message=statusCode
    
    
    return message
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
        response=data.split(' ')
        http_response = GET(response[1],response[2])#"""\
#HTTP/1.1 200 OK

#Hello, World!
#"""
        client_socket.sendall(http_response)
        # close socket client
        client_socket.close()        

# if user press ctrl + c, close socket client and exit    
except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)