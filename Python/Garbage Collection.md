- [内存管理及释放 ](https://blog.csdn.net/jiangjiang_jian/article/details/79140742)
- [Python 进程内存增长解决方案](https://zhuanlan.zhihu.com/p/28031057)
- [记一次调试python内存泄露的问题](https://cloud.tencent.com/developer/article/1115715)
- []()
- []()
- []()
- []()
- []()



----

```python
import gc （garbage collector）
del a
gc.collect()
```

```python
import gc
gc.disable()
data = range(1,5000000)  
wdict = dict(zip(data,data))  
gc.enable()
```

```
```

####  内存池机制:

![fc286b44da6362ce5b874fef5ff32b45.png](evernotecid://D8706BDE-7D2C-4F0E-B812-EA5A632A314D/appyinxiangcom/2930334/ENResource/p149)

 

当调用del时，其实Python并不会真正release内存，而是将其继续放在其内存池中；只有在显式调用gc.collect()时，才会真正release内存

```bash
while ((1)); 
    do ps -aux | sort -n -k5,6 | grep my_script; 
    free; 
    sleep 5; 
done
```




[python 内存管理](http://www.cnblogs.com/vamei/p/3232088.html)


* 对象的内存使用: 在Python中，每个对象都有存有指向该对象的引用总数，即引用计数(reference count)

```python
a = 1

print(id(a))
print(hex(id(a)))

a = 1
b = 1

print(id(a))
print(id(b))

# True
a = 1
b = 1
print(a is b)

# True
a = "good"
b = "good"
print(a is b)

# False
a = "very good morning"
b = "very good morning"
print(a is b)

# False
a = []
b = []
print(a is b)
```
可以看到，由于Python缓存了整数和短字符串，因此每个对象只存有一份。比如，所有整数1的引用都指向同一对象。即使使用赋值语句，也只是创造了新的引用，而不是对象本身。长的字符串和其它对象可以有多个相同的对象，可以使用赋值语句创建出新的对象。

* 对象引用对象: Python的一个容器对象(container)，比如表、词典等，可以包含多个对象。实际上，容器对象中包含的并不是元素对象本身，是指向各个元素对象的引用





```python
# coding=utf8
import time
import psutil, gc, commands,os

from logger_until import LoggerUntil
from until import keep_circulating

logger = LoggerUntil(name="Monitor").getlog(logfilename='Monitor.log', loglevel=2, add_StreamHandler=1)

need_monitor_procces_names = [  ##需要检测的进程的cmd命令放到这里，支持模糊匹配
    'touna0627.py',
    'dailiip.py',
    'redis-server',
    'mongod',
]


class Monitor(object):
    def __init__(self):
        self.specified_process_list = self.get_specified_process()
        self.current_process = self.get_current_process()

    @staticmethod
    def print_all_cmdlines():
        for pid in psutil.pids():
            p = psutil.Process(pid)
            print p.cmdline()

    @staticmethod
    def get_specified_process():
        all_pids = psutil.pids()
        process_list = []
        for pid in all_pids:
            p = psutil.Process(pid)
            p_cmdline = p.cmdline()
            for argx in p_cmdline:
                for name in need_monitor_procces_names:
                    if argx.find(name) > -1:
                        if p.status() != 'stopped':
                            process_list.append(p)

        p_pid_set = set()
        process_list2 = []
        for p in process_list:
            if p.pid not in p_pid_set:
                process_list2.append(p)
                p_pid_set.add(p.pid)
        return process_list2

    @staticmethod
    def monitor_system():
        psutil.cpu_percent()
        time.sleep(1)
        mem = psutil.virtual_memory()

        mem_total = mem.total / 1000000
        mem_available = mem.available / 1000000
        mem_percent_str = str(mem.percent) + '%'

        cpu_count = psutil.cpu_count()
        cpu_percent_str = str(psutil.cpu_percent()) + '%'

        msg = '本机总内存是：{0}M ， 本机可用内存是：{1}M， 本机内存使用率是：{2}， 本机cpu核数是：{3}， 本机cpu使用率是：{4}\n\n'.format(mem_total, mem_available, mem_percent_str, cpu_count, cpu_percent_str)
        logger.info(msg)

    def monitor_specified_process(self):
        for p in self.specified_process_list:
            p.cpu_percent(None)
        time.sleep(1)
        for p in self.specified_process_list:
            # p = psutil.Process(0)
            """:type :psutil.Process"""
            cmdline_str = '  '.join(p.cmdline()).ljust(60, ' ')
            p_cpu_percent_str = str(round(p.cpu_percent(), 2)) + '%'
            p_memory_percent_str = str(round(p.memory_percent(), 2)) + '%'
            p_strated_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p.create_time()))
            p_pid_str = str(p.pid)

            msg = '进程' + cmdline_str + ' 的pid是：' + p_pid_str + '  cpu使用率是：' + p_cpu_percent_str + '  内存使用率是：' + p_memory_percent_str \
                  + '  进程的启动时间是：' + p_strated_time
            logger.info(msg)

    @staticmethod
    def get_current_process():
        return psutil.Process()

    def is_need_release(self,threshold):
        print self.current_process.memory_percent()
        if self.current_process.memory_percent() < threshold:
            return 0
        else:
            logger.info('回收当前 %s 进程id的内存' % self.current_process.pid)
            return  1

    def free_current_process_memory(self, threshold):
        """回收python所处的当前进程的内存"""
        if self.is_need_release(threshold) == 1:
            gc.collect()

class MemoryReleaser():
    def __init__(self,threshold,cmd_name_str='touna0627.py'):
        """
        :type  threshold：float
        """
        self.threshold = threshold    # 内存使用率的阈值
        self.cmd_name_str =cmd_name_str
        self.stutus, self.output = self.__get_memory_available()


    def __get_memory_available(self):
        # status, output = commands.getstatusoutput("free -m | grep Mem | awk  '{print $4}'")  ##shell命令查询计算机可用内存
        status, output = commands.getstatusoutput("ps aux | grep %s  | sort -k4,4nr|head -1| awk '{print $4}'"%(self.cmd_name_str))  ##shell命令查询程序的内存使用率
        return  status, output

    def release_memory(self):
        if float(self.output) > self.threshold:
            logger.info('程序的内存使用率是 {}% ,程序需要释放内存'.format(self.output))
            gc.collect()

@keep_circulating(10)
def monitoring():
    MemoryReleaser(40).release_memory()     ###这一行来释放内存
    monitor = Monitor()
    monitor.monitor_specified_process()
    monitor.monitor_system()

if __name__ == "__main__":
    pass
    a = list(range(10000000))
    del a
    time.sleep(30)
    monitoring()
```

>如果把MemoryReleaser(600).release_memory() 注释掉，程序将一直是占用大内存
>程序中使用了 
>`free -m | grep Mem | awk  '{print $7}'`
>来判断计算机可用内存
>虽然psutil可以判断内存，但使用psutil判断内存，内存就无法回收了
>把MemoryReleaser(600).release_memory() 放到monitoring函数中的最后一行，那就回收不了内存了