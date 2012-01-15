#!/usr/bin/env python

import sys
import os

import cherrypy

from testWeb import Test

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

def initialize(consoleLogging):
    """ Initiate config with configspec """
    global CONFIG
    
    CONFIG = Config(CONFIG_FILE, CONFIG_SPEC).getConfig()
    
def start():

    if CONFIG["Boxee"]["paired"]:
        client = boxee.Boxee("192.168.50.50", 9090)
        playing = client.getCurrentlyPlaying()
    
        print playing
    
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

    from testWeb import Test
    
    app = cherrypy.tree.mount(Test(), '/')
    
    cherrypy.server.start()
    cherrypy.server.wait()
    
def sig_handler(signum=None, frame=None):
    if type(signum) != type(None):
        print "Killing cherrypy"
        cherrypy.engine.exit()
        
        if CREATEPID:
            print "Removing pidfile " + str(PIDFILE)
            os.remove(PIDFILE)
        
        print "Exiting MAIN thread"
        sys.exit()