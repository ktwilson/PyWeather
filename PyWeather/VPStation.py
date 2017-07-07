import datetime
import time
from Logger import Logger
from VPBase import VPBase
from VPDevice import VPDevice
from ExternalSite import ExternalSite
from threading import Thread
from Event import Event

class VPStation(VPBase):   

    def getHiLows(self):
        try:
            self.hiLows = self.device.getHiLows()
            if self.hiLows != None:                
                self.hiLows.forecast = self.externSite.getForecast()           
                self.externSite.updateWSocket(self.hiLows,'hilows')
                Logger.info('hi temp:' + str(self.hiLows.temperature.dailyHi))
            
            self.dtHiLow = datetime.datetime.now()
            
            self.alerts = self.externSite.getAlerts()
            #self.externSite.updateWSocket(self.alerts,'alerts')
           
        except Exception as e:
            Logger.error(e)
        finally:
            self.isBusy = False

    def getCurrent(self):      
       
        try:
            if (self.device.wakeUp()):
                self.current = self.device.getCurrent()
                if self.current != None:
                    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\t' + 'temp:' + str(self.current.temperature))  
                    thrd = Thread(target=self.updateSite,args=())
                    thrd.start()
                    
            else:
                Logger.warning('unable to wake ws')

        except Exception as e:
            Logger.error(e)
        finally:
            self.isBusy = False

    def __init__(self, config):      
        self.device = VPDevice(config['serialPort'])
        self.updateFreq = config['updateFrequency']
        self.config = config
        self.isRunning = False
        self.dtHiLow = datetime.datetime.now()  
        self.current = None
        self.hiLows = None
        self.externSite = ExternalSite(self.config) 
        self.alerts = []
        self.isBusy = False
        self.thrd = None        
        self.onEvent = Event()

    def start(self):
        self.isRunning = True

        while self.isRunning:
            self.waitAvail(20)       
            dtDiff = datetime.datetime.now() - self.dtHiLow
            if (dtDiff.seconds > 1800 or self.hiLows == None):
                self.getHiLows()

            self.getCurrent()           
            
            time.sleep(self.updateFreq)

    def stop(self):
        self.isRunning = False    

    def updateSite(self): 
        self.externSite.update(self.current)

    def waitAvail(self,secs):       
        while self.isBusy and secs != 0:
            secs-=1
            print('waiting on device availability')
            time.sleep(1)

        self.isBusy = True   

        

            