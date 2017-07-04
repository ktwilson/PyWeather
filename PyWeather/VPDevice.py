import serial
import datetime
import time
import sys
from Conditions import Conditions
from Logger import Logger
from VPBase import VPBase
from VPCRC import VPCRC
from VPHiLow import VPHiLow

class VPDevice(VPBase):
    def __init__(self, comPort):
        self.comPort = comPort
        self.isBusy = False
        self.lastActv = None

        try:
            self.port = serial.Serial(port=self.comPort,
                            baudrate=19200,
                            timeout=20,
                            parity=serial.PARITY_NONE,
                            bytesize=serial.EIGHTBITS,
                            stopbits=serial.STOPBITS_ONE)            
        except Exception as e:
            Logger.error(e)
            time.sleep(5)
            sys.exit()
             

    def getCurrent(self):            
        cmd = b'LOOP 1\n'
        current = None      

        try:        
            self.port.write(cmd)
            self.lastActv = datetime.datetime.now()       
        
            data = self.read(100)
            if len(data) != 100:
                return None
            data = bytearray(data)            

            if data[0] == 0x06:
                data.pop(0)
       
            if VPCRC.validate(data):
                current = Conditions(data)    
        except Exception as e:
            Logger.error(e)
            
        return current  

    def getHiLows(self):
        cmd = b'HILOWS\n'
        hilow = None

        try:           
            self.port.write(cmd)          
            self.lastActv = datetime.datetime.now()
            data = self.read(439)
            data = bytearray(data)
            if data[0] == 0x06:
                data.pop(0)
     
            if VPCRC.validate(data):
                hilow = VPHiLow(data)

        except Exception as e:
            Logger.error(e)

        return hilow
        

    def read(self,numbytes):
        data = self.port.read(size=numbytes)
        self.lastActv = datetime.datetime.now()
        return data   


    def wakeUp(self):
        try:            
            if self.lastActv != None:
                dtDiff = datetime.datetime.now() - self.lastActv
                if dtDiff.seconds < 10:
                    return True
                
            self.port.write(b'\n')
            attempts = 3
            while(attempts > 0):
                if self.port.in_waiting == 2:
                    break
                else:
                    time.sleep(1)

            ack = self.read(2)
            ackd = ack == b'\n\r'
            if ackd:
                self.lastActv = datetime.datetime.now()

        except Exception as e:
            Logger.error(e)
            ackd = False
        return ackd
