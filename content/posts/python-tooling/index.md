---
author: Nathan Vaughn
cover: img/cover.png
date: "2022-01-01"
description: Modern Python tools for modern Python developers
images:
  - /posts/python-tooling/img/cover.png
tags:
  - Python
title: Python Tooling
userelativecover: true
---

## Introduction

With the new year, I wanted to go over some of my favorite Python tools
that I learned about and used over the past year, and really just describe my
starting point for Python-based projects. If you think:

> Wow, Python is easy to get started with, but taking it seriously is hard.

then I hope this post will help you reconsider. Yes, for a long time Python tooling
was not great, and made using Python outside of small scripts difficult. However,
the community has come a long way in making Python easier to use
in more robust settings.

## Tools

Let's get right into the tools that I've come to love this past year.

### Environment Management

First and foremost, dependency management with Python sucks. `pip` is the default
package manager for Python, that comes with nearly any Python installation, and is
the de facto standard.

The first annoying thing about `pip` is that if you naively run
`pip install <package>`, it will install that package to your
_system-level Python interpreter_. If you you have multiple projects on your machine,
then now you have a mess of dependencies of multiple projects that may conflict with
each other. `npm` for example, will create a `node_modules` folder in the same
directory and install the packages there. With Python, you have to explicitly
create a virtual environment for every single project you want to work on. Thankfully,
Python these days ships with the `venv` module built in, but it's annoying
you have to do this, and even when you use `python -m venv`, activating the virtual
environment command is different for different operating systems.

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux
source .venv/bin/activate
```

Secondly, `pip` is painful to use in a repeatable manner. Let's say you want
to add the [requests](https://pypi.org/project/requests/) package as a dependency to
your project. If you write your `requirements.txt` file like this:

```requirements.txt
requests
```

then every time you run `python -m pip install requirements.txt`, you'll get the
latest version of the requests package every time. This is almost always
not what you want. Every time you build/install/distribute code, dependencies should be
the exact same, **always**. I've lost track the number of times version updates
of dependencies have broken my program, because I wasn't careful in pinning version
numbers.

So, to fix this, you write your `requirements.txt` file like this:

```requirements.txt
requests==2.26.0
```

Now, you're closer, but requests depends on 4 other packages. So while you'll get
the same version of requests every time, you may get different versions of its
dependencies, depending on how requests specifies its dependency versions. While
closer, you now need to write your `requirements.txt` file like this to capture
everything:

```requirements.txt
requests==2.26.0
certifi==2021.10.8
charset-normalizer==2.0.9
idna==3.3
urllib3==1.26.7
```

You can see how this can become a nightmare, especially if you ever actually want to
update one of your dependencies.

Most sane package managers (such as `npm` shockingly enough), use two separate files
to track dependencies. One for the top-level project dependencies, and then a lock
file which has the exact version of every dependency and sub-dependency. `pip`
has no such concept of this.

[`pipenv`](https://pipenv.pypa.io/en/latest/)
is an attempt to remedy these problems, and gets close,
but man, long story short, it sucks to use. Super slow, doesn't work with
cross-platform teams (as in, generating a lock file on Windows versus Linux
will often yield different results), and an unintuitive CLI. I find instead, that
[`poetry`](https://python-poetry.org/) works really well for this.

`poetry` is sort of an all-in-one replacement for `pip`, `venv` and the `setup.py`
file. You create a `pyproject.toml` file (the new de facto standard for the Python
community on project configuration) with information similar to the following:

```toml
# project information
[tool.poetry]
name = "pyleft"
version = "1.0.0"
description = "Python type annotation existence checker"
license = "MIT"
readme = "README.md"
homepage = "https://github.com/NathanVaughn/pyleft"
repository = "https://github.com/NathanVaughn/pyleft.git"
authors = ["Nathan Vaughn <nthnv.me/email>"]
classifiers = [
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Software Development :: Quality Assurance",
]

# dependencies along with supported Python versions
[tool.poetry.dependencies]
python = ">=3.6.2,<4.0"
toml = ">=0.10.0,<1"
pathspec = ">=0.9.0, <1"

# development dependencies
[tool.poetry.dev-dependencies]
pytest = "^6.2.4"
black = "^21.9b0"
isort = "^5.9.3"

# needed to compile as a package
[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

Then you can run `poetry install` to automatically create a virtual environment
and install all dependencies. Run `poetry shell` to activate the virtual environment,
or `poetry update` to update dependencies to the latest version with your version
specifier. If you want to build a package, just run `poetry build` with no need
to faff around with a confusing `setup.py` file.
Publishing to PyPi is just `poetry publish`.

For me, it's really been a game-changer for dependency management and makes
life so much easier.

Two tips for using `poetry`:

1. By default, `poetry` will create virtual environments in a cache directory.
   I prefer to keep them in the same directory as the project,
   so run `poetry config virtualenvs.in-project true` to enable this.
2. Poetry always wants to install things in a virtual environment.
   When running anything automated, especially on disposable systems,
   this is annoying and you must prefix every `python` command with `poetry run`.
   A much easier way is to run `poetry config virtualenvs.create false`
   to disable virtual environment creation.
   Additionally, you can also do `poetry export -o requirements.txt` to export
   the dependencies to a `pip` requirements file you can install with
   `python -m pip install -r requirements.txt`. This is really helpful especially
   with Docker.

### Testing

There's not a ton to say about testing with Python.
I like [`pytest`](https://pypi.org/project/pytest/) and have been using it for years.
However, a great addition to `pytest` is the
[`pytest-cov`](https://pypi.org/project/pytest-cov) plugin.
Once you install it, just add a couple options to you `pytest` command to create a
coverage report.

A simple

```bash
pytest
```

becomes

```bash
pytest --cov=. --cov-report=html --cov-branch --cov-context=test
```

To get full branch and context shown in the HTML report, you need to add

```toml
[tool.coverage.html]
show_contexts = true
```

to your `pyproject.toml` file.

You can add these options to your `pyproject.toml` file as well so you don't
have to remember them.

```toml
[tool.pytest.ini_options]
addopts = "--cov=. --cov-report=html --cov-branch --cov-context=test"
```

### Static Analysis

Besides running your code, there is also a lot that can be analyzed statically,
without needing to execute a single line.

#### Formatting

I'm a stickler about code formatting. I generally don't care what it is,
I just want it to be consistent. I also want to be to more or less hit "format"
in my editor and have all my code magically fixed. For Python, there is one excellent
tool for this: [`black`](https://pypi.org/project/black/). `black` is a Python code
formatter based on the Henry Ford quote:

> A customer can have a car painted any color that he wants, so long as it is black.

`black` has almost no formatting options other than line length, and it's fantastic.
However, `black` doesn't really do anything about the imports in your Python code.
For that, we need two more tools.

The first is [`isort`](https://pypi.org/project/isort/). `isort` really only does one
thing, and that is to take your imports, group them by type
(standard library, first-party, third-party) and then alphabetize them.

For example, this:

```python
import os
import local.module

import json
import requests
```

would become:

```python
import json
import os

import requests

import local.module
```

However, `isort` doesn't have the power to remove unused imports for you. The second
tool for that is [`autoflake`](https://pypi.org/project/autoflake/). `autoflake`
is able to automatically remove unused imports and variables. Unfortunately `autoflake`
doesn't support any sort of config file at all, so all options must be specified
via the CLI.

With the combination of those three tools, no matter how terribly you write your code,
it will come out cleaned up every time.
This is generally what I do in CI in my projects to enforce formatting:

```bash
# install packages
python -m pip install black isort autoflake
# first, run black to format
python -m black .
# now, sort the imports
python -m isort . --profile black
# finally, remove unused imports
python -m autoflake . --in-place --recursive --remove-all-unused-imports
```

If feasible, I then have the changes committed back to the branch, or add
`--check` to each command to make it fail if there any differences.

#### Type Checking

Python type hinting is something I've already talked about a great deal
[here]({{< relref "python-type-hinting" >}}) but in short, it's a fantastic way
to check for issues in your code without needing to execute it.
For this, I like to use [`pyright`](https://github.com/microsoft/pyright).

While `pyright` does a great job at checking type hints for any issues,
it doesn't actually check to make sure that all your type hints _exist_.
I like to require 100% type hinting in my code repos, and it's easy
to accidentally forget them, so I made the tool
[`pyleft`](https://pypi.org/project/pyleft) to help with this.

`pyleft` doesn't check if type hints are correct, it just makes sure they are there.
For example:

```bash
> pyleft .
- tests\files\fail_1.py
        Argument 'two' of function 'add:1' has no type annotation
- tests\files\fail_2.py
        Function 'add:1' has no return type annotation
- tests\files\fail_3.py
        Function 'drive:2' has no return type annotation
- tests\files\fail_4.py
        Argument 'one' of function 'wheels:4' has no type annotation
```

Combined with `pyright` or even [`mypy`](https://pypi.org/project/mypy),
this is a great way to check that your code is fully type checked.

#### Linting

Last but not least is linting. While all of the above helps manage dependencies,
run tests, validate formatting, and ensure type safety, the last piece of the puzzle
is ensuring best practices through linting. I'll be honest, I'm not super sold on this
still. I feel like I spend a lot more time hitting "ignore" than it brings value.
Especially tools like `bandit`, which, last I tried, would complain about
web requests being insecure, even with a hardcoded URL. However, for now
I've been using [`flake8`](https://pypi.org/project/flake8/) to help
check for easy things like using `== None` instead of the better `is None`.

**However**, `flake8` inexplicably doesn't support `pyproject.toml` files. To get
around this, I've used [`pyproject-flake8`](https://pypi.org/project/pyproject-flake8/)
as a wrapper around `flake8` to support `pyproject.toml` files.
To support `black` formatting, I add the following ignores:

```toml
[tool.flake8]
ignore = "E501,W503"
```

Then to run, use `pflake8` instead of `flake8`:

```bash
> pflake8 .
.\PCC\GUI\app.py:61:9: E722 do not use bare 'except'
```

## Conclusion

In conclusion, Python tooling has come a long way. As an example, here's roughly
what I would set up in GitHub Actions for pull requests on a Python project:

```yml
name: Tests

on:
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        # whatever Python versions you choose to support
        python_version: ["3.10", "3.9", "3.8", "3.7", "3.6"]

    steps:
      - name: Checkout Code
        uses: actions/checkout@v2

      - name: Setup Python ${{ matrix.python_version }}
        uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python_version }}

      - name: Setup Poetry
        uses: Gr1N/setup-poetry@v7

      - name: Configure Poetry
        run: poetry config virtualenvs.create false

      - name: Install Python Dependencies
        run: poetry install

      - name: Run Tests
        run: pytest -v

  formatting:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v2

      # latest supported version is probably best
      - name: Setup Python 3.10
        uses: actions/setup-python@v2
        with:
          python-version: "3.10"

      - name: Setup Poetry
        uses: Gr1N/setup-poetry@v7

      - name: Configure Poetry
        run: poetry config virtualenvs.create false

      - name: Install Python Dependencies
        run: poetry install

      - name: Run Black
        run: python -m black pyleft/ --check

      - name: Run Isort
        run: python -m isort pyleft/ --profile black --check

      - name: Run Autoflake
        run: python -m autoflake pyleft/ --recursive --remove-all-unused-imports --check

  type-checking:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v2

      # run on the lowest supported version
      - name: Setup Python 3.6
        uses: actions/setup-python@v2
        with:
          python-version: "3.6"

      - name: Setup Poetry
        uses: Gr1N/setup-poetry@v7

      - name: Configure Poetry
        run: poetry config virtualenvs.create false

      - name: Install Python Dependencies
        run: poetry install

      - name: Install Pyright
        run: npm install pyright

      - name: Run Pyright
        run: npx pyright pyleft/

      - name: Run Pyleft
        run: python -m pyleft pyleft/

  linting:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v2

      # latest supported version is probably best
      - name: Setup Python 3.10
        uses: actions/setup-python@v2
        with:
          python-version: "3.10"

      - name: Setup Poetry
        uses: Gr1N/setup-poetry@v7

      - name: Configure Poetry
        run: poetry config virtualenvs.create false

      - name: Install Python Dependencies
        run: poetry install

      - name: Run Pflake8
        run: python -m pflake8 pyleft/
```

This is just a starting point, and can be modified to fit your project.
There's a lot of things you can do like adding caching, uploading code coverage,
using a private package registry, make slower jobs like tests run after
the formatting has passed, etc. It also shouldn't be too hard to port
to other CI systems such as Azure Pipelines or GitLab.

Hopefully this has helped you rethink how to manage your Python projects
and maintain code quality. As an example, I recommend looking at my
[`pyleft`](https://github.com/NathanVaughn/pyleft) project which features
all of this in action, and is pretty small and digestible.