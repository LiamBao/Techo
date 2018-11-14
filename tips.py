# -*- coding:utf-8 -*-
__author__ = 'liam_bao@163.com'
import dis

"""

 子类无法继承父类 __slot__

"""

"""
    策略模式

"""


"""
    上下文管理器

    平常在写Python代码的时候，经常会用到 with 来处理一个上下文环境，比如文件的打开关闭，数据库的连接关闭等等。

    with语法的使用，需要我们处理的对象实现__enter__和__exit__两个魔术方法来支持。__enter__函数处理逻辑函
    数之前需要做的事情，并返回操作对象作为as后面的变量，__exit__函数处理当代码离开with代码块以后的事情。

    with语法非常方便的让我使用资源并且不用操心忘记后续操作所带来的隐患


    contextlib 中的 contextmanager 作为装饰器来提供一种针对函数级别的上下文管理机制。

    同时也支持编写协程时处理异步的上下文环境的asynccontextmanager装饰器。

    @contextmanager
    对于contextmanager装饰器的原理，通过阅读源码，我的理解是："插入式编码"。这里我有思考过和普通的装饰器怎么的不同，
    我自己定义为普通的装饰器是"包裹式编码"，看一个装饰器的功能往往是从装饰角度由外向内观察逻辑，
    而contextmanager却不同，它是"插入式"的，需要从函数出发由内向外观察。

    怎么说是插入式呢？一个函数原本是自上向下顺序执行，突然在代码的中间，我们想要做点什么，
    就把代码卡在这里，去做想做的事情，等做完了以后，再回来接着执行相应的代码。

    要做到这一点，就借助到了yield关键字，contextmanager接受一个 Generator 来借助with ... as ..的语法特性，
    在内部实现了__enter__和__exit__方法后，将yield返回的对象输出出去，这样就可以衔接上了。比较官方的用法是下面这样：

    ```
    @contextmanager
    def some_generator():
        # 这里处理之前的事情
        try:
            yield value#这里 yield 返回要操作的变量
        finally:
            # 这里处理之后的事情

    with some_generator() as variable:
        # 处理逻辑
    ```
    这样的写法执行顺序就等价于：

    # 这里处理之前的事情
    try:
        variable = value
        # 处理逻辑
    finally:
        # 这里处理之后的事情


    @asynccontextmanager
    asynccontextmanager装饰器和contextmanager类似，但其内部实现是通过async和await协程语法实现的，
    所以它装饰的函数也必须是异步的实现。（这个语法支持需要python版本大于3.5）

"""

@asynccontextmanager
async def get_connection():
    conn = await acquire_db_connection()
    try:
        yield conn
    finally:
        await release_db_connection(conn)

async def get_all_users():
    async with get_connection() as conn:
        return conn.query('SELECT ...')

class MyContextManager(object):
    
    def __enter__(self):
        print("Hello")
        return self

    def __exit__(self, *args):
        print("Bye")

    def work(self):
        print("Do something...")

with MyContextManager() as worker:
    worker.work()


"""
    Python 调用机制
    
    For new-style classes, implicit invocations of special methods are only guaranteed 
    to work correctly if defined on an object’s type, not in the object’s instance dictionary. 
"""
class A(object):
    def __call__(self):
        print("invoking __call__ from class A")

a = A()
a()

a.__call__ = lambda: "invoking __call__ from lambda method"
print(a.__call__())
a()


"""操作系统:银行家算法
   fork()调用一次，返回两次，因为操作系统自动把当前进程（称为父进程）复制了一份（称为子进程），
   然后，分别在父进程和子进程内返回。子进程永远返回0，而父进程返回子进程的ID。 父子进程执行顺讯随机的。

   比如说有两个信号量集，一个是扫描机，一个是打印机。P1程序占用打印机，P2程序占用扫描机。
   当P1程序在运行的时候想要获取扫描机的信号量，同时P2程序想要在运行的时候获取打印机的信号量的时候。就会发生死锁。

    概括而言。我们可以发现死锁的会有如下共性：

    参与死锁的进程至少有两个
    每个参与死锁的进程都要等待资源
    参与死锁的进程中至少有两个进程占用资源
    可见，死锁之所以产生，是因为每个进程都要竞争资源。由于系统资源不足，并且推进程序不当，因此产生了死锁

"""



"""
    闭包(closure)是函数式编程的重要的语法结构。闭包也是一种组织代码的结构，它同样提高了代码的可重复使用性。

    当一个内嵌函数引用其外部作作用域的变量,我们就会得到一个闭包. 总结一下,创建一个闭包必须满足以下几点:

    必须有一个内嵌函数
    内嵌函数必须引用外部函数中的变量
    外部函数的返回值必须是内嵌函数

    重点是函数运行后并不会被撤销,当函数运行完后,instance并不被销毁,而是继续留在内存空间里.这个功能类似类里的类变量,只不过迁移到了函数上.

    闭包就像个空心球一样,你知道外面和里面,但你不知道中间是什么样.

"""

"""
    分布式任务队列Celery

    在程序运行过程中，要执行一个很久的任务，但是我们又不想主程序被阻塞，常见的方法是多线程。
    可是当并发量过大时，多线程也会扛不住，必须要用线程池来限制并发个数，而且多线程对共享资源的使用也是很麻烦的事情.
    还有是协程，但是协程毕竟还是在同一线程内执行的，如果一个任务本身就要执行很长时间，
    而不是因为等待IO被挂起，那其他协程照样无法得到运行。
    强大的分布式任务队列Celery，它可以让任务的执行同主程序完全脱离，甚至不在同一台主机内。
    它通过队列来调度任务，不用担心并发量高时系统负载过大。
    它可以用来处理复杂系统性能问题，却又相当灵活易用.
    
"""


"""

Python 缓存机制

"""
import datetime
import random

class MyCache:
    """"""
    def __init__(self):
        """Constructor"""
        self.cache = {}
        self.max_cache_size = 10

    def __contains__(self, key):
        """
        根据该键是否存在于缓存当中返回True或者False
        """
        return key in self.cache

    def update(self, key, value):
        """
        更新该缓存字典，您可选择性删除最早条目
        """
        if key not in self.cache and len(self.cache) >= self.max_cache_size:
            self.remove_oldest()
        self.cache[key] = {'date_accessed': datetime.datetime.now(),
                           'value': value}

    def remove_oldest(self):
        """
        删除具备最早访问日期的输入数据
        """
        oldest_entry = None

        for key in self.cache:
            if oldest_entry == None:
                oldest_entry = key
            elif self.cache[key]['date_accessed'] < self.cache[oldest_entry]['date_accessed']:
                oldest_entry = key

        self.cache.pop(oldest_entry)

    @property
    def size(self):
        """
        返回缓存容量大小
        """
        return len(self.cache)

if __name__ == '__main__':
    #测试缓存
    keys = ['test', 'red', 'fox', 'fence', 'junk', \
            'other', 'alpha', 'bravo', 'cal', 'devo', 'ele']
    s = 'abcdefghijklmnop'
    cache = MyCache()
    for i, key in enumerate(keys):
        if key in cache:
            continue
        else:
            value = ''.join([random.choice(s) for i in range(20)])
            cache.update(key, value)
        print("#%s iterations, #%s cached entries" % (i+1, cache.size))



"""

        Mixin

"""
"""
    Mixin，表示混入(mix-in)，它告诉别人，这个类是作为功能添加到子类中，而不是作为父类，它的作用同Java中的接口
        首先它必须表示某一种功能，而不是某个物品，如同Java中的Runnable，Callable等
        其次它必须责任单一，如果有多个功能，那就写多个Mixin类
        然后，它不依赖于子类的实现
        最后，子类即便没有继承这个Mixin类，也照样可以工作，就是缺少了某个功能。（比如飞机照样可以载客，就是不能飞了
"""
class Vehicle(object):
    pass
 
class PlaneMixin(object):
    def fly(self):
        print 'I am flying'
 
class Airplane(Vehicle, PlaneMixin):
    pass



"""
     AsynicI/O
     使用事件循环驱动的协程实现并发.

##Thinking outside the GIL with asnicIO and multiprocessing
###impact 
one binary
fetccch the world
process ecerything
aggregate results
thread pool for IO

###not aging well
scales in time and memeory
runtime now too slow 
underutilizing hardware
ultimately limited by the GIL


###Multiprocessing
scacles of cpu cores
autonatic IPC
poolmaps is really useful
one task per process
beware forking, pickling

###AsyncIO
bease on futures
faster than threads
massive IO conccurrency
processing still limited by GIL
beware timeouts and queue length
"""



"""

    Graph Theory

"""

"""
shortest path
 """
from collections import defaultdict
from heapq import *

def dijkstra(graph_dict, from_node, to_node):
    cost = -1
    Shortest_path=[]
    q, seen = [(0,from_node,())], set()
    while q:
        (cost,v1,path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == to_node: # Find the to_node!!!
                break;
            for v2,c in graph_dict.get(v1, ()):
                if v2 not in seen:
                    heappush(q, (cost+c, v2, path))

    # Check the way to quit 'while' loop
    if v1 != to_node:
        # IF there isn't a path from from_node to to_node, THEN return null!!!
        print("node: %s cannot reach node: %s" %(from_node,to_node))
        cost = -1
        Shortest_path=[]
        return cost,Shortest_path
    else:
        # IF there is a path from from_node to to_node, THEN format the path and return!!!
        left = path[0]
        Shortest_path.append(left)
        right = path[1]
        while len(right)>0:
            left = right[0]
            Shortest_path.append(left)
            right = right[1]
        Shortest_path.reverse()
        
    return cost,Shortest_path

def dijkstra_all(graph_dict):
    Shortest_path_dict = defaultdict(dict)
    for i in nodes:
        for j in nodes:
            if i != j:
                cost,Shortest_path = dijkstra(graph_dict,i,j)
                Shortest_path_dict[i][j] = Shortest_path
                
    return Shortest_path_dict

nodes=['s1','s2','s3','s4','s5','s6']
print("nodes =",nodes)
M=float("inf")
# Describing graph by 2-D list
graph_list = [  
[0,30,15,M,M,M],  
[5,0,M,M,20,30],  
[M,10,0,M,M,15],  
[M,M,M,0,M,M],  
[M,M,M,10,0,M],  
[M,M,M,30,10,0]  
]
print("graph_list = [")
for l in graph_list:
    print(str(l)+",")
print("]\n")

# Describing graph by a list of tuple
graph_edges = []
print ("graph_edges = [")
for i in nodes:
    for j in nodes:
        if i!=j and graph_list[nodes.index(i)][nodes.index(j)]!=M:
            graph_edges.append((i,j,graph_list[nodes.index(i)][nodes.index(j)]))
            print (str((i,j,graph_list[nodes.index(i)][nodes.index(j)]))+", ",end="")
    print()
print("]\n")

# Describing graph by dict
graph_dict = defaultdict(list)
print("graph_dict = {")
for tail,head,cost in graph_edges:
    graph_dict[tail].append((head,cost))
for key in graph_dict:
    print("'%s': %s" %(key, graph_dict[key]))
print("}\n")

print ("----------------Dijkstra----------------")
#from_node = input ("Please input the from_node =  ")
#to_node = input("Please input the to_node = ")
#cost,Shortest_path = dijkstra(graph_dict, from_node, to_node)
#print ('The shortest path = %s, cost = %s'%(Shortest_path,cost))
Shortest_path_dict = dijkstra_all(graph_dict)
print("Shortest_path_dict = {")
for key in Shortest_path_dict:
    print("'%s': %s," %(key, Shortest_path_dict[key]))
print("}")



"""

    setup logging

"""
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    formatter = logging.Formatter(settings.LOG_FORMAT)
    logger = logging.getLogger()
    logger.setLevel(settings.LOG_LEVEL)
    handler = RotatingFileHandler(filename=settings.LOG_FILE, maxBytes=(1048576*5), backupCount=7)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
setup_logging()

def all_settings():
    from types import ModuleType
    settings = {}
    for name, item in globals().iteritems():
        if not callable(item) and not name.startswith("__") and not isinstance(item, ModuleType):
            settings[name] = item
    return settings

"""

    lazy initialize设计模式
    http://www.cnblogs.com/xybaby/p/6280313.html

"""
import functools
class lazy_attribute(object):
    """ A property that caches itself to the class object. """

    def __init__(self, func):
        functools.update_wrapper(self, func, updated=[])
        self.getter = func

    def __get__(self, obj, cls):
        value = self.getter(cls)
        setattr(cls, self.__name__, value)
        return value

class test_lazy(object):
    @lazy_attribute
    def print_dict_string(clz):
        print('print_dict_string is needed now')
        return sum(i*i for i in range(10))

if __name__ == '__main__':
    print(test_lazy.__dict__.get('print_dict_string'))
    test_lazy.print_dict_string
    print(test_lazy.__dict__.get('print_dict_string'))

# __getattr__使得实现adapter wrapper模式非常容易，我们都知道“组合优于继承”，__getattr__实现的adapter就是以组合的形式
# 如果adapter需要修改adapter_ext的行为，那么定义一个同名的属性就行了，其他的想直接“继承”的属性，通通交给__getattr__就行了

class adapter_ext(object):
    def foo(self):
        print('foo in adapter_ext')

    def bar(self):
        print('bar in adapter_ext')

class adapter(object):
    def __init__(self):
        self.adapter_ext = adapter_ext()

    def foo(self):
        print('foo in adapter') 
        self.adapter_ext.foo()

    def __getattr__(self, name):
        return getattr(self.adapter_ext, name)

if __name__ == '__main__':
    a = adapter()
    a.foo()
    a.bar()

"""

    线程锁Lock & ThreadLocal
    对于多线程来说，最大的特点就是线程之间可以共享数据，那么共享数据就会出现多线程同时更改一个变量，使用同样的资源，而出现死锁、数据错乱等情况
    线程锁: 当访问某个资源之前，用Lock.acquire()锁住资源,访问之后，用Lock.release()释放资源
    
    多线程缺陷:
    在Python中，有一个GIL，即全局解释锁，该锁的存在保证在同一个时间只能有一个线程执行任务，也就是多线程并不是真正的并发，只是交替得执行
    假如有10个线程炮在10核CPU上，当前工作的也只能是一个CPU上的线程

    虽然Python多线程有缺陷，但它很适合用在IO密集型任务中
    I/O密集型执行期间大部分是时间都用在I/O上，如数据库I/O，较少时间用在CPU计算上.因此该应用场景可以使用Python多线程
    当一个任务阻塞在IO操作上时，我们可以立即切换执行其他线程上执行其他IO操作请求

"""
## threading.Lock()
import threading
import time

a = 3
lock = threading.Lock()
def target():
    print('the curent threading  %s is running' % threading.current_thread().name)
    time.sleep(2)
    global a #使用global语句可以清楚地表明变量是在外面的块定义的
    lock.acquire()
    try:
        a += 3
    finally:
    #用finally的目的是防止当前线程无线占用资源
        lock.release()
    print('the curent threading  %s is ended' % threading.current_thread().name) 
t = threading.Thread(target=target)
t1 = threading.Thread(target=target)

t.start()
t1.start()
t.join()
t1.join()
print(a)

## threadLocal
v 属性只有本线程可以修改，其他线程不可以
from time import sleep
from random import random
from threading import Thread, local

data = local()

def bar():
    print("I'm called from", data.v)

def foo():
    bar()

class T(Thread):
    def run(self):
        sleep(random())
        data.v = self.getName()   # Thread-1 and Thread-2 accordingly
        sleep(1)
        foo()

T().start()
T().start()

"""==============>>>>>>>>>>>> Desgin Pattern STARTS <<<<<<================="""
"""

    单例模式SINGLETON

"""
def singleton(cls):
    """decorator 方法
    """
    instances ={}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper


@singleton
clss Foo(object):
    pass

foo1 = Foo()
foo2 = Foo()

print(foo1 = foo2)

### metaclass
class Singleton(type):
    """使用元类
    """
    _instance = {}
    def __call__(cls, *arg, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(singleton, cls).__call__(*arg, **kwargs)
        return cls._instance[cls]

# python2
def Foo(object):
    __metaclass__ = Singleton

# python3
class myClass(metaclass=Singleton)
    pass


# __new__ 基类实现
class Singleton(object):
    """new 使用基类
    """
    def __new__(cls, *args, **kwargs):xxx
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

class Foo(object):
    pass

foo1 = Foo()
print(dis.dis(Singleton))
foo2 = Foo()
print(foo1 = foo2)


"""
    抽象工厂模式

    提供一个接口，用于创建 相关的对象家族
    抽象工厂模式创建的是对象家族，也就是很多对象而不是一个对象，并且这些对象是相关的，也就是说必须一起创建出来
    而工厂模式只是用于创建一个对象，这和抽象工厂模式有很大不同

    至于创建对象的家族这一概念是在 Client 体现，Client 要通过 AbstractFactory 同时调用两个方法来创建出两个对象，在这里这两个对象就有很大的相关性，Client 需要同时创建出这两个对象。

"""






"""
    工厂模式:
        它把实例化的操作单独放到一个类中，这个类就成为简单工厂类，让简单工厂类来决定应该用哪个子类来实例化

        这样做能把客户类和具体子类的实现解耦，客户类不再需要知道有哪些子类以及应当实例化哪个子类
        因为客户类往往有多个，如果不使用简单工厂，所有的客户类都要知道所有子类的细节
        而且一旦子类发生改变，例如增加子类，那么所有的客户类都要进行修改

    设计原则:
        依赖倒置原则：要依赖抽象，不要依赖具体类。听起来像是针对接口编程，不针对实现编程，但是这个原则说明了：不能让高层组件依赖底层组件，而且，不管高层或底层组件，两者都应该依赖于抽象

"""



"""

   装饰模式:
   动态地将责任附加到对象上。在扩展功能上，装饰者提供了比继承更有弹性的替代方案
   装饰者（Decorator）和具体组件（ConcreteComponent）都继承自组件（Component)
   具体组件的方法实现不需要依赖于其它对象，而装饰者组合了一个组件，这样它可以装饰其它装饰者或者具体组件
   所谓装饰，就是把这个装饰者套在被装饰上，从而动态扩展被装饰者的功能。
   装饰者的方法有一部分是自己的，这属于它的功能，然后调用被装饰者的方法实现，从而也保留了被装饰者的功能。
   具体组件应当是装饰层次的最低层，因为只有具体组件的方法实现不需要依赖于其它对象

"""



"""

    观察者模式:
    定义了对象之间的一对多依赖，当一个对象改变状态时，它的所有依赖者都会收到通知并自动更新.
    主题（Subject）是被观察的对象，而其所有依赖者（Observer）称为观察者

"""
class Publisher(object):
    """创建一个发布者 Publisher，他是作为事件发布对象的抽象
    创建了一个用于存放所有观察者对象的list,add remove方法用于 新增/移除 观察者对象
    而notify方法就是将由事件触发的消息发送给每个观察者,并调用观察者自己的notify方法进行操作
    这是实现观察者模式的核心
    """ 
    def __init__(self):
        self.observers = list()

    def add(self, observers):
        if observers in self.observers:
            print('fail to add: {}'.format(observers))
        else:
            self.observers.append(observers)

    def remove(self, observers):
        try:
            self.observers.remove(observers)
        except Exception as e:
            print('fail to remove: {}, {}'.format(observers, e))

    def notify(self):
        [o.notify(self) for o in self.observers]

class DefaultFormatter(Publisher):
    """创建一个实际的事件发布对象，这个对象就是事件最初触发的位置
    发布对象需要继承自发布者，并且在__init__方法中要做的第一件事情就是调用基类的__init__方法
    在事件触发的位置，要调用 notify 方法，本例中是对 data 复制的 setter 中调用的，
    如果在事件触发的位置不调用，那么观察者模式就失去了其意义，自然也就不是观察者模式了
    """
    def __init__(self, name):
        Publisher.__init__(self)
        self.name = name
        self._data = 0

    def __str__(self):
        return '{}: "{}" has data = {}'.format(type(self).__name__, self.name, self._data)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_value):
        try:
            self._data = int(new_value)
        except Exception as e:
            print('Error: {}'.format(e))
        else:
            self.notify()

class HexFormatter(object):  
    def notify(self, publisher):
        print("{}: '{}' has now hex data = {}".format(type(self).__name__,publisher.name, hex(publisher.data)))

class BinaryFormatter(object):  
    def notify(self, publisher):
        print("{}: '{}' has now bin data = {}".format(type(self).__name__,publisher.name, bin(publisher.data)))  

def main():  
    df = DefaultFormatter('test1')
    print(df)
    cf = DefaultFormatter('test2')
    print(cf)

    print()
    hf = HexFormatter()
    df.add(hf)
    df.data = 3

    cf.add(hf)
    cf.data = 16
    print(df)
    print(cf)

    print()
    bf = BinaryFormatter()
    df.add(bf)
    df.data = 21
    cf.add(bf)
    cf.data = 16
    print(df)
    print(cf)

    print()
    df.remove(hf)
    df.data = 40
    cf.data = 1024
    print(df)
    print(cf)

    print()
    df.remove(hf)
    df.add(bf)

    df.data = 'hello'
    cf.add(bf)
    print(df)
    print(cf)

    print()
    df.data = 15.8
    print(df)
    cf.data = 32
    print(cf)

if __name__ == '__main__':  
    main()

"""

    class 类装饰器作为方法调用次数校验

"""
class Counter:
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)

@Counter
def foo():
    pass

for i in range(10):
    foo()

print(foo.count)
"""==============>>>>>>>>>>>>  Desgin Pattern ENDS <<<<<<<<<<<<<<<============"""


"""

    "is"  vs  "=="

"is" checks that 2 arguments refer to the same object, "==" checks that 2 arguments have the same value.
is比较的是id是不是一样，==比较的是值是不是一样
每个对象包含3个属性，id，type，value
id就是对象地址，可以通过内置函数id()查看对象引用的地址
type就是对象类型，可以通过内置函数type()查看对象的类型
value就是对象的值
python为了实现对内存的有效利用，对小整数[-5,256]内的整数会进行缓存，不在该范围内的则不会缓存
>>> a = 255
>>> b = 255
>>> a is b
True
>>> c = 257
>>> d = 257
>>> c is d
False

"""

"""

    type 和 isinstance 的比较

    共性:
        - type和instanceof都可以判断变量是否属于某个内建类型
    不同:
        - type可以只接收一个参数，打印其未知的所属的类型；而isinstance只能判断是否属于某个已知类型
        - isinstance可以判断子类对象是否继承于父类；而type不可以

"""
from timeit import timeit
from dis import dis

#用type和isinstance分别判断{'s'}是否属于set类型
def a():return type({'s'})is set
def b():return isinstance({'s'},set)
def c():return type({'s'})==set

time = [timeit(a),timeit(b),timeit(c)]

#打印结果
print('result:\n%s %s %s\n'%(a(),b(),c()))

#打印时间
print('time:\n%s\n'%( ''.join([str(_)+'\n' for _ in time]) )) 

#打印指令
print('orders:\n') 
dis(a)
print( '\n')
dis(b)
print( '\n')
dis(c)


#=============>>>>   Decorator STARTS
# http://python-3-patterns-idioms-test.readthedocs.io/en/latest/PythonDecorators.html#decorators-vs-the-decorator-pattern
# http://blog.xiayf.cn/2013/01/04/Decorators-and-Functional-Python/

"""
    装饰器是可以调用的对象,其参数是另一个函数(被装饰的函数). 装饰器可能会处理被装饰的函数,然后将其返回,
        或者将其替换成另外一个函数或可调用对象.

    除了在装饰器中有用处之外,闭包还是回调式异步编程和函数式编程的基础.

     Pass a function object through another function and assign the result to the original function

     - Using class as a  Decorator:

     Most introductory examples show this as a function, but I’ve found that it’s easier to start understanding decorators by using classes as decoration mechanisms instead of functions. In addition, it’s more powerful.

     The only constraint upon the object returned by the decorator is that it can be used as a function – which basically means it must be callable. Thus, any classes we use as decorators must implement __call__.
    
     Notice that the constructor for my_decorator is executed at the point of decoration of the function. Since we can call f() inside __init__(), it shows that the creation of f() is complete before the decorator is called. Note also that the decorator constructor receives the function object being decorated. Typically, you’ll capture the function object in the constructor and later use it in the __call__() method (the fact that decoration and calling are two clear phases when using classes is why I argue that it’s easier and more powerful this way).

     The reason I think decorators will have such a big impact is because this little bit of syntax sugar changes the way you think about programming. Indeed, it brings the idea of “applying code to other code” (i.e.: macros) into mainstream thinking by formalizing it as a language construct.

"""
class my_decorator(object):

    def __init__(self, f):
        print("inside my_decorator.__init__()")
        f() # Prove that function definition has completed

    def __call__(self):
        print("inside my_decorator.__call__()")

@my_decorator
def aFunction():
    print("inside aFunction()")

print("Finished decorating aFunction()")

aFunction()


"""

    Slightly More Useful

"""
class entry_exit(object):

    def __init__(self, f):
        print("decorator class __init__")
        self.f = f

    def __call__(self):
        print("Entering", self.f.__name__)
        self.f()
        print("Exited", self.f.__name__)

@entry_exit
def func1():
    print("inside func1()")
print("func start ")
func1()

"""

    Using Functions as Decorators

    The only constraint on the result of a decorator is that it be callable, so it can properly replace the decorated function. In the above examples, I’ve replaced the original function with an object of a class that has a __call__() method. But a function object is also callable, so we can rewrite the previous example using a function instead of a class, like this:


"""


#=============<<<<<<<<   Decorator ENDS

"""

    Flask sessions 实现

"""
from flask import Flask, session, redirect, url_for, escape, request

app = Flask(__name__)

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run()


""" ===========>>>>>>>>>> Magic Functions STARTS 
    http://www.cnblogs.com/Jimmy1988/p/6804095.html
"""

"""

    通常情况下，我们在访问类或者实例对象的时候，会牵扯到一些属性访问的魔法方法，主要包括：

    ① __getattr__(self, name): 访问不存在的属性时调用

    ② __getattribute__(self, name)：访问存在的属性时调用（先调用该方法，查看是否存在该属性，若不存在，接着去调用①）

    ③ __setattr__(self, name, value)：设置实例对象的一个新的属性时调用

    ④ __delattr__(self, name)：删除一个实例对象的属性时调用

"""

class Test:
      def __getattr__(self, name):
         print('__getattr__')
 
      def __getattribute__(self, name):
         print('__getattribute__')
 
      def __setattr__(self, name, value):
         print('__setattr__')
 
      def __delattr__(self, name):
         print('__delattr__')

t= Test()
t.x

"""
如上述代码所示，x并不是Test类实例t的一个属性，首先去调用 __getattribute__() 方法，得知该属性并不属于该实例对象；但是，按照常理，t.x应该打印 __getattribute__ 和__getattr__，但实际情况并非如此，为什么呢？难道以上Python的规定无效吗？

 实例对象属性寻找的顺序如下：

① 首先访问 __getattribute__() 魔法方法（隐含默认调用，无论何种情况，均会调用此方法）

② 去实例对象t中查找是否具备该属性： t.__dict__ 中查找，每个类和实例对象都有一个 __dict__ 的属性

③ 若在 t.__dict__ 中找不到对应的属性， 则去该实例的类中寻找，即 t.__class__.__dict__

④ 若在实例的类中也招不到该属性，则去父类中寻找，即 t.__class__.__bases__.__dict__中寻找

⑤ 若以上均无法找到，则会调用 __getattr__ 方法，执行内部的命令（若未重载 __getattr__ 方法，则直接报错：AttributeError)

但是，以上的说法，并不能解释为什么执行 t.x 时，不打印 ’__getattr__'  啊？

问题就出在了步骤的第④步，因为，一旦重载了 __getattribute__() 方法，如果找不到属性，则必须要手动加入第④步，否则无法进入到 第⑤步 (__getattr__)的。

验证一下以上说法是否正确：

方法一：采用object（所有类的基类）
"""
class Test:
      def __getattr__(self, name):
         print('__getattr__')
 
      def __getattribute__(self, name):
         print('__getattribute__')
         object.__getattribute__(self, name)
 
      def __setattr__(self, name, value):
         print('__setattr__')
 
      def __delattr__(self, name):
         print('__delattr__')

t= Test()
t.x


"""
super() 方法
"""
class Test:
      def __getattr__(self, name):
         print('__getattr__')
 
      def __getattribute__(self, name):
         print('__getattribute__')
        #super(Test, self).__getattribute__(name)
# OR
         super().__getattribute__(name)
 
      def __setattr__(self, name, value):
         print('__setattr__')
 
      def __delattr__(self, name):
         print('__delattr__')

t= Test()
t.x
""" ===========<<<<<<<<<< Magic Functions ENDS  """


""" 

     Python类分为两种，一种叫经典类，一种叫新式类。两种都支持多继承。
     
     super figures out which is the next class in the Method Resolution Order. The two arguments you pass in are what lets it figure that out - self gives it the entire MRO via an attribute; the current class tells it where you are along the MRO right now. So what super is actually doing is basically:

    ```
    def super(cls, inst):
        mro = inst.__class__.mro() # Always the most derived class
        return mro[mro.index(cls) + 1]
    ```

    The reason it is the current class rather than the base class is because the entire point of having super is to have a function that works out what that base class is rather than having to refer to it explicitly - which can cause problems if the base class' name changes, if you don't know exactly what the parent class is called (think of factory functions like namedtuple that spit out a new class), and especially in multi-inheritance situations (where the next class in the MRO mightn't be one of the current class' bases).

""" 
# 经典类
class A():
    def __init__(self):
        print('A')

class B(A):
    def __init__(self):
        A.__init__(self)
        print('B')

class C(B, A):
    def __init__(self):
        A.__init__(self)
        B.__init__(self)
        print('C')

c= C()


# 新式类
class A(object):
    def __init__(self):
        print('A')

class B(A):
    def __init__(self):
        super(B, self).__init__()
        print('B')

class C(B, A):
    def __init__(self):
        super(C, self).__init__()
        print('C')

c = C()


# 解决父类不能初始化问题
class Person(object):
    name = ""
    sex = ""
    def __init__(self, name, sex='U'):
        print( 'Person')
        self.name=name
        self.sex=sex

class Consumer(object):
    def __init__(self):
        print('Consumer')
    
class Student(Person, Consumer):
    def __init__(self, score, name):
        print(Student.__bases__)
        super(Student, self).__init__(name, sex='F')
        Consumer.__init__(self)
        self.score=score

s1 = Student(90, 'abc')
print(s1.name, s1.score, s1.sex, s1.__class__.__mro__)


"""

      拦截器

"""

class People(object):

    def __init__(self, age, name):
        self.age = age
        self.name = name

    def __getattribute__(self, obj):
        if obj == 'age':
            print("Age was asked")
            return object.__getattribute__(self, obj)
        elif obj == 'name':
            print('Name was asked')
            return object.__getattribute__(self, obj)
        else:
            return object.__getattribute__(self, obj)

p1 = People(13, 'liam')
print(p1.age)
print(p1.name)


"""

      非切入式访问

"""

class Fjs(object):  

    def __init__(self, name):  
        self.name = name  
  
    def hello(self):  
        print("said by : "+self.name)
  
    def fjs(self, name):  
        if name == self.name:  
            print("yes")  
        else:  
            print("no")
  
class Wrap_Fjs(object):  
    def __init__(self, fjs):  
        self._fjs = fjs  
  
    def __getattr__(self, item):  
        if item == "hello":  
            print("调用hello方法了")
        elif item == "fjs":  
            print("调用fjs方法了")
        return getattr(self._fjs, item)  
  
fjs = Wrap_Fjs(Fjs("fjs"))  
fjs.hello()  
fjs.fjs("fjs")  


"""

     Initialize the logging for IOK installer
     __file__ is not recognized once built into .exe, use getcwd instead.

"""
app_dir = os.getcwd()   # os.path.dirname(os.path.realpath(__file__))
log_dir = '%s\\%s\\' %(app_dir, iok_log_dir)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = log_dir + os.path.basename(sys.argv[0])
log_file = os.path.splitext(log_file)[0] + '.log'
log_file_old = log_file + ".old"

if os.path.exists(log_file):
    if os.path.exists(log_file_old):
        os.remove(log_file_old)
    os.rename(log_file, log_file_old)

logger = logging.getLogger(" PRO NAME ")
log_handler = logging.FileHandler(log_file)
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)


"""
    Verify if an IP is a valid IPv4 address
"""
def valid_ip(address):
    try:
        socket.inet_aton(address)
        return True
    except:
        return False

"""
    Copy directory recursively
"""
def copy_files(src_dir, dst_dir):
    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)

    shutil.copytree(src_dir, dst_dir)

