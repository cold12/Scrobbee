#!/usr/bin/env python

import re

import cherrypy

class LogController():
    
    def __init__(self):
        return
    
    @cherrypy.expose
    @cherrypy.tools.jinja(filename = 'log/log.tmpl')
    def index(self):
        return {}