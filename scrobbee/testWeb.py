#!/usr/bin/env python

import cherrypy

class Test():
    @cherrypy.expose
    @cherrypy.tools.jinja(filename='test/index.tmpl')
    def index(self):
        return {}