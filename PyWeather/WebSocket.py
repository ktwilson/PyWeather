from socketIO_client import SocketIO
class WebSocket(object):
    def on_connect(self):
        print('connect')

    def on_disconnect(self):
        print('disconnect')

    def on_reconnect(self):
        print('reconnect')

    def on_current(self,*args):
        print('on_current', args)

    def __init__(self, config):
        self.socketIO = SocketIO(config['socketServer'], config['webPort'])
        self.socketIO.on('connect', self.on_connect)
        self.socketIO.on('disconnect', self.on_disconnect)
        self.socketIO.on('reconnect', self.on_reconnect)
        self.socketIO.on('current', self.on_current)    

    def emit(self, event, data):
        self.socketIO.emit(event,data.toJSON())