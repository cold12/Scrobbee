#!/usr/bin/env python

from configobj import ConfigObj
from validate import Validator

class Config():
    config = None
    
    def __init__(self, config_file):
        self.config_file = config_file
        
    def initConfig(self, config_spec = None):
        if not config_spec is None:
            self.config_spec = config_spec
            configspec = ConfigObj(config_spec, _inspec=True)
            self.config = ConfigObj(self.config_file, configspec=configspec)
            val = Validator()
            config_validated = self.config.validate(val, copy=True)
            
            if config_validated == False:
                print 'Error in config'
                exit()
            
            self.config.write()
    
    def getSections(self):
        return self.config.keys()
    
    def getConfig(self):
        return self.config
    
    def saveConfig(self):
        self.config.write()