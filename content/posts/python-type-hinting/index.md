---
author: Nathan Vaughn
date: "2021-07-01"
description: Take your Python code to the next level with type hints
tags:
- VS Code
- Python
- Microsoft
title: Python Type Hinting
userelativecover: true
---

# What is Type Hinting

Python is a dynamically typed language. This basically means that a variable
can be any type (a `float`, `str`, `dict` etc.) and can change at any time. 

```python
var = 123
var = "spam"
```

Generally in compiled languages like C, a variable can only ever be one type, and
your compiler will refuse to compile your code if this isn't followed.

```c
int var;
var = 123
var = "spam"
// this will cause a compilation error
```

While this provides a ton of flexibility and makes Python easy to pick up and use,
this can often hide issues in your code that will only appear at runtime.

```python
def add_two(val):
    return val + 2

add_two("eggs")
# perfectly valid Python code
```

```bash
> python temp.py
Traceback (most recent call last):
  File "temp.py", line 4, in <module>
    add_two("eggs")
  File "temp.py", line 2, in add_two 
    return val + 2
TypeError: can only concatenate str (not "int") to str
```

Static analysis tools can't really help either, as they would effectively have
to execute your code in order to check for any issues. 

To help alleviate this pain, with Python 3.5, Python
introduced the concept of type hinting. These are basically annotations in your
code that help static analysis tools check for errors before they occur, by indicating
what types a variable is expected to be.

# Basic Usage

Taking our example from before, the function expects a variable that is a number,
and returns a new number. With type hints, this looks like:

```python
def add_two(val: float) -> float:
    return val + 2

add_two("eggs")
```

Now if we run a static analysis tool such as
[`pyright`](https://github.com/microsoft/pyright) 
(the engine behind [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)),
we can see our protentional type issue (of adding a number to a string)
while never having to actually execute our code.

```bash
# output shortened for clarity
> pyright temp.py
...
temp.py
  temp.py:4:9 - error: Argument of type "Literal['eggs']" cannot be assigned to parameter "val" of type "float" in function "add_two"
    "Literal['eggs']" is incompatible with "float" (reportGeneralTypeIssues)
1 error, 0 warnings, 0 infos
```

Great! Now if we change the function call to use a number, we get no errors.

```python
def add_two(val: float) -> float:
    return val + 2

add_two(123)
```
```bash
> pyright temp.py
...
0 error, 0 warnings, 0 infos
```

Even though the type hint is a `float` and `123` is an `int`, `pyright` is smart
enough to know that this is fine, as an `int` can always be turned into a `float`.

# Multiple Types

Now, what if we have a function that can accept multiple types? 
Take a look at this more complicated example:

```python
from typing import Union

def print_info(data: Union[str, dict]) -> None:
    if isinstance(data, str):
        print(f"Given data is {data}")
    elif isinstance(data, dict):
        print("Given data is:")
        for key, value in data.items():
            print(f"{key}: {value}")

print_info("spam") # Given data is spam
print_info({"foo": "bar"}) # Given data is:
                           # foo: bar
```

In this example, there are a lot of things going on. First, `typing.Union` with 
square brackets is how we specify that an argument may be any of the given types.
Additionally, now the return type hint is `None` as the function doesn't return any
values. While this isn't strictly necessary, as a lack of a `return` statement 
implies None, I like to add it to be more explicit. So what happens if we run `pyright`?

```bash
> pyright temp.py
...
0 error, 0 warnings, 0 infos
```

Once again, no errors. This also shows another interesting thing. `pyright` is smart 
enough to realize that code nested under `isinstance()` restricts the variable
to be of that type. Without this intelligence, it would complain that in the line
`for key, value in data.items():`, `data` could be a string and does not have an
`.items()` method.

# Any

Now let's say your function doesn't have different `print` statements based
on the type of the variable, it can handle anything. This can conveniently be typed
with `typing.Any`.

```python
from typing import Any

def print_info(data: Any) -> None:
    print(f"Given data is {data}")

print_info("spam") # Given data is spam
print_info({"foo": "bar"}) # Given data is {"foo": "bar"}
```

This tells your type checker that literally any type is a valid input. Use with caution,
but this is safe to use for functions that just print something, 
or convert it to a string, since any Python variable should be able to do 
this[[1]](#footnotes).

# Overloads

Let's say your function doesn't return `None`, but rather returns the type it was given.
You would think that you would put a `Union` on the argument and another `Union` 
on the return value, like so.

```python
from typing import Union

def return_data(data: Union[str, dict]) -> Union[str, dict]:
    return data

return_data("spam")
return_data({"foo": "bar"})
```

While on a surface level this looks okay, and `pyright` doesn't raise any errors,
you'll quickly get type errors if you try to do something with the return data.

```python
from typing import Union

def return_data(data: Union[str, dict]) -> Union[str, dict]:
    return data

a = return_data("spam")
print(a[1:4]) # pam
b = return_data({"foo": "bar"})
print(b["foo"]) # bar
```

```bash
> pyright temp.py
...
temp.py
  temp.py:9:7 - error: Argument of type "Literal['foo']" cannot be assigned to parameter "i" of type "int | slice" in function "__getitem__"
    Type "Literal['foo']" cannot be assigned to type "int | slice"
      "Literal['foo']" is incompatible with "int"
      "Literal['foo']" is incompatible with "slice" (reportGeneralTypeIssues)
1 error, 0 warnings, 0 infos 
```

While the error is pretty confusing, what's really happening is that `pyright` knows
that the output of `return_data` can be either a `str` OR a `dict`. So on line 9, where
we get the key `"foo"` from a `dict`, `pyright` is also considering the possibility
that you're trying to slice a string (like line 7) with another string, 
which is not allowed.

To fix this, we use `typing.overload` and a bit of syntactic sugar to tie the input
type to the output type.

```python
from typing import overload, Union

@overload
def return_data(data: str) -> str: ...

@overload
def return_data(data: dict) -> dict: ...

def return_data(data: Union[str, dict]) -> Union[str, dict]:
    return data

a = return_data("spam")
print(a[1:4]) # pam
b = return_data({"foo": "bar"})
print(b["foo"]) # bar
```

```bash
> pyright temp.py
...
0 error, 0 warnings, 0 infos
```

Note here that you still need to create a `Union` in the actual function declaration
with all the possible input types.

# Literals

Next, how about a function that only accepts a specific list of arguments?
You don't want to put a blanket `float` or `str` type, so you can be more specific
with `typing.Literal`[[2]](#footnotes).

```python
from typing import Literal

def process(mode: Literal["choice1", "choice2"]) -> None:
    if mode == "choice1":
        print("Green eggs and SPAM")
    elif mode == "choice2":
        print("Green eggs and ham")

process("choice1")
process("choice3")
```

```bash
> pyright temp.py
...
temp.py
  temp.py:10:9 - error: Argument of type "Literal['choice3']" cannot be assigned to parameter "mode" of type "Literal['choice1', 'choice2']" in function "process"
    Type "Literal['choice3']" cannot be assigned to type "Literal['choice1', 'choice2']"
      "Literal['choice3']" cannot be assigned to type "Literal['choice1']"
      "Literal['choice3']" cannot be assigned to type "Literal['choice2']" (reportGeneralTypeIssues)
1 error, 0 warnings, 0 infos
```

You can see that `Literal` acts a built-in `Union`. You don't need to do 
`Union[Literal["choice1"], Literal["choice2"]]`.

# Classes

You're also completely free to use a class as a type hint:

```python
class Car:
    def __init__(self) -> None:
        self.tank = 0

def add_gas(car: Car) -> None:
    car.tank += 20

car = Car()
add_gas(car)
print(car.tank) # 20
```

However, in some cases (mainly in return types), the variable for a type hint
may actually be defined *after* the type hint itself, which causes an issue.
Type hints are evaluated before code is ever executed, so you can run into possible
`NameError`s for undefined variables. 
A simple demonstration of this is to flip the order of the function and class:

```python
def add_gas(car: Car) -> None:
    car.tank += 20

class Car:
    def __init__(self) -> None:
        self.tank = 0

car = Car()
add_gas(car)
print(car.tank) # 20
```

```bash
> python temp.py
Traceback (most recent call last):
  File "temp.py", line 1, in <module>
    def add_gas(car: Car) -> None:
NameError: name 'Car' is not defined
```

`pyright` reports the same error as well:

```bash
> pyright temp.py 
...
temp.py
  temp.py:1:18 - error: "Car" is not defined (reportUndefinedVariable)
1 error, 0 warnings, 0 infos
```

Thankfully, there's an easy fix without needing to reorganize your code. Option 1,
is to wrap the type hint with quotes to make it a string. This way, Python
has nothing to execute, while a type checker knows to still look for a class matching
the string (this is why you must use `typing.Literal` for actual strings).

```python
def add_gas(car: "Car") -> None:
```

The second and preferred option is to add 

```python
from __future__ import annotations
```

to your file(s). This effectively tells Python to evaluate type hints *later*, so the
class name will able to be resolved after the file has been parsed.

One last thing about classes. If your class is in a different file, and you're
only importing it for the sake of type hinting, you can place the import inside
a check for `typing.TYPE_CHECKING`:

```python
# car.py
class Car:
    def __init__(self) -> None:
        self.tank = 0
```

```python
# gas_station.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from car import Car

def add_gas(car: Car) -> None:
    car.tank += 20
```

This is a magic variable which is always `False` when code is run by the Python
interpreter, but `True` for type checkers. This is a great way to be able to
type hint functions without actually needing to import other files.

# Variables

Thus far, we've been talking about how to type hint function arguments 
and return values. What about type hinting variables or class attributes? 
Well, you can do that with the same `:` syntax before the assignment of the variable
or attribute. This is great to help prevent accidentally changing the type 
of a variable to something unexpected.

```python
from typing import Union

class Car:
    def __init__(self) -> None:
        self.model: str = "5000"

    def set_model(self, model: Union[str, int]) -> None:
        self.model = model
```

```bash
> pyright temp.py
...
temp.py
  temp.py:8:14 - error: Cannot assign member "model" for type "Car"
    Expression of type "str | int" cannot be assigned to member "model" of class "Car"
      Type "str | int" cannot be assigned to type "str"
        "int" is incompatible with "str" (reportGeneralTypeIssues)
1 error, 0 warnings, 0 infos
```

If you don't like that syntax, you can do the same thing with a `# type: <hint>` comment
at the end of the line.

```python
# these are functionally the same
self.model : str = "5000"
self.model = "5000" # type: str
```

# Overrides

Sometimes, you can't avoid that `pyright` is just wrong about something, or that 
some 3rd party library isn't typed correctly. This is a bit of a contrived
example, but here's such an instance:

```python
# based on this example:
# http://docs.peewee-orm.com/en/latest/peewee/quickstart.html#model-definition
import peewee as pw

db = pw.SqliteDatabase("people.db")

class Person(pw.Model):
    name = pw.CharField()
    age = pw.FloatField()

    class Meta:
        database = db

person = Person(name="Nathan", age=99)

temp_age: float
temp_age = float(person.age)
```

```bash
> pyright temp.py
...
0 errors, 0 warnings, 0 infos 
```

{{< figure src="img/peewee-float.png" alt="Type 'FloatField' cannot be assigned to type 'SupportsFloat | SupportsIndex | str | bytes | bytearray'" caption="Strangely, this only occurs in VS Code for me, and not the command-line `pyright` tool" >}}

In reality, this works fine, but `pyright` isn't having it. Often, putting something like

```python
assert isinstance(var, float)
# or
assert var is not None
```

in the proceeding lines works great, but in this case, `person.age` is not a float,
but a database `FloatField` which pretends to be a float. The only solution
I've found to get the warning to go away is to add the comment `type: ignore` to the
end of the line.

```python
temp_age = float(person.age) # type: ignore
```

Use with great caution, as this effectively hide all warnings of any kind from Pylance
or `pyright` for that line. I generally consider this a last resort as nearly always,
I've typed something poorly, or there is a legitimate possible bug.

# Red Squiggly Driven Development

Hopefully by now, you can see the value of type hinting your Python code. Now,
trying to make sure your code doesn't have any possible type issues in a large codebase
can be a bit difficult. You could click through every single file in 
VS Code with Pylance, *or* you could setup an automated job to check every pull request
or commit as part of testing. `pyright` already returns an exit code of `0`
for no issues, and other values for problems. This makes it work great for 
CI (continuous integration) where an exit code of non-zero is almost always 
considered a failure.

You can pretty easily install the `pyright` tool with `npm`. You will need to also
install all of your Python requirements as well.

GitHub Actions example:
```yml
name: Type Checking

on:
  workflow_dispatch:
  pull_request:
    branches:
      - main

jobs:
  type-checking:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v2

      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          # whatever Python version you want to use
          python-version: 3.9

      - name: Install requirements
        run: python -m pip install -r requirements.txt

      - name: Install pyright
        run: sudo npm install -g pyright
        # specific node version doesn't matter, even the oldest node installed
        # on the latest Ubuntu agents is new enough for pyright

      - name: Run pyright
        run: pyright
```

Azure Pipelines example:
```yml
trigger: none
pr:
- main

pool:
  vmImage: ubuntu-latest

steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.9'
  displayName: Setup Python

- script: python -m pip install -r requirements.txt
  displayName: Install requirements

- script: sudo npm install -g pyright
  displayName: Install pyright 

- script: pyright
  displayName: Run pyright
```

With these CI workflows, this achieves what I like to call, 
"Red Squiggly Driven Development". Instead of say, 
"[Test Driven Development](https://en.wikipedia.org/wiki/Test-driven_development)" or
"Hype Driven Development", pull requests cannot be merged until all red squiggles 
have been removed 
(see [my previous post]({{< relref "vs-code-extensions#python-type-hint" >}}) 
for how to turn on the red squiggles).

# Caveats

To begin with, type hints are nothing but mere suggestions. The Python interpreter
does nothing to actually enforce them, they are solely for the sake of the programmer.
If you are interested in strict typing in Python, the 
[Pydantic](https://pydantic-docs.helpmanual.io/) package is quite interesting.
You can create class objects with strictly typed attributes, or add a decorator
to your existing functions to strictly type them as well.

Additionally, type checking is only as good as the type hints that you, the programmer,
write. If you're lazy and don't write type hints for your functions, there's (currently)
no way for a type checker to be able to validate that there won't be able any 
type issues.

```python
def add_two(val):
    return val + 2

add_two("eggs")
```

```bash
> pyright temp.py
...
0 errors, 0 warnings, 0 infos 
```

Lastly, but most annoyingly, you may have to interact with certain libraries, 
(particularly ones based on auto-generated code)
*cough* 
[protobuf](https://github.com/protocolbuffers/protobuf/issues/2638#issuecomment-495003625) 
*cough*
that don't support type-hints, which can make working with them a hell 
of `# type: ignore` statements. If you're determined, you can create 
[stub files](https://google.github.io/pytype/developers/type_stubs.html)[[3]](#footnotes)
that define the type hints, or find a library that does it for you 
(for example, [mypy-protobuf](https://github.com/dropbox/mypy-protobuf)).

# Conclusion

This is really just scratching the surface of type hinting. There's a ton of tricks,
and lots of different ways you can type hint stuff for more complex functions
and data structures. I highly recommend looking through the 
[`typing` library documentation](https://docs.python.org/3/library/typing.html) 
to learn more. For example, you can use 
[`typing.NewType`](https://docs.python.org/3/library/typing.html#newtype) to make
"pseudo" types which can be helpful for things like units. Or 
[`typing.TypedDict`](https://docs.python.org/3/library/typing.html#typing.TypedDict)
to type very specific dictionary formats.

I truly hope this helps improve your Python code and make you a better programmer.
It certainly has helped me reduce the errors in my code without needing to 
actually run it.

# Footnotes

1. Yes, in some extremely rare cases, this is not the case. One would have to override
   the `__str__` or `__repr__` functions of the type's class to raise an exception.
2. Only available in Python 3.8+, 
   though [typing-extensions](https://pypi.org/project/typing-extensions/) helps
   backport this functionality to older versions.
3. [Ironic](https://tenor.com/view/ironic-starwars-chode-gif-5274592) that Google
   has an article explaining the benefits of static type analysis for Python, 
   but their own protobuf library doesn't support it.
