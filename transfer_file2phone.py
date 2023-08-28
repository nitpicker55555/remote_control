import http.server
import socketserver
import socket
import os
import base64
def get_lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
print(get_lan_ip())
import http.server
import socketserver
import os

PORT = 8000
DIRECTORY = r"C:\Users\Morning\Downloads\bdfdc356_nagisa-29\nagisa-29\ccc"

os.chdir(DIRECTORY)

class AuthHandler(http.server.SimpleHTTPRequestHandler):
    # Replace 'user' and 'pass' with your username and password
    key = base64.b64encode(b'user:pass').decode()

    def do_HEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Restricted\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.headers.get('Authorization') == None:
            self.do_HEAD()
            self.wfile.write(b'No auth header received')
        elif self.headers.get('Authorization') == 'Basic ' + self.key:
            http.server.SimpleHTTPRequestHandler.do_GET(self)
        else:
            self.do_HEAD()
            self.wfile.write(b'Not authenticated')

with socketserver.TCPServer(("0.0.0.0", PORT), AuthHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()