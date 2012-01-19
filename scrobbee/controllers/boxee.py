#!/usr/bin/env python

import re

import cherrypy

import scrobbee
from scrobbee.boxee import Boxee
from scrobbee.helpers import db
from boxeeboxclient import BoxeeClientAPIException

ValidIpAddressRegex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$";

class BoxeeController():
    
    def __init__(self):
        return
    
    @cherrypy.expose
    @cherrypy.tools.jinja(filename = 'boxee/add.tmpl')
    def add(self, ip='', port=''):
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
            
            raise cherrypy.HTTPRedirect('/boxee/add/challenge')
            
        return {'ip': ip, 'port': port}
    
    @cherrypy.expose
    @cherrypy.tools.jinja(filename = 'boxee/add_challenge.tmpl')
    def add_challenge(self, challenge=''):
        if (not challenge is ''):
            pattern = re.compile("^[0-9]{4}$")
            if (pattern.match(challenge) is None):
                return {'challenge': challenge}
            
            boxeeclient = Boxee(self.ip, self.port)
            try:
                boxeeclient.pairResponse(challenge)
            except BoxeeClientAPIException:
                return{'error': 'You probably entered a faulty challenge code. Retry!'}
            
            raise cherrypy.HTTPRedirect('/boxee/add/finish')
        
        return {'challenge': challenge}
    
    @cherrypy.expose
    @cherrypy.tools.jinja(filename = 'boxee/add_finish.tmpl')
    def add_finish(self):
        connection = db.DBConnection()
        connection.action("INSERT INTO boxee_boxes (boxee_name, ip, port) VALUES (?, ?, ?)", ["test", self.ip, self.port])
        
        return {}