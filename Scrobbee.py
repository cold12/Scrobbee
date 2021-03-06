#!/usr/bin/env python

import sys
import os
import argparse
import signal
import threading
import time
import webbrowser

# Add lib folder to path so we don't need to prepend al imports with lib.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib'))

import scrobbee
from scrobbee.helpers import logger

signal.signal(signal.SIGINT, scrobbee.sig_handler)
signal.signal(signal.SIGTERM, scrobbee.sig_handler)

def daemonize():
    """ Fork off as a daemon """

    # Make a non-session-leader child process
    try:
        pid = os.fork()
        if pid != 0:
            sys.exit(0)
    except OSError, e:
        raise RuntimeError("1st fork failed: %s [%d]" %
                   (e.strerror, e.errno))

    os.setsid()

    # Make sure I can read my own files and shut out others
    prev = os.umask(0)
    os.umask(prev and int('077', 8))

    # Make the child a session-leader by detaching from the terminal
    try:
        pid = os.fork()
        if pid != 0:
            sys.exit(0)
    except OSError, e:
        raise RuntimeError("2st fork failed: %s [%d]" %
                   (e.strerror, e.errno))

    dev_null = file('/dev/null', 'r')
    os.dup2(dev_null.fileno(), sys.stdin.fileno())

    if scrobbee.CREATEPID:
        pid = str(os.getpid())
        logger.log(u"Writing PID " + pid + " to " + str(scrobbee.PIDFILE))
        file(scrobbee.PIDFILE, 'w').write("%s\n" % pid)

def main():
    """ Runs Scrobbee """
    
    scrobbee.PROG_DIR = os.path.dirname(os.path.abspath(__file__))
    scrobbee.DATA_DIR = scrobbee.PROG_DIR
    scrobbee.CONFIG_SPEC = os.path.join(scrobbee.PROG_DIR, "configspec.ini")
    
    threading.currentThread().name = "MAIN"
    
    parser = argparse.ArgumentParser(description="Scrobble what's playing on the Boxee Box.")
    parser.add_argument('-q', '--quiet', action='store_true', dest="QUIET", help="disables console output and quiets Scrobbee")
    parser.add_argument('--nolaunch', action='store_true', dest="NOLAUNCH", help="makes sure the browser doesn't launch on startup")
    parser.add_argument('-p', '--port', dest="PORT", type=int, help="defines the port on which Scrobbee will run")
    parser.add_argument('-d', '--daemon', dest="DAEMON", help="daemonizes Scrobbee so it keeps running in the background until close explicitly")
    parser.add_argument('--datadir', dest="DATADIR", type=os.path.abspath, help="determins the location where the Scrobbee data (config file, database, PID file ...) is stored")
    parser.add_argument('--config', dest="CONFIG_FILE", type=os.path.abspath, help="determines the location of the config file. Can be a filename or a directory. In the latter case, the config file will be named config.ini")
    parser.add_argument('--pidfile', dest="PIDFILE", type=os.path.abspath, help="determines the location of the PID file")
    
    args = parser.parse_args(namespace=scrobbee)
    
    # Check the arguments
    if (scrobbee.DAEMON):
        if (sys.platform == "win32"):
            print "Daemonize not supported under Windows, starting normally"
            scrobbee.DAEMON = False
        else:
            scrobbee.QUIET = True
    
    if not scrobbee.PIDFILE is None:
        # if the pidfile already exists, sickbeard may still be running, so exit
        if os.path.exists(scrobbee.PIDFILE):
            sys.exit("PID file " + scrobbee.PIDFILE + " already exists. Exiting.")
        if scrobbee.DAEMON:
            try:
                file(scrobbee.PIDFILE, 'w').write("pid\n") #Move this together with the other file checking
            except IOError, e:
                raise SystemExit("Unable to write PID file: %s [%d]" % (e.strerror, e.errno))
        else:
            scrobbee.PIDFILE = None
            logger.log(u"Not running in daemon mode. PID file creation disabled.")
    
    # Set config file if not specified
    if not scrobbee.CONFIG_FILE:
        scrobbee.CONFIG_FILE = os.path.join(scrobbee.DATA_DIR, "config.ini")
    
    # Check if datadir exists and create it otherwise
    if not os.access(scrobbee.DATA_DIR, os.F_OK):
        try:
            os.makedirs(scrobbee.DATA_DIR, 0744)
        except os.error, e:
            raise SystemExit("Unable to create datadir '" + sickbeard.DATA_DIR + "'")
    
    # Check if the datadir is writeable
    if not os.access(scrobbee.DATA_DIR, os.W_OK):
        raise SystemExit("Datadir must be writeable '" + scrobbee.DATA_DIR + "'")
    
    # Check if the config file is writeable
    if not os.access(scrobbee.CONFIG_FILE, os.W_OK):
        if os.path.isfile(scrobbee.CONFIG_FILE):
            raise SystemExit("Config file '" + scrobbee.CONFIG_FILE + "' must be writeable")
        elif not os.access(os.path.dirname(scrobbee.CONFIG_FILE), os.W_OK):
            raise SystemExit("Config file dir '" + os.path.dirname(scrobbee.CONFIG_FILE) + "' must be writeable")
    
    
    # Initialize Scrobbee
    scrobbee.initialize()
    
    # Daemonize if necessary
    if scrobbee.DAEMON:
        daemonize()
    
    # While loop with actual functionality
    
    if not scrobbee.QUIET:
        print "Starting Scrobbee"
    
    scrobbee.start()
    
    # Start web browser
    if not scrobbee.NOLAUNCH:
        browserURL = "http://localhost:8080/"
        try:
            webbrowser.open(browserURL, 2, 1)
        except:
            try:
                webbrowser.open(browserURL, 1, 1)
            except:
                logger.error(u"Unable to launch a browser", 'Launch')
    
    while (True):
        time.sleep(1)

  
if __name__ == "__main__":
    main()