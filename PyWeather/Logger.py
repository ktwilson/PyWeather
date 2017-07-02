import logging
import datetime
import traceback

class Logger(object): 
        
    def info(msg):
        logging.info(str(datetime.datetime.now()) + '\t' + msg)
        print(msg)

    def error(err):
        logging.error(str(datetime.datetime.now()) + '\t' + str(err))        

    def warning(err):
        logging.warning(str(datetime.datetime.now()) + '\t' + str(err))
        print(err)



