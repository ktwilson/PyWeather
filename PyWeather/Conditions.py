from Constants import Constants 
from VPBase import VPBase
import math
import datetime

class Conditions(VPBase):
    
    def __init__(self, serialdata):    
        VPBase.__init__(self,serialdata)
        if serialdata == None:
            self.temperature = 75
            return
        
        self.dataIndex = 3
        if (self.serialdata[0] == 0x6):
            self.dataIndex+=1

        self.barometerTrend = self.getBarometerTrend()
        self.dataIndex+=3
        
        self.barometer = self.getBarometer()
        self.temperatureIn = self.getTemperature()
        self.humidityIn = self.getByte()
        self.temperature = self.getTemperature()
        self.windSpeed = self.getByte()
        self.windAvg = self.getByte()
        self.windDir = self.getNumber()
        self.windDirection = self.getWindDirection(self.windDir)

        self.dataIndex += 15
        self.humidity = self.getByte()
        self.dewpoint = self.getDewpoint()
        
        self.dataIndex +=7
        self.rainRate = self.getRain()
        self.dataIndex +=3

        self.stormRain = self.getRain()
        self.stormDate = self.getDate()
        self.dayRain = self.getRain()
        self.monthRain = self.getRain()
        self.yearRain = self.getRain()

        self.dataIndex +=30
        self.battery = self.getByte()
        self.voltage = self.getNumber()
        self.forecastIcon = self.getForecastIcon()
        self.forecastRule = self.getByte()
        self.sunrise = self.getTime()
        self.sunset = self.getTime()
        self.dateLoaded = str(datetime.datetime.now())

        self.serialdata = None


    def getBarometer(self):
        bar = self.getNumber() / 1000
        return round(bar,2)

    def getBarometerTrend(self):
        trend = self.getByte()       
        
        result = Constants.trends.get(trend);
        return result    

    def getDewpoint(self):
        dewPt = 0.0
        try:
            tem = -1.0 * self.temperature
            es = 6.112 * math.exp(-1.0 * 17.67 * tem / (243.5 - tem))
            ed = self.humidity / 100.0 * es
            eln = math.log(ed / 6.112)
            dewPt = -243.5 * eln / (eln - 17.67) 
        except Exception as e:
            self.logError(e)
            return 0.0

        return round(dewPt * 100) / 100

    def getForecastIcon(self):        
        fcastnum = self.getByte()
        return Constants.forecasts.get(fcastnum)   

    def getRain(self): 
        rain = self.getNumber()
        if rain == 65535:
            rain = 0

        return round(rain,2) / 100
    
    def getWindDirection(self,degrees):
        
        dirindx = round(degrees / 360 * 16)

        if dirindx < len(Constants.directions):
            return Constants.directions[dirindx]
        else:
            return ''    

    

        





