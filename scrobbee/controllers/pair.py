#!/usr/bin/env python

import re

import cherrypy
from scrobbee.boxee import Boxee

class PairController():
    
    def __init__(self):
        return
    
    @cherrypy.expose
    @cherrypy.tools.jinja(filename = 'pair/index.tmpl')
    def index(self):
        return {}
    
    @cherrypy.expose
    @cherrypy.tools.jinja(filename = 'pair/step2.tmpl')
    def step2(self, ip, port=9090):
        self.ip = ip
        self.port = int(port)
        
        boxeeclient = Boxee(self.ip, self.port)
        boxeeclient.pairChallenge()
        
        return {}
    
    @cherrypy.expose
    @cherrypy.tools.jinja(filename = 'pair/step3.tmpl')
    def step3(self, challenge):
        boxeeclient = Boxee(self.ip, self.port)
        
        pattern = re.compile("^[0-9]{4}$")
        boxeeclient.pairResponse(challenge)
        
        return {}