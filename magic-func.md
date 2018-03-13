- ***__getattr__(self, item):***

- ***__setattr__(self, item, value)***:

- ***__getattribute__(self, item)***:

```
## Interceptor
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

```





### Overriding the __new__ method


When subclassing immutable built-in types like numbers and strings, and occasionally in other situations, the static method __new__ comes in handy. __new__ is the first step in instance construction, invoked before __init__. The __new__ method is called with the class as its first argument; its responsibility is to return a new instance of that class. Compare this to __init__: __init__ is called with an instance as its first argument, and it doesn't return anything; its responsibility is to initialize the instance. There are situations where a new instance is created without calling __init__ (for example when the instance is loaded from a pickle). There is no way to create a new instance without calling __new__ (although in some cases you can get away with calling a base class's __new__).

Recall that you create class instances by calling the class. When the class is a new-style class, the following happens when it is called. First, the class's __new__ method is called, passing the class itself as first argument, followed by any (positional as well as keyword) arguments received by the original call. This returns a new instance. Then that instance's __init__ method is called to further initialize it. (This is all controlled by the __call__ method of the metaclass, by the way.)

Here is an example of a subclass that overrides __new__ - this is how you would normally use it.

>>> class inch(float):
...     "Convert from inch to meter"
...     def __new__(cls, arg=0.0):
...         return float.__new__(cls, arg*0.0254)
...
>>> print inch(12)
0.3048
>>> 
This class isn't very useful (it's not even the right way to go about unit conversions) but it shows how to extend the constructor of an immutable type. If instead of __new__ we had tried to override __init__, it wouldn't have worked:

>>> class inch(float):
...     "THIS DOESN'T WORK!!!"
...     def __init__(self, arg=0.0):
...         float.__init__(self, arg*0.0254)
...
>>> print inch(12)
12.0
>>> 
The version overriding __init__ doesn't work because the float type's __init__ is a no-op: it returns immediately, ignoring its arguments.

All this is done so that immutable types can preserve their immutability while allowing subclassing. If the value of a float object were initialized by its __init__ method, you could change the value of an existing float object! For example, this would work:

>>> # THIS DOESN'T WORK!!!
>>> import math
>>> math.pi.__init__(3.0)
>>> print math.pi
3.0
>>>
I could have fixed this problem in other ways, for example by adding an "already initialized" flag or only allowing __init__ to be called on subclass instances, but those solutions are inelegant. Instead, I added __new__, which is a perfectly general mechanism that can be used by built-in and user-defined classes, for immutable and mutable objects.

Here are some rules for __new__:

__new__ is a static method. When defining it, you don't need to (but may!) use the phrase "__new__ = staticmethod(__new__)", because this is implied by its name (it is special-cased by the class constructor).
The first argument to __new__ must be a class; the remaining arguments are the arguments as seen by the constructor call.
A __new__ method that overrides a base class's __new__ method may call that base class's __new__ method. The first argument to the base class's __new__ method call should be the class argument to the overriding __new__ method, not the base class; if you were to pass in the base class, you would get an instance of the base class. (This is really just analogous to passing self to an overridden __init__ call.)
Unless you want to play games like those described in the next two bullets, a __new__ method must call its base class's __new__ method; that's the only way to create an instance of your object. The subclass __new__ can do two things to affect the resulting object: pass different arguments to the base class __new__, and modify the resulting object after it's been created (for example to initialize essential instance variables).
__new__ must return an object. There's nothing that requires that it return a new object that is an instance of its class argument, although that is the convention. If you return an existing object of your class or a subclass, the constructor call will still call its __init__ method. If you return an object of a different class, its __init__ method will not be called. If you forget to return something, Python will unhelpfully return None, and your caller will probably be very confused.
For immutable classes, your __new__ may return a cached reference to an existing object with the same value; this is what the int, str and tuple types do for small values. This is one of the reasons why their __init__ does nothing: cached objects would be re-initialized over and over. (The other reason is that there's nothing left for __init__ to initialize: __new__ returns a fully initialized object.)
If you subclass a built-in immutable type and want to add some mutable state (maybe you add a default conversion to a string type), it's best to initialize the mutable state in the __init__ method and leave __new__ alone.
If you want to change the constructor's signature, you often have to override both __new__ and __init__ to accept the new signature. However, most built-in types ignore the arguments to the method they don't use; in particular, the immutable types (int, long, float, complex, str, unicode, and tuple) have a dummy __init__, while the mutable types (dict, list, file, and also super, classmethod, staticmethod, and property) have a dummy __new__. The built-in type 'object' has a dummy __new__ and a dummy __init__ (which the others inherit). The built-in type 'type' is special in many respects; see the section on metaclasses.
(This has nothing to do to __new__, but is handy to know anyway.) If you subclass a built-in type, extra space is automatically added to the instances to accomodate __dict__ and __weakrefs__. (The __dict__ is not initialized until you use it though, so you shouldn't worry about the space occupied by an empty dictionary for each instance you create.) If you don't need this extra space, you can add the phrase "__slots__ = []" to your class. (See above for more about __slots__.)
Factoid: __new__ is a static method, not a class method. I initially thought it would have to be a class method, and that's why I added the classmethod primitive. Unfortunately, with class methods, upcalls don't work right in this case, so I had to make it a static method with an explicit class as its first argument. Ironically, there are now no known uses for class methods in the Python distribution (other than in the test suite). However, class methods are still useful in other places, for example, to program inheritable alternate constructors.
As another example of __new__, here's a way to implement the singleton pattern.

class Singleton(object):
    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwds)
        return it
    def init(self, *args, **kwds):
        pass
To create a singleton class, you subclass from Singleton; each subclass will have a single instance, no matter how many times its constructor is called. To further initialize the subclass instance, subclasses should override 'init' instead of __init__ - the __init__ method is called each time the constructor is called. For example:

>>> class MySingleton(Singleton):
...     def init(self):
...         print "calling init"
...     def __init__(self):
...         print "calling __init__"
... 
>>> x = MySingleton()
calling init
calling __init__
>>> assert x.__class__ is MySingleton
>>> y = MySingleton()
calling __init__
>>> assert x is y
>>> 