#!/usr/bin/env python

import os

import cherrypy

import scrobbee
from scrobbee.helpers import views, logger

def initServer(options = {}):
    options.setdefault('port',      8081)
    options.setdefault('host',      '0.0.0.0')
    options.setdefault('prog_dir',   os.path.dirname(os.path.abspath(os.path.join(__file__, '..'))))
    options.setdefault('data_dir',   os.path.dirname(os.path.abspath(os.path.join(__file__, '..', '..'))))
    
    loader = views.JinjaLoader(os.path.join(options['prog_dir'], 'views'))
    cherrypy.tools.jinja = cherrypy.Tool('before_handler', loader, priority=70)
    
    # Use a controller for errors (such as 404) to keep the templates cleaner
    from scrobbee.controllers.error import ErrorController
    ec = ErrorController(os.path.join(options['prog_dir'], 'views'))
    
    # cherrypy setup
    cherrypy.config.update({
            #'server.socket_port': options['port'],
            #'server.socket_host': options['host'],
            'log.screen':           False,
            'log.access_file':      os.path.join(options['data_dir'], 'logs', 'cherrypy.log'),
            #'error_page.401':     http_error_401_hander,
            'error_page.404':      ec.error_404,
    })
    
    from scrobbee.helpers.routes import setup as Routes
            
    conf = {
        '/': {
            'request.dispatch': Routes(),
            'tools.sessions.on': True,
            'tools.sessions.timeout': 240,

            'tools.gzip.on': True,
            'tools.gzip.mime_types': ['text/html', 'text/plain', 'text/css', 'text/javascript', 'application/javascript']
        },
    }
    
    app = cherrypy.tree.mount(root = None, config = conf)
    
    logger.info("Starting Cherrpy", 'Startup')
    cherrypy.server.start()
    cherrypy.server.wait()
    