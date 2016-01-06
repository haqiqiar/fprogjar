from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os

class simpleHTTPRequestHandler(BaseHTTPRequestHandler):

        #handle GET command
        def do_GET(self):
                rootdir = 'c:/xampp/htdocs/' #lokasi file
                try:
                        if self.path.endswith('.html'):
                                f = open(rootdir + self.path) #membuka file
                                self.send_response(200, 'OK')

                                self.send_header('Content-type','text-html')
                                self.end_headers()

                                self.wfile.write(f.read())
                                f.close()
                                return

                except IOError:
                        self.send_error(404, 'Not Found')

def run():
print('http server is starting...')

server_address = ('127.0.0.1', 80)
httpd = HTTPServer(server_address, simpleHTTPRequestHandler)
print('http server is running...')
httpd.serve_forever()

if __name__ == '__main__':
    run()
