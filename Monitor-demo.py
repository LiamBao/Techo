import time, uwsgi, os, sys, logging
import threading, re, json, subprocess
from datetime import datetime

logger = logging.getLogger("/yourpropath/monitor")

## Demo1: StrictRedis to Monitor service status.
from project import redis_connection, models, __version__, settings

def get_status():
    status = {}
    info = redis_connection.info()
    status['redis_used_memory'] = info['used_memory']
    status['redis_used_memory_human'] = info['used_memory_human']
    status['version'] = __version__
    status['queries_count'] = models.db.session.query(models.Query).count()
    if settings.FEATURE_SHOW_QUERY_RESULTS_COUNT:
        status['query_results_count'] = models.db.session.query(models.QueryResult).count()
        status['unused_query_results_count'] = models.QueryResult.unused().count()

    status['workers'] = []
    status['manager'] = redis_connection.hgetall('project:status')

    queues = {}
    for ds in models.DataSource.query:
        for queue in (ds.queue_name, ds.scheduled_queue_name):
            queues.setdefault(queue, set())
            queues[queue].add(ds.name)

    status['manager']['queues'] = {}
    for queue, sources in queues.iteritems():
        status['manager']['queues'][queue] = {
            'data_sources': ', '.join(sources),
            'size': redis_connection.llen(queue)
        }

    return status

#  Demo2: Creating Thread Using Threading Module
"""
https://www.tutorialspoint.com/python/python_multithreading.htm

To implement a new thread using the threading module, you have to do the following
Define a new subclass of the Thread class.
Override the __init__(self [,args]) method to add additional arguments.
Then, override the run(self [,args]) method to implement 
what the thread should do when started.
Once you have created the new Thread subclass, 
you can create an instance of it and then start a new thread by invoking the start(), 

which in turn calls run() method.

"""
import threading
import time

exitFlag = 0

class myThread(threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      print("Starting " + self.name)
      print_time(self.name, 5, self.counter)
      print("Exiting " + self.name)

def print_time(threadName, counter, delay):
   while counter:
      if exitFlag:
         threadName.exit()
      time.sleep(delay)
      print("%s: %s" % (threadName, time.ctime(time.time())))
      counter -= 1

# Create new threads
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# Start new Threads
thread1.start()
thread2.start()

print("Exiting Main Thread")


#  Demo3 :
class serverMonitor():
    def update():
        
        now=datetime.now()
        update_time= datetime.now()
        time.sleep(2)
        diff=now-update_time
        days,rest=divmod(diff.days*24*3600+diff.seconds,24*3600)
        hours,rest=divmod(rest,3600)
        minutes,seconds=divmod(rest,60)
        print("%dd%dh%dm%ds" % (days,hours,minutes,seconds))

monitors = {}
def startMonitor(MonitorClass):
    tryTimes = 3
    for i in range(0, tryTimes)


if "__name__" == "__main__":
    try:
        startMonitor(serverMonitor)
    except e as Exception:
        print(e)


# Demo 4
"""
demo for 
"""
import threading

class Monitor(threading.Thread):
    def __init__(self):
        super(Monitor, self).__init__()

    def _check_server_status(self):
        raise NotImplementedError

    def check_status(self):
        _check_server_status()
    
    def run(self):
        try:
            self.check_status()
        except Exception as e:
            print("error: " + e)

class ServerMonitor(Monitor):

    def __init__(self):
        super(ServerMonitor, self).__init__()

    def _check_service_status(self):
        #mainbody
        pass

def start_monitor():
    ServerMonitor().start()


#  Decorator Demo

class myClass:
    somevar = "somevar"

    def _func_to_be_threaded(self):
        #main body
    
    def func_to_be_threaded(self):
        threading.Thread(target=self._func_to_be_threaded).start()


# and it can be shorted with a decorator

def threaded(func):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwarg)
        thread.start() 
        return thread
    return wrapper


class myClass:
    somevar="somevar"

    @threaded
    def func_to_be_threaded(self):
        #main body