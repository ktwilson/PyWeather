import inspect
class HiLow(object):
    def __init__(self):     
        self.hourlyHi = 0.0
        self.dailyLo = 0.0
        self.dailyHi = 0.0
        self.monthLo = 0.0
        self.monthHi = 0.0
        self.yearLo = 0.0
        self.yearHi = 0.0
        self.dailyLoTime = 0.0
        self.dailyHiTime = 0.0

    def props(self):
        pr = {}
        for name in dir(self):
            value = getattr(self, name)
            if not name.startswith('__') and not inspect.ismethod(value):
                pr[name] = value
        return pr



