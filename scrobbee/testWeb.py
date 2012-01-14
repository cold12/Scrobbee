#!/usr/bin/env python

import cherrypy

class Test():
    @cherrypy.expose
    def index(self):
        return "Test"