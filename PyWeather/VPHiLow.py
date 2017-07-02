from VPBase import VPBase
from HiLow import HiLow

class VPHiLow(VPBase):
    def __init__(self,serialdata):  
        VPBase.__init__(self,serialdata)     

        if (self.serialdata[0] == 0x6):
            self.dataIndex+=1

        self.barometer = self.getBarometer()
        self.windSpeed = self.getWindSpeed()
        self.inTemperature = self.getHiLoTemp(False)
        self.inHumidity = self.getHumidity(False)
        self.temperature = self.getHiLoTemp(True)
        self.dewpoint = self.getDewpoint()
        self.windChill = self.getWindChill()
        self.heatIndex = self.getHeatIndex()
        self.thswIndex = self.getHeatIndex()
        self.radiation = self.getHeatIndex()
        self.uvHigh = self.getUVHigh()

        self.rainHigh = self.getRain() 

        self.dataIndex += 150                       #extra/leaf/soil

        self.humidity = self.getHumidity(True)  

        self.serialdata = None

    def getBarometer(self):
        hilo = HiLow()
        hilo.dailyLo = round(self.getNumber() / 1000,2)
        hilo.dailyHi = round(self.getNumber() / 1000,2)
        hilo.monthLo = round(self.getNumber() / 1000,2)
        hilo.monthHi = round(self.getNumber() / 1000,2)
        hilo.yearLo = round(self.getNumber() / 1000,2)
        hilo.yearHi = round(self.getNumber() / 1000,2)
        hilo.dailyLoTime = self.getTime()
        hilo.dailyHiTime = self.getTime()
        return hilo   

    def getDewpoint(self):
        hilo = HiLow()
        hilo.dailyLo = self.getNumber()
        hilo.dailyHi = self.getNumber()
        hilo.dailyLoTime = self.getTime()
        hilo.dailyHiTime = self.getTime()
        hilo.monthHi = self.getNumber()
        hilo.monthLo = self.getNumber()
        hilo.yearHi = self.getNumber()
        hilo.yearLo = self.getNumber()
        return hilo

    def getHiLoTemp(self,outside):
        hilo = HiLow()
        dailyHi = self.getTemperature()
        dailyLo = self.getTemperature()
        dailyHiTime = self.getTime()
        dailyLoTime = self.getTime()
        monthLo = self.getTemperature()
        monthHi = self.getTemperature()
        yearLo = self.getTemperature()
        yearHi = self.getTemperature()

        hilo.dailyLo = dailyHi if outside else dailyLo
        hilo.dailyHi = dailyLo if outside else dailyHi

        hilo.dailyHiTime = dailyLoTime if outside else dailyHiTime
        hilo.dailyLoTime = dailyHiTime if outside else dailyLoTime
        hilo.monthHi = monthLo if outside else monthHi
        hilo.monthLo = monthHi if outside else monthLo
        hilo.yearHi = yearLo if outside else yearHi
        hilo.yearLo = monthHi if outside else yearLo

        return hilo

    def getHeatIndex(self):
        hi = HiLow()
        hi.dailyHi = self.getNumber()
        hi.dailyHiTime = self.getTime()
        hi.monthHi = self.getNumber()
        hi.yearHi = self.getNumber()
        return hi

    def getHumidity(self,outside):
        hilo = HiLow()

        if (outside == False):
            hilo.dailyHi = self.getByte()
            hilo.dailyLow = self.getByte()

            hilo.dailyHighTime = self.getTime()
            hilo.dailyLowTime = self.getTime()

            hilo.monthHi = self.getByte()
            hilo.monthLow = self.getByte()

            hilo.yearHi = self.getByte()
            hilo.yearLow = self.getByte()        
        else:
            hilo.dailyLow = self.getByte()
            self.dataIndex += 7
            hilo.dailyHi = self.getByte()
            self.dataIndex += 7

            hilo.dailyLowTime = self.getTime()
            self.dataIndex += 14
            hilo.dailyHighTime = self.getTime()
            self.dataIndex += 14
            
            hilo.monthHi = self.getByte()
            self.dataIndex += 7
            hilo.monthLow = self.getByte()
            self.dataIndex += 7

            hilo.yearHi = self.getByte()
            self.dataIndex += 7
            hilo.yearLow = self.getByte()
            self.dataIndex += 7
        
        return hilo

    def getRain(self):
        hi = HiLow()
        hi.dailyHi = self.getNumber() / 100
        hi.dailyHiTime = self.getTime()
        hi.hourlyHi = self.getNumber() / 100
        hi.monthHi = self.getNumber() / 100
        hi.yearHi = self.getNumber() / 100
        return hi

    def getUVHigh(self):
        hi = HiLow()
        hi.dailyHi = self.getByte()
        hi.dailyHiTime = self.getTime()
        hi.monthHi = self.getByte()
        hi.yearHi = self.getByte()
        return hi

    def getWindChill(self):
        lo = HiLow()
        lo.dailyLo = self.getNumber()
        lo.dailyLoTime = self.getTime()
        lo.monthLo = self.getNumber()       
        lo.yearLo = self.getNumber()
        return lo

    def getWindSpeed(self):
        hilo = HiLow()
        hilo.dailyHi = self.getByte()
        hilo.dailyHiTime = self.getTime()
        hilo.monthHi = self.getByte()
        hilo.yearHi = self.getByte()
        return hilo   

    def props(self):
        pr = {}
        for name in dir(self):
            value = getattr(self, name)
            if not name.startswith('__') and not inspect.ismethod(value):
                pr[name] = value
        return pr
     


