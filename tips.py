# -*- coding:utf-8 -*-




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