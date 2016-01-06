import os.path
import socket
import signal
import time
import genheader

server_address = ('localhost', 8080)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

if string[0:4] == 'HEAD':
         if (request_method == 'HEAD'):
             #file_requested = string[5:]

             # split on space "GET /file.html" -into-> ('GET','file.html',...)
             file_requested = string.split(' ')
             file_requested = file_requested[1] # get 2nd element

             #Check for URL arguments. Disregard them
             file_requested = file_requested.split('?')[0]  # disregard anything after '?'

             if (file_requested == '/'):  # in case no file is specified by the browser
                 file_requested = '/index.html' # load index.html by default

             file_requested = self.www_dir + file_requested
             print ("Serving web page [",file_requested,"]")

             ## Load file content
             try:
                 file_handler = open(file_requested,'rb')
                 if (request_method == 'HEAD'):  #only read the file when HEAD
                     response_content = file_handler.read() # read file content
                 file_handler.close()

                 response_headers = self._gen_headers( 200)

             except Exception as e: #in case file was not found, generate 404 page
                 print ("Warning, file not found. Serving response code 404\n", e)
                 response_headers = self._gen_headers( 404)

                 if (request_method == 'HEAD'):
                    response_content = b"<html><body><p>Error 404: File not found</p><p>Python HTTP server</p></body></html>"

             server_response =  response_headers.encode() # return headers for GET and HEAD
             if (request_method == 'GET'):
                 server_response +=  response_content  # return additional conten for GET only