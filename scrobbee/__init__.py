#!/usr/bin/env python

import sys

import cherrypy

from testWeb import Test

from configobj import ConfigObj
from validate import Validator
from scrobbee import boxee

""" Variables for startup """
QUIET = False

DAEMON = False
CREATEPID = False
PIDFILE = None

PROG_DIR = None
DATA_DIR = None
CONFIG_SPEC = None
CONFIG_FILE = None

PAIRED = False

""" Variables for config """

CONFIG = None

def initialize(consoleLogging):
    """ Initiate config with configspec """
    global CONFIG
    
    client = None
    
    configspec = ConfigObj(CONFIG_SPEC, _inspec=True)
    CONFIG = ConfigObj(CONFIG_FILE, configspec=configspec)
    val = Validator()
    config_validated = CONFIG.validate(val, copy=True)
        
    if config_validated == False:
        print 'Error in config'
        exit()
        
    CONFIG.write()
    
def start():

    if PAIRED:
        client = boxee.Boxee("192.168.50.50", 9090)
        playing = client.getCurrentlyPlaying()
    
        print playing
    
    app = cherrypy.tree.mount(Test(), '/')
    
    cherrypy.server.start()
    cherrypy.server.wait()
    
def sig_handler(signum=None, frame=None):
    if type(signum) != type(None):
        print "Killing cherrypy"
        cherrypy.engine.exit()
        
        if CREATEPID:
            print "Removing pidfile " + str(PIDFILE)
            os.remove(PIDFILE)
        
        print "Exiting MAIN thread"
        sys.exit()