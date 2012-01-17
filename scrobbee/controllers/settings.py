#!/usr/bin/env python

import re

import cherrypy

class SettingsController():
    
    def __init__(self):
        return
    
    @cherrypy.expose
    @cherrypy.tools.jinja(filename = 'settings/settings.tmpl')
    def index(self):
        return {}