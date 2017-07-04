import datetime
import json
import logging
import sys
import time
from VPStation import VPStation
from Logger import Logger
from threading import Thread

global ws,thrd
try:
    cf = open('config.json', 'r')
    configstr = cf.read()
    cf.close()
    config = json.loads(configstr)    
    daynum = str(datetime.datetime.now().day)
    logging.basicConfig(filename=config['logFilePath'] + 'pyWeather' + daynum + '.log', level=logging.INFO)
    Logger.info('starting')
    
    ws = VPStation(config)
    thrd = Thread(target=ws.start, args=())
    thrd.start()
    time.sleep(1)

    while thrd.isAlive():
        time.sleep(1)        
    
    Logger.info('terminated at ' + datetime.datetime.now().ctime())
    sys.exit()

except KeyboardInterrupt:
    print('^C received')
    ws.stop()    
    time.sleep(5)
   
except Exception as e:
    ws.stop()    
    Logger.error(e)
    time.sleep(5)


