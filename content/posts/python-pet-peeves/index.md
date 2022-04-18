---
author: Nathan Vaughn
date: "2022-04-16"
description: My personal pet peeves when writing Python
tags:
  - Python
title: Python Pet Peeves
---

## Unnecessary Nesting

Something that I see frequently is over-nesting of `if` statements with no
`else` condition. For example, something like ths:

```python
def check(thing):
    if thing is not None:
        do_something1()

        if thing > 0:
            do_something2()

            if thing < 10:
                return True
```

This is a completely made up example, but I see stuff like this far too often.
While it's not _technically_ wrong, it can make things very difficult to read.
Especially as the statements get longer, they can very easily begin to word-wrap
when using a formatter that limits line-length. Because there is no `else` condition
for these `if` statements, it's much cleaner to add an early `return` and not need
to nest as much. A better way to write this would be:

```python
def check(thing):
    if thing is None:
        return

    do_something1()

    if thing <= 0:
        return

    do_something2()

    if thing < 10:
        return True
```

Here, if any of the `if` statements fail, the function simply returns
(exactly as it was doing before, just implicitly), and allows us to not nest things.
While this adds some to the line count, I feel the increase in readability
(especially with a split view) is well worth it.

## == None/True/False

A common source of confusion in Python is the difference between `is` and `==`,
and this causes it to be used incorrectly.

```python
if var == True:
    do_something()
```

The way this could be improved is changing out the `==` operator for `is`.
The difference is, `==` does an equality comparison, while `is` checks
if the the two sides of the expression are the exact same instance of the same object.
For example:

```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int

a = Person("Nathan", 24)
b = Person("Nathan", 24)

a == b # True
a is b # False
```

In this example, `a` and `b` are two different instances of `Person`, but they
are _equal_ to each other, but they are not the same instance.

The reason that `is` is better than `==` for comparing to `True`, `False`, and `None`
is that in Python, `True`, `False`, and `None` are constants that are always
references to the same underlying object. Doing `is` and the instance check is more
efficient than `==` and the equality comparisons required.

## Subprocess shell=True

One final pet peeve of mine is when using the `subprocess` module, is the overuse
of `shell=True`. Generally, this is a bad idea and can make your code
vulnerable to shell injections, and lose cross-platform compatibility.
What does `shell=True` do? It takes the raw command
you give `subprocess.Popen` and runs it in a new shell directly
([`/bin/sh` on POSIX](https://github.com/python/cpython/blob/8560f4a0f288fec33ba49f85bb872353d631a4dc/Lib/subprocess.py#L1714-L1720),
or [`cmd.exe` on Windows](https://github.com/python/cpython/blob/8560f4a0f288fec33ba49f85bb872353d631a4dc/Lib/subprocess.py#L1433-L1437)).
This means that the command is run with no escaping. This can be dangerous
for example,

```python
import subprocess

url = input("Enter a URL: ")
subprocess.Popen(f"curl {url}", shell=True)
```

In this case, if a user enters "https://www.google.com/ && rm -rf /", then
the shell will blindly wipe your entire filesystem. The benefit of turning `shell=True`
off is that you will get proper escaping with your commands. Replace the above example
with

```python
import subprocess

url = input("Enter a URL: ")
subprocess.Popen(["curl", url])
```

and now that vulnerability no longer exists. This also has the benefit that complex
arguments with things like quotes or spaces in them will get handled correctly.
This is because Python is able to natively pass arguments to a program
(like what you get with `sys.argv`) while a shell has to figure that out, usually
using spaces as a delimiter.

For example, echoing back the string:

> "This isn't any easy thing to handle" said my boss.

is fairly easy to do:

```python
import subprocess
subprocess.Popen(["echo", '"This isn\'t any easy thing to handle" said my boss.'])
```

but if you turn on `shell=True`, well, I haven't been able to figure it out myself yet
(though I fully admit I'm not great at bash scripting).

Back to the other point I made earlier, if you're using `shell=True` to take
advantage of things like pipes or redirects, you're making your Python code
only work on that specific platform. It's almost always not too difficult to find
a more Pythonic, cross-platform solution.

For example, to replace a shell redirect, you can use the `stdout` and `stderr`
arguments and give them a file pointer.

```python
import subprocess
with open("output.txt", "w") as fp:
    subprocess.Popen(["echo", "We are the knights who say 'Ni!'"], stdout=fp)
```

If you have a long running command, that's a great way to easily create log
files if it crashes or something.

If you're trying to replicate a pipe, you can capture the output of one process,
and then feed to a second `subprocess` call easily. While no longer being one line,
you get the escaping advantages talked about before.

```python
import subprocess
import json
out = json.loads(subprocess.check_output(["docker", "info", "--format", "{{ json . }}"]))
# do something with `out`
```
