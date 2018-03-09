import time, uwsgi, os, sys, logging
import threading, re, json, subprocess
from datetime import datetime

logger = logging.getLogger("/yourpropath/monitor")

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




###=============================== 

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


