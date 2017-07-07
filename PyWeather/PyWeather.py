import datetime
import json
import logging
import sys
import time
from VPStation import VPStation
from Logger import Logger
from threading import Thread
from Event import Event
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from Conditions import Conditions
 
class PyWeather(object):   

    def __init__(self):     

        try:          
            cf = open('config.json', 'r')
            configstr = cf.read()
            cf.close()
            config = json.loads(configstr)   
            self.config = config
            daynum = str(datetime.datetime.now().day)
            logging.basicConfig(filename=config['logFilePath'] + 'pyWeather' + daynum + '.log', level=logging.INFO)            

        except KeyboardInterrupt:
            print('^C received')
            ws.stop()    
            time.sleep(5)
   
        except Exception as e:
            ws.stop()    
            Logger.error(e)
            time.sleep(5)

    def start(self):
        Logger.info('starting')        
        
        self.vpstation = VPStation(self.config)
         
        self.vpThrd = Thread(target=self.vpstation.start, args=())
        self.vpThrd.start()
        
        self.isServing = True
        self.startWebServer()
      
    def stop(self):
        self.vpstation.stop()
        time.sleep(5)
        self.vpThrd.cancel()
        self.isServing = False   
    
    def startWebServer(self):
        port = self.config['webPort']
        self.server = HTTPServer(('',port),PyWeather.makeHandlerClass(self.vpstation))
        
        print('server port ' + str(port))
        while self.isServing:
            self.server.handle_request()

    def makeHandlerClass(vpstation):
        class RequestHandler(BaseHTTPRequestHandler, object):
            def __init__(self, *args, **kwargs):
                 self.vpstation = vpstation
                 super(RequestHandler, self).__init__(*args, **kwargs)

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

        return RequestHandler
     
        

        


