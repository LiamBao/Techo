[Python 魔术方法指南Link](http://pycoders-weekly-chinese.readthedocs.io/en/latest/issue6/a-guide-to-pythons-magic-methods.html)

- ***\_\_getattr\_\_(self, item):***

- ***\_\_setattr\_\_(self, item, value):***

- ***\_\_getattribute\_\_(self, item):***

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





### Overriding the \_\_new\_\_ method


When subclassing immutable built-in types like numbers and strings, and occasionally in other situations, the static method \_\_new\_\_ comes in handy. \_\_new\_\_ is the first step in instance construction, invoked before \_\_init\_\_. The \_\_new\_\_ method is called with the class as its first argument; its responsibility is to return a new instance of that class. Compare this to \_\_init\_\_: \_\_init\_\_ is called with an instance as its first argument, and it doesn't return anything; its responsibility is to initialize the instance. There are situations where a new instance is created without calling \_\_init\_\_ (for example when the instance is loaded from a pickle). There is no way to create a new instance without calling \_\_new\_\_ (although in some cases you can get away with calling a base class's \_\_new\_\_).

Recall that you create class instances by calling the class. When the class is a new-style class, the following happens when it is called. First, the class's \_\_new\_\_ method is called, passing the class itself as first argument, followed by any (positional as well as keyword) arguments received by the original call. This returns a new instance. Then that instance's \_\_init\_\_ method is called to further initialize it. (This is all controlled by the \_\_call\_\_ method of the metaclass, by the way.)

Here is an example of a subclass that overrides \_\_new\_\_ - this is how you would normally use it.

```
>>> class inch(float):
...     "Convert from inch to meter"
...     def __new__(cls, arg=0.0):
...         return float.__new__(cls, arg*0.0254)
...
>>> print inch(12)
0.3048
>>> 
```

This class isn't very useful (it's not even the right way to go about unit conversions) but it shows how to extend the constructor of an immutable type. If instead of \_\_new\_\_ we had tried to override \_\_init\_\_, it wouldn't have worked:

```
>>> class inch(float):
...     "THIS DOESN'T WORK!!!"
...     def __init__(self, arg=0.0):
...         float.__init__(self, arg*0.0254)
...
>>> print inch(12)
12.0
>>> 
```

The version overriding \_\_init\_\_ doesn't work because the float type's \_\_init\_\_ is a no-op: it returns immediately, ignoring its arguments.

All this is done so that immutable types can preserve their immutability while allowing subclassing. If the value of a float object were initialized by its \_\_init\_\_ method, you could change the value of an existing float object! For example, this would work:

```
>>> # THIS DOESN'T WORK!!!
>>> import math
>>> math.pi.__init__(3.0)
>>> print math.pi
3.0
>>>
```

I could have fixed this problem in other ways, for example by adding an "already initialized" flag or only allowing \_\_init\_\_ to be called on subclass instances, but those solutions are inelegant. Instead, I added \_\_new\_\_, which is a perfectly general mechanism that can be used by built-in and user-defined classes, for immutable and mutable objects.

Here are some rules for \_\_new\_\_:

\_\_new\_\_ is a static method. When defining it, you don't need to (but may!) use the phrase "\_\_new\_\_ = staticmethod(\_\_new\_\_)", because this is implied by its name (it is special-cased by the class constructor).
The first argument to \_\_new\_\_ must be a class; the remaining arguments are the arguments as seen by the constructor call.
A \_\_new\_\_ method that overrides a base class's \_\_new\_\_ method may call that base class's \_\_new\_\_ method. The first argument to the base class's \_\_new\_\_ method call should be the class argument to the overriding \_\_new\_\_ method, not the base class; if you were to pass in the base class, you would get an instance of the base class. (This is really just analogous to passing self to an overridden \_\_init\_\_ call.)
Unless you want to play games like those described in the next two bullets, a \_\_new\_\_ method must call its base class's \_\_new\_\_ method; that's the only way to create an instance of your object. The subclass \_\_new\_\_ can do two things to affect the resulting object: pass different arguments to the base class \_\_new\_\_, and modify the resulting object after it's been created (for example to initialize essential instance variables).
\_\_new\_\_ must return an object. There's nothing that requires that it return a new object that is an instance of its class argument, although that is the convention. If you return an existing object of your class or a subclass, the constructor call will still call its \_\_init\_\_ method. If you return an object of a different class, its \_\_init\_\_ method will not be called. If you forget to return something, Python will unhelpfully return None, and your caller will probably be very confused.
For immutable classes, your \_\_new\_\_ may return a cached reference to an existing object with the same value; this is what the int, str and tuple types do for small values. This is one of the reasons why their \_\_init\_\_ does nothing: cached objects would be re-initialized over and over. (The other reason is that there's nothing left for \_\_init\_\_ to initialize: \_\_new\_\_ returns a fully initialized object.)
If you subclass a built-in immutable type and want to add some mutable state (maybe you add a default conversion to a string type), it's best to initialize the mutable state in the \_\_init\_\_ method and leave \_\_new\_\_ alone.
If you want to change the constructor's signature, you often have to override both \_\_new\_\_ and \_\_init\_\_ to accept the new signature. However, most built-in types ignore the arguments to the method they don't use; in particular, the immutable types (int, long, float, complex, str, unicode, and tuple) have a dummy \_\_init\_\_, while the mutable types (dict, list, file, and also super, classmethod, staticmethod, and property) have a dummy \_\_new\_\_. The built-in type 'object' has a dummy \_\_new\_\_ and a dummy \_\_init\_\_ (which the others inherit). The built-in type 'type' is special in many respects; see the section on metaclasses.
(This has nothing to do to \_\_new\_\_, but is handy to know anyway.) If you subclass a built-in type, extra space is automatically added to the instances to accomodate \_\_dict\_\_ and \_\_weakrefs\_\_. (The \_\_dict\_\_ is not initialized until you use it though, so you shouldn't worry about the space occupied by an empty dictionary for each instance you create.) If you don't need this extra space, you can add the phrase "\_\_slots\_\_ = []" to your class. (See above for more about \_\_slots\_\_.)
Factoid: \_\_new\_\_ is a static method, not a class method. I initially thought it would have to be a class method, and that's why I added the classmethod primitive. Unfortunately, with class methods, upcalls don't work right in this case, so I had to make it a static method with an explicit class as its first argument. Ironically, there are now no known uses for class methods in the Python distribution (other than in the test suite). However, class methods are still useful in other places, for example, to program inheritable alternate constructors.
As another example of \_\_new\_\_, here's a way to implement the singleton pattern.

```
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
```

To create a singleton class, you subclass from Singleton; each subclass will have a single instance, no matter how many times its constructor is called. To further initialize the subclass instance, subclasses should override 'init' instead of \_\_init\_\_ - the \_\_init\_\_ method is called each time the constructor is called. For example:

```
>>> class MySingleton(Singleton):
...     def init(self):
...         print "calling init"
...     def __init___(self):
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
```