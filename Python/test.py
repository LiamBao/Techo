import os

from  multiprocessing import Process, Lock

def f( i):
#    l.acquire()
#    try:
        print('hello ', i)
#    finally:
#        l.release()

if __name__ == "__main__":
#    lock = Lock()
    for i in range(100):
#        Process(target=f, args=(lock, i)).start()
        Process(target=f, args=(i,)).start()


