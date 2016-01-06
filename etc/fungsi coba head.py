try:
                 file_handler = open(file_requested,'rb')
                 if (request_method == 'HEAD'):  #only read the file when GET
                     response_content = file_handler.read() # read file content
                 file_handler.close()

                 response_headers = self._gen_headers( 200)

             except Exception as e: #in case file was not found, generate 404 page
                 print ("Warning, file not found. Serving response code 404\n", e)
                 response_headers = self._gen_headers( 404)

                 if (request_method == 'HEAD'):
                    response_content = b"<html><body><p>Error 404: File not found</p><p>Python HTTP server</p></body></html>"

             server_response =  response_headers.encode() # return headers for GET and HEAD
             if (request_method == 'HEAD'):
                 server_response +=  response_content  

             conn.send(server_response)
             print ("Closing connection with client")
             conn.close()

         else:
             print("Unknown HTTP request method:", request_method)