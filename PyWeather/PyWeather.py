
from VPStation import VPStation
from Logger import Logger
import datetime
import json
import logging
import io
import sys
import time

global isactive,ws

try:
    file = open('config.json','r')
    configstr = file.read()
    file.close()
    config = json.loads(configstr)    
    daynum = str(datetime.datetime.now().day)
    logging.basicConfig(filename=config['logFilePath'] + 'pyWeather' + daynum + '.log', level=logging.INFO)
    
    isactive = True
    ws = VPStation(config)
    ws.start()
    Logger.info('started at ' + datetime.datetime.now().ctime())

    while(isactive):
         time.sleep(1)

    Logger.info('terminated at ' + datetime.datetime.now().ctime())
    sys.exit()

except KeyboardInterrupt:
    print('^C received')
    ws.stop()
    isactive = False
    time.sleep(5)
   
except Exception as e:
    ws.stop()
    isactive = False
    Logger.error(e)
    time.sleep(5)


