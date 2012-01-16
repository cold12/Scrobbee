#!/usr/bin/env python

import sys
import os

import cherrypy
import jinja2

from scrobbee.helpers import views, logger
from scrobbee import boxee
from scrobbee.helpers.config import Config

""" Variables for startup """
QUIET = False

DAEMON = False
CREATEPID = False
PIDFILE = None

PROG_DIR = None
DATA_DIR = None
CONFIG_SPEC = None
CONFIG_FILE = None

""" Variables for config """

CONFIG = None

def initialize():
    global CONFIG
    
    CONFIG = Config(CONFIG_FILE)
    CONFIG.initConfig(CONFIG_SPEC)
    
    logger.scrobbee_log_instance.initLogging(os.path.join(DATA_DIR, 'logs'), QUIET)
    
def start():

    if CONFIG.getConfig()["Boxee"]["paired"]:
        client = boxee.Boxee("192.168.50.50", 9090)
        playing = client.getCurrentlyPlaying()
    
        logger.debug(str(playing), "Boxee playing")
    
    loader = views.JinjaLoader(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'views'))
    cherrypy.tools.jinja = cherrypy.Tool('before_handler', loader, priority=70)

    cherrypy.config.update({
        'global': {
            #'server.thread_pool': 10,
            #'server.socket_port': port,
            #'server.socket_host': ca.get('global', 'host'),
            #'server.environment': ca.get('global', 'server.environment'),
            #'engine.autoreload_on': ca.get('global', 'server.environment') == 'development',

            #'basePath': path_base,
            #'runPath': rundir,
            #'cachePath': cachedir,
            #'debug': debug,
            #'frozen': frozen,
            #
            ## Global workers
            #'config': ca,
            #'updater': myUpdater,
            #'cron': myCrons.threads,
            #'searchers': myCrons.searchers,
            #'flash': app.flash()
        }
    })
    
    # cherrypy setup
    cherrypy.config.update({
            #'server.socket_port': options['port'],
            #'server.socket_host': options['host'],
            'log.screen':           False,
            'log.access_file':      os.path.join(DATA_DIR, 'logs', 'cherrypy.log')
            #'error_page.401':     http_error_401_hander,
            #'error_page.404':     http_error_404_hander,
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
    
    cherrypy.server.start()
    cherrypy.server.wait()
    
def sig_handler(signum=None, frame=None):
    if type(signum) != type(None):
        logger.debug("Killing cherrypy", 'shutdown')
        cherrypy.engine.exit()
        
        if CREATEPID:
            logger.debug("Removing pidfile " + str(PIDFILE))
            os.remove(PIDFILE)
        
        logger.debug("Saving config file")
        CONFIG.saveConfig()
        
        logger.debug("Exiting MAIN thread")
        sys.exit()