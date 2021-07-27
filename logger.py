import logging
import sys
import datetime

def Logger(label, filename='log.log'):
    filename='logs/%s-%s' % (datetime.datetime.now().strftime('%Y-%m-%d'), filename)
    FORMAT = '[%(asctime)-15s] [%(levelname)s]:%(name)s:%(filename)s msg=%(message)s'
    
    logger = logging.getLogger(label)

    fileHandler = logging.FileHandler(filename)
    fileHandler.setFormatter(logging.Formatter(FORMAT))
    
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(logging.Formatter(FORMAT))

    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)
    logger.setLevel(logging.INFO)
    return logger