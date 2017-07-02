class WeatherAlert(object):
    def __init__(self, alert):         
        self.description = alert['description']
        self.expires = alert['expires']
        self.phenomena = alert['phenomena']
        self.date = alert['date']
        self.significance = alert['significance']
        self.message = alert['message']
        self.type = alert['type']

