#!/usr/bin/env python

import re

import cherrypy
from scrobbee.boxee import Boxee
from boxeeboxclient import BoxeeClientAPIException

ValidIpAddressRegex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$";

class PairController():
    
    def __init__(self):
        return
    
    @cherrypy.expose
    @cherrypy.tools.jinja(filename = 'pair/index.tmpl')
    def index(self, ip='', port=''):
        if (not ip is '' and not port is ''):
            pattern = re.compile(ValidIpAddressRegex)
            if (pattern.match(ip) is None):
                #Error
                return{'error': 'error', 'ip': ip, 'port': port}
            
            self.ip = ip
            self.port = int(port)
                
            boxeeclient = Boxee(self.ip, self.port)
            try:
                boxeeclient.pairChallenge()
            except BoxeeClientAPIException:
                return{'error': 'Already paired to this ip?', 'ip': ip, 'port': port}
            
            raise cherrypy.HTTPRedirect('/pair/step2')
            
        return {'ip': ip, 'port': port}
    
    @cherrypy.expose
    @cherrypy.tools.jinja(filename = 'pair/step2.tmpl')
    def step2(self, challenge=''):
        if (not challenge is ''):
            pattern = re.compile("^[0-9]{4}$")
            if (pattern.match(challenge) is None):
                return {'challenge': challenge}
            
            boxeeclient = Boxee(self.ip, self.port)
            try:
                boxeeclient.pairResponse(challenge)
            except BoxeeClientAPIException:
                return{'error': 'You probably entered a faulty challenge code. Retry!'}
            
            raise cherrypy.HTTPRedirect('/pair/step3')
        
        return {'challenge': challenge}
    
    @cherrypy.expose
    @cherrypy.tools.jinja(filename = 'pair/step3.tmpl')
    def step3(self):        
        return {}