from socketIO_client import SocketIO, LoggingNamespace
from VPBase import VPBase
class WebSocket(object):   

    def on_connect(self):
        print('connect')
        #self.onConnect()

    def on_disconnect(self):
        print('socket disconnect')

    def on_reconnect(self):
        print('reconnect')

    def on_current(self,*args):
        print('on_current', args)

    def on_event(self):
        print ('on_event')

    def __init__(self, config):
        host = config['socketServer']
        port = config['webPort']
        print(host,port)
        self.socketIO = SocketIO(host,port)

        self.socketIO.on('connect', self.on_connect)
        self.socketIO.on('disconnect', self.on_disconnect)
        self.socketIO.on('reconnect', self.on_reconnect)
        self.socketIO.on('current', self.on_current)       

    def emit(self, event, data):
        if isinstance(data, VPBase):
            data = data.toJSON()
        self.socketIO.emit(event,data)
