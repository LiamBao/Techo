# -*- coding:utf-8 -*-




"""

 "is"  vs  "=="

"""
# "is" checks that 2 arguments refer to the same object, "==" checks that 2 arguments have the same value.
# is比较的是id是不是一样，==比较的是值是不是一样
# 每个对象包含3个属性，id，type，value
# id就是对象地址，可以通过内置函数id()查看对象引用的地址
# type就是对象类型，可以通过内置函数type()查看对象的类型
# value就是对象的值
# python为了实现对内存的有效利用，对小整数[-5,256]内的整数会进行缓存，不在该范围内的则不会缓存
# >>> a = 255
# >>> b = 255
# >>> a is b
# True
# >>> c = 257
# >>> d = 257
# >>> c is d
# False


"""

    type 和 isinstance 的比较

    共性:
        - type和instanceof都可以判断变量是否属于某个内建类型
    不同:
        - type可以只接收一个参数，打印其未知的所属的类型；而isinstance只能判断是否属于某个已知类型
        - isinstance可以判断子类对象是否继承于父类；而type不可以

"""
# from timeit import timeit
# from dis import dis

# #用type和isinstance分别判断{'s'}是否属于set类型
# def a():return type({'s'})is set
# def b():return isinstance({'s'},set)
# def c():return type({'s'})==set

# time = [timeit(a),timeit(b),timeit(c)]

# #打印结果
# print('result:\n%s %s %s\n'%(a(),b(),c()))

# #打印时间
# print('time:\n%s\n'%( ''.join([str(_)+'\n' for _ in time]) )) 

# #打印指令
# print('orders:\n') 
# dis(a)
# print( '\n')
# dis(b)
# print( '\n')
# dis(c)


#=============>>>>   Decorator STARTS
# http://python-3-patterns-idioms-test.readthedocs.io/en/latest/PythonDecorators.html#decorators-vs-the-decorator-pattern
# http://blog.xiayf.cn/2013/01/04/Decorators-and-Functional-Python/

"""

     Pass a function object through another function and assign the result to the original function

     - Using class as a  Decorator:

     Most introductory examples show this as a function, but I’ve found that it’s easier to start understanding decorators by using classes as decoration mechanisms instead of functions. In addition, it’s more powerful.

     The only constraint upon the object returned by the decorator is that it can be used as a function – which basically means it must be callable. Thus, any classes we use as decorators must implement __call__.
    
     Notice that the constructor for my_decorator is executed at the point of decoration of the function. Since we can call f() inside __init__(), it shows that the creation of f() is complete before the decorator is called. Note also that the decorator constructor receives the function object being decorated. Typically, you’ll capture the function object in the constructor and later use it in the __call__() method (the fact that decoration and calling are two clear phases when using classes is why I argue that it’s easier and more powerful this way).

     The reason I think decorators will have such a big impact is because this little bit of syntax sugar changes the way you think about programming. Indeed, it brings the idea of “applying code to other code” (i.e.: macros) into mainstream thinking by formalizing it as a language construct.

"""
# class my_decorator(object):

#     def __init__(self, f):
#         print("inside my_decorator.__init__()")
#         f() # Prove that function definition has completed

#     def __call__(self):
#         print("inside my_decorator.__call__()")

# @my_decorator
# def aFunction():
#     print("inside aFunction()")

# print("Finished decorating aFunction()")

# aFunction()


"""

    Slightly More Useful

"""
# class entry_exit(object):

#     def __init__(self, f):
#         print("decorator class __init__")
#         self.f = f

#     def __call__(self):
#         print("Entering", self.f.__name__)
#         self.f()
#         print("Exited", self.f.__name__)

# @entry_exit
# def func1():
#     print("inside func1()")
# print("func start ")
# func1()

"""

    Using Functions as Decorators

    The only constraint on the result of a decorator is that it be callable, so it can properly replace the decorated function. In the above examples, I’ve replaced the original function with an object of a class that has a __call__() method. But a function object is also callable, so we can rewrite the previous example using a function instead of a class, like this:


"""


#=============<<<<<<<<   Decorator ENDS

"""

    Flask sessions 实现

"""
# from flask import Flask, session, redirect, url_for, escape, request

# app = Flask(__name__)

# @app.route('/')
# def index():
#     if 'username' in session:
#         return 'Logged in as %s' % escape(session['username'])
#     return 'You are not logged in'

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         session['username'] = request.form['username']
#         return redirect(url_for('index'))
#     return '''
#         <form action="" method="post">
#             <p><input type=text name=username>
#             <p><input type=submit value=Login>
#         </form>
#     '''

# @app.route('/logout')
# def logout():
#     # remove the username from the session if it's there
#     session.pop('username', None)
#     return redirect(url_for('index'))

# # set the secret key.  keep this really secret:
# app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# if __name__ == '__main__':
#     app.run()


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

# class Test:
#       def __getattr__(self, name):
#          print('__getattr__')
 
#       def __getattribute__(self, name):
#          print('__getattribute__')
 
#       def __setattr__(self, name, value):
#          print('__setattr__')
 
#       def __delattr__(self, name):
#          print('__delattr__')

# t= Test()
# t.x

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
# class Test:
#       def __getattr__(self, name):
#          print('__getattr__')
 
#       def __getattribute__(self, name):
#          print('__getattribute__')
#          object.__getattribute__(self, name)
 
#       def __setattr__(self, name, value):
#          print('__setattr__')
 
#       def __delattr__(self, name):
#          print('__delattr__')

# t= Test()
# t.x


"""
super() 方法
"""
# class Test:
#       def __getattr__(self, name):
#          print('__getattr__')
 
#       def __getattribute__(self, name):
#          print('__getattribute__')
#         #super(Test, self).__getattribute__(name)
# # OR
#          super().__getattribute__(name)
 
#       def __setattr__(self, name, value):
#          print('__setattr__')
 
#       def __delattr__(self, name):
#          print('__delattr__')

# t= Test()
# t.x
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
# class A():
#     def __init__(self):
#         print('A')

# class B(A):
#     def __init__(self):
#         A.__init__(self)
#         print('B')

# class C(B, A):
#     def __init__(self):
#         A.__init__(self)
#         B.__init__(self)
#         print('C')

# c= C()


# 新式类
# class A(object):
#     def __init__(self):
#         print('A')

# class B(A):
#     def __init__(self):
#         super(B, self).__init__()
#         print('B')

# class C(B, A):
#     def __init__(self):
#         super(C, self).__init__()
#         print('C')

# c = C()


# 解决父类不能初始化问题
# class Person(object):
#     name = ""
#     sex = ""
#     def __init__(self, name, sex='U'):
#         print( 'Person')
#         self.name=name
#         self.sex=sex

# class Consumer(object):
#     def __init__(self):
#         print('Consumer')
    
# class Student(Person, Consumer):
#     def __init__(self, score, name):
#         print(Student.__bases__)
#         super(Student, self).__init__(name, sex='F')
#         Consumer.__init__(self)
#         self.score=score

# s1 = Student(90, 'abc')
# print(s1.name, s1.score, s1.sex, s1.__class__.__mro__)


"""

      拦截器

"""

# class People(object):

#     def __init__(self, age, name):
#         self.age = age
#         self.name = name

#     def __getattribute__(self, obj):
#         if obj == 'age':
#             print("Age was asked")
#             return object.__getattribute__(self, obj)
#         elif obj == 'name':
#             print('Name was asked')
#             return object.__getattribute__(self, obj)
#         else:
#             return object.__getattribute__(self, obj)

# p1 = People(13, 'liam')
# print(p1.age)
# print(p1.name)


"""

      非切入式访问

"""

# class Fjs(object):  

#     def __init__(self, name):  
#         self.name = name  
  
#     def hello(self):  
#         print("said by : "+self.name)
  
#     def fjs(self, name):  
#         if name == self.name:  
#             print("yes")  
#         else:  
#             print("no")
  
# class Wrap_Fjs(object):  
#     def __init__(self, fjs):  
#         self._fjs = fjs  
  
#     def __getattr__(self, item):  
#         if item == "hello":  
#             print("调用hello方法了")
#         elif item == "fjs":  
#             print("调用fjs方法了")
#         return getattr(self._fjs, item)  
  
# fjs = Wrap_Fjs(Fjs("fjs"))  
# fjs.hello()  
# fjs.fjs("fjs")  
