#!/usr/bin/env python

import logging
from logging import handlers
import os

LOG_SIZE = 1000000
LOG_NUM_BACKUP = 4
LOG_LEVEL = logging.DEBUG

class ScrobbeeLogger():
    def __init__(self):
        self.logger = logging.getLogger('scrobbee')
        self.logger.setLevel(logging.DEBUG)
    
    def initLogging(self, log_path, quiet = False):
        self.log_path = log_path
        
        self.logger = logging.getLogger('scrobbee')
        self.logger.setLevel(logging.DEBUG)
        
        if not os.access(log_path, os.W_OK):
            try:
                os.makedirs(log_path, mode=0755)
            except OSError:
                raise SystemExit("Log dir doesn't exist and can't be created '" + scrobbee.DATA_DIR + "'")
        
        self.log_file = os.path.join(log_path, 'Scrobbee.log')
        self.quiet = quiet
        
        rotFileHandler = handlers.RotatingFileHandler(self.log_file, 'a', LOG_SIZE, LOG_NUM_BACKUP)
        rotFileHandler.setLevel(logging.DEBUG)
        rotFileHandler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-5s %(message)s', '%b-%d %H:%M:%S'))
        self.logger.addHandler(rotFileHandler)
        
        if not self.quiet:
            consoleHandler = logging.StreamHandler()
            consoleHandler.setLevel(logging.DEBUG)
            consoleHandler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-5s %(message)s', '%b-%d %H:%M:%S'))
            self.logger.addHandler(consoleHandler)
        
    def log(self, message, logLevel, context = ''):
        scrobbee_logger = self.logger
        
        if not context is '':
            message = '[' + context.rjust(25) + ']  ' + message
        
        if logLevel == logging.DEBUG:
            scrobbee_logger.debug(message)
        elif logLevel == logging.INFO:
            scrobbee_logger.info(message)
        elif logLevel == logging.WARNING:
            scrobbee_logger.warning(message)
        elif logLevel == logging.ERROR:
            scrobbee_logger.error(message)

scrobbee_log_instance = ScrobbeeLogger()
logger = logging.getLogger('scrobbee')

def log(message, logLevel=logging.INFO):
    scrobbee_log_instance.log(message, logLevel)
    
def debug(message, context=''):
    scrobbee_log_instance.log(message, logging.DEBUG, context)
    
def info(message):
    scrobbee_log_instance.log(message, logging.INFO)
    
def warning(message):
    scrobbee_log_instance.log(message, logging.WARNING)
    
def error(message):
    scrobbee_log_instance.log(message, logging.ERROR)
    
def changeHandlers(logger_name, log_file, quiet = True, enabled = False):
    logger_temp = logging.getLogger(str(logger_name))
    formatter_temp = logger_temp.__format__
    
    for handler in logger_temp.handlers:
        logger_temp.removeHandler(handler)
    
    rotFileHandler = handlers.RotatingFileHandler(log_file, 'a', LOG_SIZE, LOG_NUM_BACKUP)
    rotFileHandler.setLevel(logging.DEBUG)
    rotFileHandler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-5s [' + logger_name.rjust(25) + ']  %(message)s', '%b-%d %H:%M:%S'))
    logger_temp.addHandler(rotFileHandler)
    
    if not quiet:
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.DEBUG)
        consoleHandler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-5s [' + logger_name.rjust(25) + ']  %(message)s', '%b-%d %H:%M:%S'))
        logger_temp.addHandler(consoleHandler)