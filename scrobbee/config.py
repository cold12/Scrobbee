#!/usr/bin/env python

from lib.configobj import ConfigObj
from lib.validate import Validator

class Config():
    def __init__(self, configfile, configspec):
        """ Initiate config with configspec """
        configspec = ConfigObj(configspec, _inspec=True)
        config = ConfigObj(configfile, configspec=configspec)
        val = Validator()
        config_validated = config.validate(val, copy=True)
        
        if config_validated == False:
            print 'Error in config'
            exit()
        
        config.write()
    
    def initialize(self, configfile):
        self.configfile = configfile
        self.config = ConfigObj(configfile)

    