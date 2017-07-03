import logging
import datetime
import traceback

class Logger(object): 
        
    def info(msg):
        msg = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +  '\t' + msg
        logging.info(msg)
        print(msg)

    def error(err):
        err = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\t' + str(err)
        logging.error(err)    
        print(err)

    def warning(msg):
        msg = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\t' + str(msg)
        logging.warning(msg)
        print(msg)



