from Logger import Logger
from WeatherAlert import WeatherAlert
import datetime
import json
import httplib2
import VPBase

class ExternalSite(object):
    def __init__(self, config):         
        self.config = config;

    def getAlerts(self):
        wualerts = []
        cityState = self.config['wuCityState'].split(',')

        if len(cityState) != 2:
            return

        city = cityState[0];
        state = cityState[1];
        token = self.config['wuToken'];
        url = self.config['wuAlertUrl'].format(token,state,city)

        alertjs = self.getWebData(url)      
        if alertjs != None:
            for alert in alertjs['alerts']:
                wualerts.append(WeatherAlert(alert))

        return wualerts

    def getForecast(self):
        forecast = dict()
        forecast['periods'] = []

        token = self.config['wuToken']
        cityState = self.config['wuCityState'].split(',')
        city = cityState[0]
        state = cityState[1]
        url = self.config['forecastUrl'].format(token,state,city)

        wforecast = self.getWebData(url)
        if wforecast != None:
            periods = wforecast['forecast']['txt_forecast']['forecastday']               
            forecast['last'] = datetime.datetime.now().ctime()                
            for period in periods:
                forecast['periods'].append(period)        

        return forecast

    def getWebData(self,url):
        dictobj = None

        try:
            http = httplib2.Http()           
            resp, respdata = http.request('http://' + url, "GET")
            if type(respdata) is bytes:                
                respdata = respdata.decode('utf-8')              

            if (resp.status != 200):
                respdata = None
                Logger.warning('getWebData ' + str(resp.status))     
            else:                
                dictobj = json.loads(respdata)
        except Exception as e:          
            Logger.error(e)

        return dictobj
    
    def update(self,current):
        self.current = current;
        self.updateWU(current)        

    def updateWU(self,current):
        respdata = None
        wuHost = self.config['uploadHost']
        wuUser = self.config['wuUserID']
        wuPswd = self.config['wuPassword']
        dtUtc = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S').replace(' ','%20')
        c = current
        rtFreq = self.config['updateFrequency']
        wuPath = self.config['uploadPath'].format(wuUser,wuPswd,dtUtc,c.windDir,c.windAvg,c.windSpeed,c.temperature,c.rainRate,c.dayRain,c.barometer,c.humidity,c.dewpoint,rtFreq)

        try:
            h = httplib2.Http()           
            resp, respdata = h.request('http://' + wuHost + wuPath, "GET")

            if (resp.status != 200):
                respdata = None
                Logger.error('updateWU ' + str(resp.status))            
                
        except Exception as e:          
            Logger.error(e)

        return respdata	




