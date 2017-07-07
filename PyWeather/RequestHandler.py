import json
from http.server import BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):  

    def do_HEAD(self,contentType):        
        self.send_response(200)
        self.send_header('Content-type', contentType)
        self.end_headers()

    def do_GET(self):
        global vpstation
        req = self.path[1:]
        if req == 'current':
            self.do_HEAD('application/json')
            self.wfile.write(bytes(self.vpstation.current.toJSON(),'utf-8'))
        elif req == 'hilows':
                self.do_HEAD('application/json')
                self.wfile.write(json.dumps(self.vpstation.hilows))
        elif req == 'alerts':
                self.do_HEAD('application/json')
                self.wfile.write(json.dumps(self.vpstation.alerts))
        else:
            self.do_HEAD('text/html')
            self.send_response(404)

    def do_POST(self):
        cmd = self.path[1:]
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self.do_HEAD('application/json')
		#self.wfile.write(json.dumps(retval))