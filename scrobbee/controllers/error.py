#!/usr/bin/env python

import cherrypy

import jinja2
from jinja2 import Environment, PackageLoader

class ErrorController():
    
    def __init__(self, views_dir):
        self.views_dir = views_dir
        return
    
    def error_404(self, status, message, traceback, version):
        # Different method. Loading template through @cherrypy.tools.jinja doesn't work here.
        env = Environment(loader=jinja2.FileSystemLoader(self.views_dir))
        template = env.get_template('error/404.tmpl')
        
        return template.render({'status': status, 'message': message, 'traceback': traceback, 'version': version})
        
