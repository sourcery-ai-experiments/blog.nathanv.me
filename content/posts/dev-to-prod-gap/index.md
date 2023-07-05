---
author: Nathan Vaughn
date: "2023-07-05"
description: Making your dev environment more closely resemble production/CI
tags:
  - CI/CD
  - GitHub Actions
  - Python
  - VS Code
  - GitHub Actions
title: Closing the dev-to-prod gap
---

## Background

At [my last job](https://nathanv.me/work-experience/bell-flight/), buzzwords were used
constantly. One of the many that was used a lot was "closing the sim-to-real gap".
This referred (I think) to how make simulators as close to real-life as possible.
While in the context of flight simulators, I tend to think it's silly,
one thing I feel passionately about is making a software development
environment as close to the real thing as possible.

Differences between a local
development environment and where code is actually deployed or tested always causes
problems. CI/CD jobs fail while it worked fine on your machine, missing dependencies
in one environment, or differing versions of libraries wrecking havoc.
Since this a purely software problem with (hopefully!) no physical forces acting
on the developer, this is far more achievable problem to solve.
Today I want to go over 3 tools I have been using lately to close the gap between
my development environment and production and CI/CD.

## Pre-Commit

I've [talked about this before]({{< relref "python-tooling-vol-2/#pre-commit" >}})
so I won't repeat too much here. Basically, [pre-commit](https://pre-commit.com/)
allows you to easily set up tasks that must run before a commit can be made.
Everything is configured in a single YAML file, and can easily be run locally
and in CI/CD with the command `pre-commit run --all-files`.

This is really awesome for things like enforcing formatting, preventing checked-in
merge conflicts, checking for trailing whitespace, static analysis, etc.
There's an entire library of pre-made hooks available
[here](https://pre-commit.com/hooks.html) and it's pretty straight forward to
create your own in a variety of languages.

For me, this has helped considerably standardize formatting. While I'm a big
believer in enforcing consistent formatting in a codebase, remembering to always run
formatting before committing and pushing code was a constant challenge.
And even if I _did_ remember, sometimes I would forget command line options
(some tools I loved completely lacked any configuration file support).
So then I'd inevitably write a script to do that, but if it was in Bash, then it
wouldn't really work on Windows, so I'd convert it to Python, and whoops! I re-invented
the same thing but worse.

### Example

`.pre-commit-config.yaml`

```yaml
default_language_version:
  python: python3.11
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
    rev: 1.5.1
  - hooks:
      - id: black
    repo: https://github.com/psf/black
    rev: 23.3.0
  - hooks:
      - args:
          - --fix
        id: ruff
    repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.0.275
  - hooks:
      - id: pyleft
    repo: https://github.com/nathanvaughn/pyleft
    rev: v1.2.2
  - hooks:
      - id: pyright
    repo: https://github.com/RobertCraigie/pyright-python
    rev: v1.1.316
  - hooks:
      - id: markdownlint
    repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.35.0
```

```powershell
$ pre-commit run --all-files
check json...............................................................Passed
check toml...............................................................Passed
check yaml...............................................................Passed
check for case conflicts.................................................Passed
trim trailing whitespace.................................................Passed
check for merge conflicts................................................Passed
poetry-check.............................................................Passed
poetry-lock..............................................................Passed
black....................................................................Passed
ruff.....................................................................Passed
pyleft...................................................................Passed
pyright..................................................................Passed
markdownlint.............................................................Passed
```

## Dev Containers

[Dev Containers](https://containers.dev/) are the most game-changing development
in the last few years for software development, in my opinion. To explain why, I'd like
to tell a story.

Right before Dev Containers were being integrated in VS Code and were really a thing, a
coworker and myself were being contracted as DevOps engineers to a large defense
company. One of the problems this defense company faced was that they had a group
of third-party contractors that worked on the codebase for this project.
These third parties were contributing drivers and interfaces for their hardware
devices. This defense company did not specify a standardized development environment
to their contractors. They only gave them some vague outlines like
"we use Boost, it runs on Linux, ... and make sure it compiles with GCC!".

One week before a major test event, all the third parties were brought together
to merge their code together.

{{< video src="vid/git-merge.mp4" alt="Git merge" >}}

All hell broke loose. Every third party had a different interpretation of what the
development environment should be. Some used CentOS, others used various versions Ubuntu,
and I'm pretty sure one did all of their work on Windows in Visual Studio with Comic
Sans on a purple background. Every single one
of these "environments" had a different version of `gcc` and much of the code
wouldn't compile on the other versions of `gcc` that the other third parties were using.

My coworker and I got called in to unravel the mess and _rapidly_.

What we did was give all the third parties a version of the Docker container
we were working on for deployment and packaging of the software. This was a Linux
distribution with every package and library needed to compile and run the software
with a **pinned** version number. We then made a script to easily launch
the container with the repository bind-mounted in. We told all the third parties:

> Use this to do your development work. If your code compiles here, it will
> compile when we package and deploy the software.

Once that got sorted out, we made another container using the development image
as the base, copied in the code, and basically just ran `make`.
From then on out, we had no more problems with compiler versions,
code not compiling, and we looked like heros.

All of this is to say [Dev Containers](https://containers.dev/) is an actual
proper specification to do the same thing, and is not something two people hacked
together in a very panicked week. VS Code natively supports it, and there
is a GitHub Action and Azure Pipelines Task available as well:
[https://github.com/devcontainers/ci](https://github.com/devcontainers/ci).

As described in my story, a smart way to structure containers is to have your
production image be the same or based on the development image. This is a great
way to have the same environment no matter where code is developed/tested/run.
I understand this does not always make sense. As always, discretion is required.

Lastly, another good way to use Dev Containers is for development environments
that are not cross-platform, or have lots of dependencies. For example,
I worked on a web app that was a Python monolith. Python was obviously required,
Node was required for some of the frontend assets, and Java was also needed
for some of the AWS emulation tools. Getting 3 runtimes installed was always a pain,
so a Dev Container was an amazing way to easily get everything set up and repeatedly.
I use Dev Containers like this to compile [PX4](https://px4.io) which requires
lot of Linux-only ARM compilers:
[https://github.com/bellflight/AVR-PX4-Firmware/blob/main/.devcontainer/devcontainer.json](https://github.com/bellflight/AVR-PX4-Firmware/blob/main/.devcontainer/devcontainer.json)

### Example

Here is a quick example.

`.devcontainer/devcontainer.json`

```json
{
  "build": {
    "dockerfile": "Dockerfile"
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "actboy168.tasks",
        "charliermarsh.ruff",
        "christian-kohler.path-intellisense",
        "cschlosser.doxdocgen",
        "davidanson.vscode-markdownlint",
        "eamodio.gitlens",
        "github.vscode-github-actions",
        "gruntfuggly.todo-tree",
        "jeff-hykin.better-cpp-syntax",
        "matepek.vscode-catch2-test-adapter",
        "ms-azuretools.vscode-docker",
        "ms-python.python",
        "ms-vscode.cpptools-extension-pack",
        "ms-vscode.cpptools",
        "njpwerner.autodocstring",
        "ue.alphabetical-sorter"
      ]
    }
  }
}
```

GitHub Actions Workflow file

```yaml
name: Build & Test

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]

jobs:
  build-and-test:
    name: Build & Test
    runs-on: ubuntu-latest
    if: "${{ !contains(github.event.head_commit.message, 'ci skip') }}"

    steps:
      - uses: actions/checkout@v3

      - name: Build
        uses: devcontainers/ci@v0.3
        with:
          runCmd: |
            cmake -B build/ -DCMAKE_BUILD_TYPE=${{ inputs.build_type }}
            cmake --build build/ -j
```

## VS Code Task Runner

One day, [my good friend](https://mwrona.com) was telling me about
how he likes using [VS Code Tasks](https://code.visualstudio.com/docs/editor/tasks)
to run common build commands. After looking at his CI/CD configuration, I realized
he had the exact same commands laid out there as well. This made me think, why
do we have to type this out twice? I thought about options:

- Makefiles: As a Python person, I find the syntax confusing, and they really only work on Linux.
- [Task](https://taskfile.dev/): This looks pretty cool, but it's still something
  I have to figure out how to install repeatedly and get into PATH. My experiences
  with [protoc](https://grpc.io/docs/protoc-installation/) have shown me
  how frustrating this can be. And still, this would require another configuration file.
- Other language-specific tools like npm: Michael in particular was working on a
  C++ project. I write a lot of Python, and Python doesn't have a de facto option
  either.

The `.vscode/tasks.json` file seemed like a good enough option. I already liked using
it, it has a lot of features and dependency system, and with extensions like
[actboy168.tasks](https://marketplace.visualstudio.com/items?itemName=actboy168.tasks)
you can get handy buttons in the editor to run tasks.

Microsoft has said they won't add functionality to run VS Code tasks programmatically
in [microsoft/vscode#112594](https://github.com/microsoft/vscode/issues/112594).
I was only able to find [one project](https://github.com/cmccandless/vstask)
that tried to do the same thing, but it is pretty limited and only supports running
tasks with Bash. So like any developer procrastinating on other projects,
I decided to write my own.

I created [vscode-task-runner](https://github.com/NathanVaughn/vscode-task-runner)
which can be easily installed with pip or [pipx](https://pypa.github.io/pipx/).
I recommend reading the GitHub page for a full explanation of usage, but the
jist is that you can run tasks with the `vtr` command followed by the task label(s).

```bash
vtr pre-commit tests
```

I tried to implement as much of the same functionality from VS Code as
I felt reasonable. This required a lot of digging through the VS Code source code.
It turns out escaping characters in a variety of different shells is a nightmarish
endeavour, and I did **not** want to reinvent the wheel here. As someone who
writes as little Javascript as I can, this was a challenge. Thankfully
ChatGPT became very useful for converting some of the Typescript code into Python.
Additionally, some of the documentation Microsoft has on the VS Code website
is different from what VS Code _really_ does. VS Code tended to be
more lenient than described, so I tried to as closely replicate the leniency.

Overall, I'm super pleased with how it turned out. It's now super easy
to run the same commands reliably on my computer and in CI/CD.

### Example

`.vscode/tasks.json`

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "install",
      "type": "shell",
      "command": "poetry install --sync"
    },
    {
      "label": "build",
      "type": "shell",
      "command": "poetry build",
      "dependsOn": ["install"]
    }
  ]
}
```

My computer:

```powershell
$ vtr build
[1/2] Executing task "install": C:\Program Files\WindowsApps\Microsoft.PowerShell_7.3.5.0_x64__8wekyb3d8bbwe\pwsh.exe -Command poetry install --sync
Installing dependencies from lock file

No dependencies to install or update

Installing the current project: pyleft (1.2.2)
[2/2] Executing task "build": C:\Program Files\WindowsApps\Microsoft.PowerShell_7.3.5.0_x64__8wekyb3d8bbwe\pwsh.exe -Command poetry build
Building pyleft (1.2.2)
  - Building sdist
  - Built pyleft-1.2.2.tar.gz
  - Building wheel
  - Built pyleft-1.2.2-py3-none-any.whl
```

GitHub Actions Workflow File

```yaml
name: Publish

on:
  workflow_dispatch:
  push:
    branches:
      - main

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: write

    if: "${{ !contains(github.event.head_commit.message, 'ci skip') }}"

    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Install poetry/vscode-task-runner
        run: |
          pipx install poetry
          pipx install vscode-task-runner

      - name: Build
        run: vtr build

      - name: Publish package distributions to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
```

GitHub Actions Log

```text
Run vtr build
  vtr build
  shell: /usr/bin/bash -e {0}
  env:
    PROJECT_VERSION: 1.2.2

[1/2] Executing task "install": /usr/bin/bash -c poetry install --sync
Installing dependencies from lock file

Package operations: 18 installs, 1 update, 0 removals

  • Installing distlib (0.3.6)
  • Installing exceptiongroup (1.1.1)
  • Installing filelock (3.12.0)
  • Installing iniconfig (2.0.0)
  • Installing packaging (23.1)
  • Installing platformdirs (3.5.0)
  • Installing pluggy (1.0.0)
  • Updating setuptools (67.8.0 -> 67.7.2)
  • Installing tomli (2.0.1)
  • Installing cfgv (3.3.1)
  • Installing coverage (7.2.5)
  • Installing identify (2.5.23)
  • Installing nodeenv (1.7.0)
  • Installing pytest (7.4.0)
  • Installing pyyaml (6.0)
  • Installing virtualenv (20.23.0)
  • Installing pathspec (0.11.1)
  • Installing pre-commit (2.21.0)
  • Installing pytest-cov (4.1.0)

Installing the current project: pyleft (1.2.2)
[2/2] Executing task "build": /usr/bin/bash -c poetry build
Building pyleft (1.2.2)
```

## Conclusion

Hopefully this gives you some ideas on how to get your local dev environment
to more closely resemble your production environment. An exact duplicate is
not always possible, but I find the closer you can make it, the less headache
you will have later. As always, exact implementation details depend on
the languages, application type, industry, etc.

Particularly with Python, certain things like testing multiple versions of Python
or multiple operating systems are not things I've personally found benefit
setting up locally. These I tend to find much easier to configure in CI/CD,
which can take advantage of parallel runners. If it was something that
caused a lot of heartache, then setting something up locally could be done.
