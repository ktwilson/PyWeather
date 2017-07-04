import datetime
import json
import math
from Logger import Logger

class VPBase():
    def __init__(self,serialdata):   
        self.serialdata = serialdata
        self.dataIndex = 0

    def getByte(self): 
        byte = self.serialdata[self.dataIndex]
        self.dataIndex+=1
        return byte

    def getDate(self):
        dtnum = self.getNumber()
        if dtnum == 65535 or dtnum == 0:
            return ''
        yrs = (dtnum & 0x7f) + 2000
        days = (dtnum & 0xf80) >> 7
        month = (dtnum & 0xf000) >> 12
        sdate = str(yrs) +  '-' + str(month) + '-' + str(days)
        return sdate    

    def getNumber(self):
        byte1 = self.getByte()
        byte2 = self.getByte()
        return byte2 * 256 + byte1

    def getTemperature(self): 
        temp1 = self.peek(0)
        temp2 = self.peek(1)
        temp = self.getNumber()
        if (temp2 == 255):
            temp = -(255 - temp1)

        try:
            temp = round(temp,2) / 10
        except Exception as e:
            Logger.error(e)
            
        return temp    
    

    def getTime(self):
        time = self.getNumber()
        if time < 65000:
            hrs = math.floor(time / 100)
            mins = math.floor((time / 100 - hrs) * 100)
        else:
            return ''

        dt = datetime.datetime.strptime(str(hrs) + ':' + str(mins), '%H:%M' )

        return dt.strftime('%I:%M %p')

    def peek(self,index):
        return self.serialdata[self.dataIndex + index]     
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)



