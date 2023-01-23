---
author: Nathan Vaughn
date: "2023-01-22"
description: "Modern Python tools for modern Python developers: Volume 2"
tags:
  - Python
title: Python Tooling Volume 2
---

## Introduction

Since I've written
["Modern Python tools for modern Python developers"]({{< relref "python-tooling" >}})
I've made a number of changes to my Python workflows as I've discovered and started
using new tools. I want to share these tools to help you potentially improve
your workflow and efficiency

## Tools

Most of my tools are still the same from my previous post, so I'll focus
on the changes I've made.

### Environment Management

First off, let's talk about environment management again. I am still using
[Poetry](https://python-poetry.org), however there are a number of competitors in this
space that do similar things, that I want to discuss.
Pradyun Gedam has a great article on this topic
[here](https://pradyunsg.me/blog/2023/01/21/thoughts-on-python-packaging/),
but I would like to dive a little deeper in some of the tools.

To start, I still think Poetry is a wonderful tool. I think has a very intuitive CLI,
that works the same on every operating system.
`poetry install` installs all the dependencies.
`poetry shell` spawns a shell with the environment already activated.
No need to remember `source .venv/bin/activate` and `.venv\Scripts\activate`.
`poetry run` lets you run a command inside the virtual environment, without having it
activated, for automated situations like CI/CD or Docker.
`poetry build` builds a `.tar.gz` and `.whl` file of your package.
`poetry publish` uploads the package to PyPi.
Additionally, `poetry` has a lock file format that installs the same dependency versions
every time. At my last job, some of our Python applications were being used to make
business decisions, so having reproducible installations was of great concern for us.

However, Poetry has two major pain points. The first is that by default, Poetry
creates virtual environments in its own cache directory, rather than in the same
project directory. While this can be changed, it's annoying, and can cause unexpected
results in CI/CD. The second is Poetry's refusal to follow a number of PEPs
(Python Enhancement Proposal) that are trying to modernize Python packaging around the
`pyproject.toml` file:

- [PEP 508 – Dependency specification for Python Software Packages](https://peps.python.org/pep-0508/)
- [PEP 517 – A build-system independent format for source trees](https://peps.python.org/pep-0517/)
- [PEP 621 – Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
- [PEP 631 – Dependency specification in pyproject.toml based on PEP 508](https://peps.python.org/pep-0631/)
- [PEP 660 – Editable installs for pyproject.toml based builds (wheel based)](https://peps.python.org/pep-0660/)

Two tools that address some of these pain points are:

- [PDM](https://github.com/pdm-project/pdm)
- [Hatch](https://github.com/pypa/hatch)

Both are interesting. Hatch is a semi-official tool that is under the umbrella
of the Python Packaging Authority. It does nearly everything Poetry does and more,
and strictly adheres to Python PEPs. Unfortunately, as of writing, I think it's
strict adherence to Python PEPs makes it not viable. From
[the FAQ](https://hatch.pypa.io/latest/meta/faq/#libraries-vs-applications):

> The only caveat is that currently there is no support for re-creating an
> environment given a set of dependencies in a reproducible manner. Although a
> standard lock file format may be far
> off since [PEP 665](https://peps.python.org/pep-0665/) was rejected, resolving
> capabilities are [coming to pip](https://github.com/pypa/pip/pull/10748).
> When that is stabilized, Hatch will add locking
> functionality and dedicated documentation for managing applications.

So currently, Hatch does not have any sort of lockfile, and therefore, dependency
versions are not guaranteed to be the same. As someone who has had too many things
break due to dependency upgrades, this is a feature I will not go without. I
definitely look forward to the future of Hatch, however. It's ability to create
multiple Python environments like [`tox`](https://tox.wiki/) is a great idea, though
not being able to locate them in the project directory is a major downside.

The other tool, `pdm` takes heavy inspiration from `poetry`, but altered to follow
PEP 517, PEP 621, and experimental support for
[PEP 582](https://www.python.org/dev/peps/pep-0582). Unlike `poetry`, it
creates environments directly in the project directory. It also
has awesome support for a [script system](https://pdm.fming.dev/latest/usage/scripts/),
like `npm`.

The only thingI find missing from `pdm` is a `shell` command like `poetry`. While there
is a third party plugin for it ([pdm-shell](https://github.com/abersheeran/pdm-shell)),
I found (at least on Windows) it doesn't work very well. I think given more time
to mature, `pdm` may become a very enticing `poetry` alternative. It does all the same
things right as `poetry`, but fixes some of the annoyances, and adds even more
features.

### Pre-Commit

The major new tool I've using is [pre-commit](https://pre-commit.com/). While I was
vaguely aware of it before, I never really tried it, nor understood what it could do
for me.

At it's simplest, `pre-commit` is a tool written in Python, that takes a list of
commands, and runs them against files that have changed when you run `git commit`.
This takes advantage of
[`git` hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
to work. While `pre-commit` works with a large number of languages and ecosystems
like `docker`, it primarily seems to be used with Python tools.
`pre-commit` automatically installs every tool in an isolated virtual environment.

To use `pre-commit`, you need to create a `.pre-commit-config.yaml` file
in the root of your repository (`.yaml` versus `.yml` is very important). In this file,
you list hooks you would like to use from `git` repositories like so:

```yaml
repos:
  - hooks:
      - id: check-json
      - id: check-toml
      - id: check-yaml
      - id: check-case-conflict
      - id: trailing-whitespace
      - id: check-merge-conflict
      - id: mixed-line-ending
    repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0

  - hooks:
      - id: absolufy-imports
    repo: https://github.com/MarcoGorelli/absolufy-imports
    rev: v0.3.1
```

`pre-commit` is very picky that `rev` must be an exact commit hash, or tag of the repo.
What `pre-commit` is doing here, is downloading the repository at the specified `rev`,
and reading the `.pre-commit-hooks.yaml` from that repository to configure a virtual
environment.

With your `.pre-commit-config.yaml` file created, you can install `pre-commit` with

```bash
pip install pre-commit
```

and install the `git` hook with

```bash
pre-commit install
```

Now, whenever you run `git commit`, the command `pre-commit run` runs first, which
checks _only the files that have changed_. To check all files, run

```bash
pre-commit run --all-files
```

instead.

What I like so much about `pre-commit`, is that it helps create a single source
of checks that should be run, locally and in CI/CD. In the past, getting my team
members to remember to run the myriad of tools (`black`, `isort`, `autoflake`)
we used to format and check code, before committing was always a pain, and a mistake
I often made myself. This would inevitably result in CI/CD failing for simple
mistakes that could have been caught easily. This frustrates developers, and requires
setting up steps in CI/CD to run all these tools individually, and keeping the
command line option in-sync can often be challenging (looking at you `autoflake`
with no config file).

With `pre-commit`, developers get code checked before every commit, and it's very easy
to create a CI/CD pipeline to run the exact same checks, just in case someone forgets
to run `pre-commit install`:

1. Clone repo
2. Install dependencies
3. Run `pre-commit run --all-files --show-diff-on-failure`

If you're using `poetry`, there's also a plug available to automatically run
`pre-commit install` after `poetry install`:
[poetry-pre-commit-plugin](https://pypi.org/project/poetry-pre-commit-plugin/)

```bash
poetry self add poetry-pre-commit-plugin
```

There are a few downsides with `pre-commit` however. The first and most major one
to me, is updating the tools used is challenging to automate.
Dependabot (my auto-updater of choice since it's built in to GitHub) does not support
it at time of writing:
[dependabot/dependabot-core#1524](https://github.com/dependabot/dependabot-core/issues/1524)

There are a few workarounds. The first one is,
[Renovate](https://docs.renovatebot.com/modules/manager/pre-commit/) does, so if you're
using that, that's fantastic. Additionally, if you use the
[creator's CI service](https://pre-commit.ci/), that also automatically updates
tools for you. The option I have decided to go with is to use a GitHub Action on
a schedule to update the tools and make a pull request. However, this has
the downside, that pull requests created by GitHub Actions, can't then trigger
subsequent GitHub Actions (to prevent infinite loops), so verifying the changes
requires manual effort:

````yaml
# Inspired by: https://browniebroke.com/blog/gh-action-pre-commit-autoupdate/
name: Pre-Commit Update

on:
  workflow_dispatch:
  schedule:
    - cron: 0 8 * * 1

jobs:
  auto-update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          ref: main

      - name: Install pre-commit-update
        run: pip install pre-commit-update

      - name: Run pre-commit-update
        run: pre-commit-update

      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v4
        with:
          token: ${{ github.token }}
          branch: update/pre-commit-update
          title: Update Pre-Commit hooks
          commit-message: Update Pre-Commit hooks
          body: |
            Update versions of tools in pre-commit configs to latest version.
            Please verify the changes locally, as a pull request created by GitHub Actions cannot trigger workflows:
            ```bash
            git fetch
            git checkout update/pre-commit-update
            git pull
            poetry run pre-commit run --all-files
            ```
          labels: dependencies
````

You may notice, I'm also using the third party
[pre-commit-update](https://pypi.org/project/pre-commit-update/) tool,
since I find it works better than the built in `pre-commit autoupdate` command.
[Poetry](https://python-poetry.org/docs/pre-commit-hooks/#why-does-pre-commit-autoupdate-not-update-to-the-latest-version)
in particular conflicts with this built-in command.

### Type Checking

While I'm still using [`pyright`](https://github.com/microsoft/pyright) for
type checking since it's tightly integrated with VS Code, I have started using it
locally through `pre-commit` as well, rather than install it with `npm` and defining
a `package.json` file. This is facilitated by the community
[`pyright` Python package](https://pypi.org/project/pyright/).

```yaml
repos:
  - hooks:
      - id: pyright
    repo: https://github.com/RobertCraigie/pyright-python
    rev: v1.1.289
```

However, since `pre-commit` installs tools into their own virtual environment,
this means `pyright` needs to be told where the _actual_ virtual environment is.
In `pyproject.toml`, add:

```toml
[tool.pyright]
    typeCheckingMode = "basic" # turn on type checking
    venvPath         = "."     # parent venv path
    venv             = ".venv" # venv directory name
```

Additionally, if using Poetry, you also need to force Poetry to create the virtual
environment in your project folder, rather than its normal cache directory. Otherwise,
this will not work in CI/CD, or on other developer's machines.
Add the file `poetry.toml`:

```toml
[virtualenvs]
in-project = true
```

With these settings added, everything will work as you would expect.

### Linting

In the past, I have used `isort` for sorting imports, `autoflake` for removing
unused imports, and `flake8` to lint code. I recently learned about the tool
[`ruff`](https://github.com/charliermarsh/ruff) which basically does all three in one,
with proper `pyproject.toml` support. Probably the best part about it, is that it can
automatically fix a number of issues, like sorting imports (`isort`),
removing unused imports (`autoflake`) and common issues like `var == None`.

Interestingly, like `pyright`, it's not written
in Python. Much like some JavaScript tools, it's written in Rust, so it is way faster
than native Python.

Using it with `pre-commit` is easy, there is a specific repo for it:

```yaml
- hooks:
    - args:
        - --fix
      id: ruff
  repo: https://github.com/charliermarsh/ruff-pre-commit
  rev: v0.0.223
```

There is also a VS Code extension which highlights issues, and helps
automatically fix them:
[https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)

## Conclusion

In conclusion, `pre-commit` makes things so much easier, in having a consistent
local development and CI/CD pipeline experience. While the tools I'm using
largely are the same (`black`, `pyright`, `pyleft`), how I'm using them
got so much easier to manage.

As an example, here's roughly what I would set up with `pre-commit` and GitHub Actions
for pull requests on a Python project:

```yml
repos:
  - hooks:
      - id: check-json
      - id: check-toml
      - id: check-yaml
      - id: check-case-conflict
      - id: trailing-whitespace
      - id: check-merge-conflict
    repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
  - hooks:
      - id: poetry-check
      - args:
          - --no-update
        id: poetry-lock
    repo: https://github.com/python-poetry/poetry
    rev: 1.3.2
  - hooks:
      - id: black
    repo: https://github.com/psf/black
    rev: 22.12.0
  - hooks:
      - args:
          - --fix
        id: ruff
    repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.0.223
  - hooks:
      - id: pyleft
    repo: https://github.com/nathanvaughn/pyleft
    rev: v1.1.4
  - hooks:
      - id: pyright
    repo: https://github.com/RobertCraigie/pyright-python
    rev: v1.1.289
  - hooks:
      - id: markdownlint
    repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.33.0
```

```yml
name: Tests

on:
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    if: "!contains(github.event.head_commit.message, 'ci skip')"

    strategy:
      fail-fast: false
      matrix:
        python_version: ["3.11", "3.10", "3.9", "3.8", "3.7"]

    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Install Poetry
        run: |
          python -m pip install pip wheel pipx --upgrade
          pipx install poetry

      - name: Setup Python ${{ matrix.python_version }}
        uses: actions/setup-python@v4
        with:
          # last version is default
          python-version: |
            3.11
            ${{ matrix.python_version }}
          cache: poetry

      - name: Cache Pre-Commit
        uses: actions/cache@v3
        with:
          path: ~/.cache/pre-commit
          key: pre-commit-${{ hashFiles('.pre-commit-config.yaml') }}
          restore-keys: pre-commit-

      - name: Install Python Dependencies
        run: poetry install --sync

      - name: Run Pre-Commit Checks
        run: poetry run pre-commit run --all-files --color=always --show-diff-on-failure

      - name: Run Tests
        run: poetry run pytest -v
```
