#!/usr/bin/env python

from lib.configobj import ConfigObj
from lib.validate import Validator

""" Variables for startup """
DAEMON = False
CREATEPID = False
PIDFILE = None

PROG_DIR = None
DATA_DIR = None
CONFIG_SPEC = None
CONFIG_FILE = None

""" Variables for config """

CONFIG = None

def initialize(consoleLogging):
    """ Initiate config with configspec """
    global CONFIG
    
    configspec = ConfigObj(CONFIG_SPEC, _inspec=True)
    CONFIG = ConfigObj(CONFIG_FILE, configspec=configspec)
    val = Validator()
    config_validated = CONFIG.validate(val, copy=True)
        
    if config_validated == False:
        print 'Error in config'
        exit()
        
    CONFIG.write()