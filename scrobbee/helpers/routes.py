#!/usr/bin/env python

from scrobbee.controllers.pair import PairController
import cherrypy

def setup():
    mapper = cherrypy.dispatch.RoutesDispatcher()
    
    mapper.connect('main', '/', controller = PairController(), action = 'index')
    mapper.connect('pair', '/pair/', controller = PairController(), action = 'index')
    mapper.connect('pair', '/pair/:action', controller = PairController(), action = 'index')

    return mapper