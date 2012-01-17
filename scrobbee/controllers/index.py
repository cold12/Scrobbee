#!/usr/bin/env python

import re

import cherrypy

class IndexController():
    
    def __init__(self):
        return
    
    @cherrypy.expose
    @cherrypy.tools.jinja(filename = 'index/index.tmpl')
    def index(self):
        return {}