import socket
import sys

# create socket and connect to server
server_address = ('localhost', 8080)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)
# send string to server and close socket
message = sys.stdin.readline()
client_socket.send(message)
resp=client_socket.recv(1024)
print resp 
client_socket.close()