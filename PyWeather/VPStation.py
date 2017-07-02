import datetime
import httplib2
import threading
from Logger import Logger
from VPBase import VPBase
from VPDevice import VPDevice
from ExternalSite import ExternalSite
from WebSocket import WebSocket

class VPStation(VPBase):   

    def getHiLows(self):
        self.hiLows = self.device.getHiLows()
        if self.hiLows != None:
            self.dtHiLow = datetime.datetime.now()          
            self.hiLows.forecast = self.externSite.getForecast()
            self.externSite.updateHiLows(self.hiLows)
            self.webSocket.emit('hilows', self.hiLows)
              
        self.alerts = self.externSite.getAlerts()
        if len(self.alerts) > 0:
            self.externSite.updateLocal(self.alerts,'alerts')

        self.start()

    def getCurrent(self):      
       
        if (self.device.wakeUp()):
            self.current = self.device.getCurrent()
            if self.current != None:
                print(self.current.temperature)
                self.externSite.update(self.current)
                self.webSocket.emit('current',self.current)
        else:
            Logger.warning('unable to wake ws')

        if self.stopped == False:            
           self.start()

    def __init__(self, config):      
        self.device = VPDevice(config['serialPort'])
        self.updateFreq = config['updateFrequency'] * 1000
        self.config = config
        self.stopped = False
        self.dtHiLow = datetime.datetime.now()     
        self.hiLows = None
        self.externSite = ExternalSite(self.config)   
        self.webSocket = WebSocket(self.config)

    def start(self):
        dtDiff = datetime.datetime.now() - self.dtHiLow
        if (dtDiff.seconds > 3600 or self.hiLows == None):
            self.tmr = threading.Timer(1,self.getHiLows)
        else:
            self.tmr = threading.Timer(5,self.getCurrent)
        
        self.tmr.start()

    def stop(self):
        self.stopped = True
        self.tmr.cancel()
       

        

            