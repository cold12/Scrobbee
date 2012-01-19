#!/usr/bin/env python

import re

import cherrypy

from scrobbee.helpers import logger, db

class IndexController():
    
    def __init__(self):
        return
    
    @cherrypy.expose
    @cherrypy.tools.jinja(filename = 'index/index.tmpl')
    def index(self):
        connection = db.DBConnection()
        boxee_boxes = connection.action("SELECT * FROM BOXEE_BOXES").fetchall()
        
        return {'boxee_boxes': boxee_boxes}