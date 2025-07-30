# aspyx

![Pylint](https://github.com/andreasernst/aspyx/actions/workflows/pylint.yml/badge.svg)
![Build Status](https://github.com/andreasernst/aspyx/actions/workflows/ci.yml/badge.svg)


## Table of Contents

- [Introduction](#aspyx)
- [Registration](#registration)
  - [Class](#class)
  - [Class Factory](#class-factory)
  - [Method](#method)
- [Environment](#environment)
  - [Definition](#definition)
  - [Retrieval](#retrieval)
- [Lifecycle methods](#lifecycle-methods)
- [Post Processors](#post-processors)
- [Custom scopes](#custom-scopes)
- [AOP](#aop)
- [Configuration](#configuration)

# Introduction

Aspyx is a small python libary, that adds support for both dependency injection and aop.

The following features are supported 
- constructor injection
- method injection
- post processors
- factory classes and methods
- support for eager construction
- support for singleton and reuqest scopes
- possibilty to add custom scopes
- lifecycle events methods
- bundling of injectable object sets by environment classes including recursive imports and inheritance
- container instances that relate to environment classes and manage the lifecylce of related objects
- hierarchical environments

Let's look at a simple example

```python
from aspyx.di import injectable, on_init, on_destroy, environment, Environment


@injectable()
class Foo:
    def __init__(self):
        pass

    def hello(msg: str):
        print(f"hello {msg}")


@injectable()  # eager and singleton by default
class Bar:
    def __init__(self, foo: Foo): # will inject the Foo dependency
        self.foo = foo

    @on_init() # a lifecycle callback called  after the constructor
    def init(self):
        ...


# this class will register all - specifically decorated - classes and factories in the own module
# In this case Foo and Bar

@environment()
class SampleEnvironment:
    # constructor

    def __init__(self):
        pass


# go, forrest

environment = SampleEnvironment(Configuration)

bar = env.get(Bar)
bar.foo.hello("Andi")
```

The concepts should be pretty familiar , as well as the names which are a combination of Spring and Angular names :-)

Let's add some aspects...

```python
@advice
class SampleAdvice:
    def __init__(self):
        pass

    @before(methods().named("hello").of_type(Foo))
    def callBefore(self, invocation: Invocation):
        print("before Foo.hello(...)")

    @error(methods().named("hello").of_type(Foo))
    def callError(self, invocation: Invocation):
        print("error Foo.hello(...)")
        print(invocation.exception)

    @around(methods().named("hello"))
    def callAround(self, invocation: Invocation):
        print("around Foo.hello()")

        return invocation.proceed()
```

The invocation parameter stores the complete context of the current execution, which are
- the method
- args
- kwargs
- the result
- the possible caught error

Let's look at the details

# Registration

Different mechanisms are available that make classes eligible for injection

## Class

Any class annotated with `@injectable` is eligible for injection

**Example**: 

```python
@injectable()
class Foo:
    def __init__(self):
        pass
```
 Please make sure, that the class defines a constructor, as this is required to determine injected instances. 

 The constructor can only define parameter types that are known as well to the container! 


 The decorator accepts the keyword arguments
 - `eager=True` if `True`, the container will create the instances automatically while booting the environment
 - `scope="singleton"` defines how often instances will be created. `singleton` will create it only once - per environment -, while `request` will recreate it on every injection request

 Other scopes can be defined. Please check the corresponding chapter.

## Class Factory

Classes that implement the `Factory` base class and are annotated with `@factory` will register the appropriate classes returned by the `create` method.

**Example**: 
```python
@factory()
class TestFactory(Factory[Foo]):
    def __init__(self):
        pass

    def create(self) -> Foo:
        return Foo()
```

As in `@injectable`, the same arguments are possible.

## Method 

Any `injectable` can define methods decorated with `@create()`, that will create appropriate instances.

**Example**: 
```python
@injectable()
class Foo:
    def __init__(self):
        pass

    @create(scope="request")
    def create(self) -> Baz:
        return Baz()
```

 The same arguments as in `@injectable` are possible.

# Environment

## Definition

An `Environment` is the container that manages the lifecycle of objects. The set of classes and instances is determined by a constructor argument that controls the class registry.

**Example**: 
```python
@environment()
class SampleEnvironment:
    def __init__(self):
        pass

environment = Environment(SampleEnvironment)
```

The default is that all eligible classes, that are implemented in the containing module or in any submodule will be managed.

By adding an `imports: list[Type]` parameter, specifying other environment types, it will register the appropriate classes recursively.

**Example**: 
```python
@environment()
class SampleEnvironmen(imports=[OtherEnvironment])):
    def __init__(self):
        pass
```

Another possibility is to add a parent environment as an `Environment` constructor parameter

**Example**: 
```python
rootEnvironment = Environment(RootEnvironment)
environment = Environment(SampleEnvironment, parent=rootEnvironment)
```

The difference is, that in the first case, class instances of imported modules will be created in the scope of the _own_ environment, while in the second case, it will return instances managed by the parent.

The method

```shutdown()```

is used when a container is not needed anymore. It will call any `on_destroy()` of all created instances.

## Retrieval

```python
def get(type: Type[T]) -> T
```

is used to retrieve object instances. Depending on the respective scope it will return either cached instances or newly instantiated objects.

The container knows about class hierarchies and is able to `get` base classes, as long as there is only one implementation. 

In case of ambiguities, it will throw an exception.

Please be aware, that a base class are not _required_ to be annotated with `@injectable`, as this would mean, that it could be created on its own as well. ( Which is possible as well, btw. ) 

# Lifecycle methods

It is possible to declare methods that will be called from the container
- `@on_init()` 
   called after the constructor and all other injections.
- `@on_destroy()` 
   called after the container has been shut down

# Post Processors

As part of the instantiation logic it is possible to define post processors that execute any side effect on newly created instances.

**Example**: 
```python
@injectable()
class SamplePostProcessor(PostProcessor):
    def process(self, instance: object, environment: Environment):
        print(f"created a {instance}")
```

Any implementing class of `PostProcessor` that is eligible for injection will be called by passing the new instance.

Please be aware, that a post processor will only handle instances _after_ its _own_ registration.

As injectables within a single file will be handled in the order as they are declared, a post processor will only take effect for all classes after its declaration!

# Custom scopes

As explained, available scopes are "singleton" and "request".

It is easily possible to add custom scopes by inheriting the base-class `Scope`, decorating the class with `@scope(<name>)` and overriding the method `get`

```python
def get(self, provider: AbstractInstanceProvider, environment: Environment, argProvider: Callable[[],list]):
```

Arguments are:
- `provider` the actual provider that will create an instance
- `environment`the requesting environment
- `argPovider` a function that can be called to compute the required arguments recursively

**Example**: The simplified code of the singleton provider ( disregarding locking logic )

```python
@scope("singleton")
class SingletonScope(Scope):
    # constructor

    def __init__(self):
        super().__init__()

        self.value = None

    # override

    def get(self, provider: AbstractInstanceProvider, environment: Environment, argProvider: Callable[[],list]):
        if self.value is None:
            self.value = provider.create(environment, *argProvider())

        return self.value
```

# AOP

It is possible to define different Aspects, that will be part of method calling flow. This logic fits nicely in the library, since the DI framework controls the instantiation logic and can handle aspects within a regular post processor. 

Advice classes need to be part of classes that add a `@advice()` decorator and can define methods that add aspects.

```python
@advice()
class SampleAdvice:
    def __init__(self):  # could inject dependencies
        pass

    @before(methods().named("hello").of_type(Foo))
    def callBefore(self, invocation: Invocation):
        # arguments: invocation.args
        print("before Foo.hello(...)")

    @error(methods().named("hello").of_type(Foo))
    def callError(self, invocation: Invocation):
        print("error Foo.hello(...)")
        print(invocation.exception)

    @around(methods().named("hello"))
    def callAround(self, invocation: Invocation):
        print("around Foo.hello()")

        return invocation.proceed()  # will leave a result in invocation.result or invocation.exception in case of an exception
```

Different aspects - with the appropriate decorator - are possible:
- `before`  
   methods that will be executed _prior_ to the original method
- `around`  
   methods that will be executed _around_ to the original method giving it the possibility add side effects or even change the parameters.
- `after`  
    methods that will be executed _after_ to the original method
- `error`  
   methods that will be executed in case of a caught exception, which can be retrieved by `invocation.exception`

All methods are expected to hava single `Invocation` parameter, that stores, the function, args and kwargs, the return value and possible exceptions.

It is essential for `around` methods to call `proceed()` on the invocation, which will call the next around method in the chain and finally the original method.
If the `proceed` is called with parameters, they will replace the original parameters! 

The arguments to the corresponding decorators control, how aspects are associated with which methods.
A fluent interface is used describe the mapping. 
The parameters restrict either methods or classes and are constructed by a call to either `methods()` or `classes()`.

Both add the fluent methods:
- `of_type(type: Type)`  
   defines the matching classes
- `named(name: str)`  
   defines method or class names
- `matches(re: str)`  
   defines regular expressions for methods or classes
- `decorated_with(type: Type)`  
   defines decorators on methods or classes

The fluent methods `named`, `matches` and `of_type` can be called multiple timess!

# Configuration 

It is possible to inject configuration values, by decorating methods with `@value(<name>)` given a configuration key.

```python
@injectable()
class Foo:
    def __init__(self):
        pass

    @value("OS")
    def inject_value(self, os: str):
        ...
```

This concept relies on a central object `ConfigurationManager` that stores the overall configuration values as provided by so called configuration sources that are defined as follows.

```python
class ConfigurationSource(ABC):
    def __init__(self, manager: ConfigurationManager):
        manager._register(self)
        pass

    @abstractmethod
    def load(self) -> dict:
        pass
```

The `load` method is able to return a tree-like structure by returning a `dict`.

As a default environment variables are already supported.

Other sources can be added dynamically by just registering them.

```python
@injectable()
class SampleConfigurationSource(ConfigurationSource):
    # constructor

    def __init__(self, manager: ConfigurationManager):
        super().__init__(manager)


    def load(self) -> dict:
        return {
            "a": 1, 
            "b": {
                "d": "2", 
                "e": 3, 
                "f": 4
                }
            }
```




      

