#!/usr/bin/env python

def daemonize():
    """ Fork off as a daemon """

    # Make a non-session-leader child process
    try:
        pid = os.fork() #@UndefinedVariable - only available in UNIX
        if pid != 0:
            sys.exit(0)
    except OSError, e:
        raise RuntimeError("1st fork failed: %s [%d]" %
                   (e.strerror, e.errno))

    os.setsid() #@UndefinedVariable - only available in UNIX

    # Make sure I can read my own files and shut out others
    prev = os.umask(0)
    os.umask(prev and int('077', 8))

    # Make the child a session-leader by detaching from the terminal
    try:
        pid = os.fork() #@UndefinedVariable - only available in UNIX
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
    try:
        opts, args = getopt.getopt(sys.argv[1:], "qdp::", ['quiet', 'daemon', 'port=', 'pidfile=', 'config=', 'datadir=']) #@UnusedVariable
    except getopt.GetoptError:
        print "Available options: --quiet, --port, --daemon, --pidfile, --config, --datadir"
        sys.exit()
    
    consoleLogging = True
    
    for o, a in opts:
        # for now we'll just silence the logging
        if o in ('-q', '--quiet'):
            consoleLogging = False

        # use a different port
        if o in ('-p', '--port'):
            forcedPort = int(a)

        # Run as a daemon
        if o in ('-d', '--daemon'):
            if sys.platform == 'win32':
                print "Daemonize not supported under Windows, starting normally"
            else:
                consoleLogging = False
                scrobbee.DAEMON = True

        # config file
        if o in ('--config',):
            scrobbee.CONFIG_FILE = os.path.abspath(a)

        # datadir
        if o in ('--datadir',):
            scrobbee.DATA_DIR = os.path.abspath(a)

        # write a pidfile if requested
        if o in ('--pidfile',):
            scrobbee.PIDFILE = str(a)

            # if the pidfile already exists, sickbeard may still be running, so exit
            if os.path.exists(scrobbee.PIDFILE):
                sys.exit("PID file " + scrobbee.PIDFILE + " already exists. Exiting.")

            # a pidfile is only useful in daemon mode
            # also, test to make sure we can write the file properly
            if scrobbee.DAEMON:
                scrobbee.CREATEPID = True
                try:
                    file(scrobbee.PIDFILE, 'w').write("pid\n")
                except IOError, e:
                    raise SystemExit("Unable to write PID file: %s [%d]" % (e.strerror, e.errno))
            else:
                logger.log(u"Not running in daemon mode. PID file creation disabled.")
                
    # Set config file if not specified
    
    # Check if datadir exists and create it otherwise
    
    # Check if the datadir is writeable
    
    # Check if the config file is writeable
    
    # Load config
    
    # Initialize Scrobbee
    
    # Daemonize if necessary
    
    # Initialize the webserver
    
    # While loop with actual functionality

  
if __name__ == "__main__":
    main()