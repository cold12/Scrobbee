#!/usr/bin/env python

import sys
import os
import threading

import cherrypy
import jinja2

from scrobbee.helpers import views, logger, webserver
from scrobbee import boxee
from scrobbee.helpers.config import Config

INIT_LOCK = threading.Lock()
__INITIALIZED__ = False

""" Variables for startup """
QUIET = False
NOLAUNCH = False

DAEMON = False
CREATEPID = False
PIDFILE = None

PROG_DIR = None
DATA_DIR = None
CONFIG_SPEC = None
CONFIG_FILE = None

""" Variables for config """

CONFIG = None

def initialize():
    
    with INIT_LOCK:
        
        global __INITIALIZED__, CONFIG
    
        if __INITIALIZED__:
            return False
    
        # Initialize the config. Accessible through scrobbee.CONFIG.getConfig()
        CONFIG = Config(CONFIG_FILE)
        CONFIG.initConfig(CONFIG_SPEC)
    
        # Initialize the logger. Just use import logger and logger.debug/info/...
        logger.scrobbee_log_instance.initLogging(os.path.join(DATA_DIR, 'logs'), QUIET)
    
        #Initialize threads / scheduler
        
        __INITIALIZED__ = True
    
def start():
    global __INITIALIZED__
    
    with INIT_LOCK:
        
        if __INITIALIZED__:

            # Start the threads.
    
            # Start the webserver.
            webserver.initServer()

def stopThreads():
    
    global __INITIALIZED__
    
    with INIT_LOCK:
        
        if __INITIALIZED__:
            
            logger.log(u'Stopping scrobbee threads', 'Shutdown')
            
            # Stop the threads.
            
            __INITIALIZED__ = False

def save():
    global CONFIG
    
    logger.debug("Saving config file", 'Shutdown')
    CONFIG.saveConfig()
    
def shutdown():
    save()
    
    logger.debug("Killing cherrypy", 'Shutdown')
    cherrypy.engine.exit()
    
    if CREATEPID:
        logger.debug("Removing pidfile " + str(PIDFILE), 'Shutdown')
        os.remove(PIDFILE)
        
    logger.debug("Exiting MAIN thread", 'Shutdown')
    sys.exit()
    
def sig_handler(signum=None, frame=None):
    if type(signum) != type(None):
        logger.info(u"Signal %(signum)i caught, shutting down Scrobbee ..." % {'signum': int(signum)}, 'Shutdown')
        shutdown()