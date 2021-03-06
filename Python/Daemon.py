
class BaseDaemon(object):
    """A generic daemon class.
    Usage: subclass the daemon class and override the run() method."""

    def __init__(self, pidfile): self.pidfile = pidfile

    def daemonize(self):
        """Deamonize class. UNIX double fork mechanism."""

        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork #1 failed: {0}\n'.format(err))
            sys.exit(1)

        # decouple from parent environment
        os.chdir('/')
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork #2 failed: {0}\n'.format(err))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)

        pid = str(os.getpid())
        with open(self.pidfile,'w+') as f:
            f.write(pid + '\n')

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """Start the daemon."""

        # Check for a pidfile to see if the daemon already runs
        try:
            with open(self.pidfile,'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if pid:
            message = "pidfile {0} already exist. \nDaemon already running?\n"
            sys.stderr.write(message.format(self.pidfile))
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """Stop the daemon."""

        # Get the pid from the pidfile
        try:
            with open(self.pidfile,'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if not pid:
            message = "pidfile {0} does not exist. \nDaemon not running?\n"
            sys.stderr.write(message.format(self.pidfile))
            return # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            e = str(err.args)
            if e.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                logging.error(str(err.args))
                sys.exit(1)

    def restart(self):
        """Restart the daemon."""
        self.stop()
        self.start()

    def run(self):
        """You should override this method when you subclass Daemon.

        It will be called after the process has been daemonized by
        start() or restart()."""


class EventReplayDaemon(BaseDaemon):
    def run(self):
        # count = 0
        # logging.debug('loop')
        # while True:
        #     count += 1
        #     logging.debug("====> {}".format(count))
        #     time.sleep(1)
        StartUdpServer()
 
if __name__ == "__main__":
    #js_parser = JsonTextParser().get_all_nodes_latest_events()
    # ==================<
    StartUdpServer()
    # ==================>
    # with open('/Users/liambao/Desktop/gerrit/cg-mesh/tools/matrix_ui/server/test', 'rb+') as f:
    #     data = f.read()
    # e= EventReplay(data)
    # data = e.parse_rawdata()
    # e.save_to_file(data)
    # print("===++===")

    # daemon process
    # try:
    #     daemon = EventReplayDaemon('/tmp/event-replay.pid')
    #     if len(sys.argv) == 2:
    #         if 'start' == sys.argv[1]:
    #             logging.debug('Start the event replay Daemen')
    #             daemon.start()
    #         elif 'stop' == sys.argv[1]:
    #             logging.debug('Stop event replay Daemen')
    #             daemon.stop()
    #         elif 'restart' == sys.argv[1]:
    #             logging.debug('Restart Daemen')
    #             daemon.restart()
    #         else:
    #             logging.debug("Unknown command")
    #             sys.exit(2)
    #         sys.exit(0)
    #     else:
    #         logging.debug("usage: %s start|stop|restart" % sys.argv[0])
    #         sys.exit(2)
    # except Exception as e:
    #     logging.error(e)

if __name__ == '__main__':
    main()
