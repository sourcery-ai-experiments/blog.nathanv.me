---
author: Nathan Vaughn
date: "2021-09-02"
description: How to effectively cache Python packages from Azure Artifacts in CI/CD
tags:
  - Python
  - Azure Artifacts
  - Azure Pipelines
  - GitHub Actions
title: Azure Artifacts Python Package Caching
---

## Introduction

Where I work, we use
[Azure Artifacts](https://azure.microsoft.com/en-us/services/devops/artifacts/)
extensively to store our Python packages. It works great.
It allows us to easily maintain copies of public packages we depend on
(which helps prevent any "left-pad" scenarios, and keeps our cybersecurity team happy),
and publish and distribute our own internal packages. However, it's kind of slow.
This is probably due to the proxying it does to public package indexes, along with
all of the authentication and authorization it does. Sometimes, our CI/CD jobs
with a lot of dependencies would take 2-3 minutes alone just to install the Python
packages. In an attempt to speed things up, we enabled caching
to not need to constantly re-download packages. However, this didn't
really seem to work. `pip install` would still constantly re-redownload packages
it should have had cached.

## Problem

To understand why caching with Azure Artifacts doesn't work, we first need to understand
how `pip` caches packages. When you run `python -m pip install <package>`, `pip`
doesn't cache the **file(s)** that it downloads, rather, it caches the **HTTP response**
of the URL it was given to download the package at. So for example, if you do
`python -m pip install requests`, `pip` asks `https://pypi.org/simple` for the latest
version of the package `requests`. `https://pypi.org` then responds with a URL something
like `https://files.pythonhosted.org/packages/really/big/hash`. `pip` then caches
that URL and the response it gets from it.

So, why does Azure Artifacts break this? Well Azure Artifacts stores its files
in Azure Blob Storage, understandably. As these files are not public, whenever
Azure Artifacts returns the URL for a package file to download, it includes a temporary
access token that allows `pip` to download the file for a short period of time.
For example, `pip` would get a URL roughly like
`https://azureartifacts.blob.core.windows.net/path/package?acccess_token=sometoken`.
This is the crux of the problem. More or less, every time `pip` tries to get a package
from Azure Artifacts, it's given a different URL every single time,
as the token changes, which renders the local cache useless.

## Solution

The solution to this is to have `pip` first download the packages it needs,
and then install them _only_ from that directory, effectively caching the package
files rather than the package URLs.

```bash
set -e

mkdir -p $PIP_CACHE_DIR

python -m pip install pip wheel --upgrade
python -m pip wheel --find-links=$PIP_CACHE_DIR --wheel-dir=$PIP_CACHE_DIR <packages>
python -m pip install --find-links=$PIP_CACHE_DIR --no-index <packages>
```

The `pip wheel` command downloads the given packages and creates `.whl` files for them
in the directory given by `--wheel-dir`.
Most packages these days are distributed as wheels, but for any packages that
only provide distributions, this will generate a wheel file locally.

Additionally, the `--find-links` option tells `pip` to also look for packages
in the given directory. In our case, we want that to be the directory we're saving
wheels to. This helps prevent downloading packages we already have.

Then, the `pip install` command installs packages from the directory the
wheels were saved to, and the `--no-index` parameter tells `pip` not to use
an index to find packages (as it should already have everything it needs locally).

Lastly, the environment variable `PIP_CACHE_DIR` is what `pip` already uses
to determine where to cache stuff, so by using this, we can also leverage
whatever cache of `pip`'s that actually works.

With this script however, you do need to be a bit careful. If you do not
provide exact versions of packages you want, you may get local packages that
are older than the latest versions available
(though you should be pinning your version numbers anyways).

An example implementation for Azure Pipelines:

```yml
- task: Cache@2
  inputs:
    key: 'python | "$(Agent.OS)" | **/requirements**.txt'
    restoreKeys: |
      python | "$(Agent.OS)"
      python
    path: $(Agent.TempDirectory)/.pip
  displayName: Cache pip packages

- task: Bash@3
  inputs:
    targetType: inline
    script: |
      <insert script here>
  env:
    PIP_CACHE_DIR: $(Agent.TempDirectory)/.pip
  displayName: Install pip packages
```

With Azure Pipelines as well, you can easily set up a reusable template for this
that you can use across your organization.

An example implementation for GitHub Actions:

```yml
- name: Cache pip packages
  uses: actions/cache@v2
  with:
    path: ${{ runner.temp }}/.pip
    key: python-${{ runner.os }}-${{ hashFiles('**/requirements**.txt') }}
    restore-keys: |
      python-${{ runner.os }}
      python

- name: Install pip packages
  shell: bash
  run: |
    <insert script here>
  env:
    PIP_CACHE_DIR: ${{ runner.temp }}/.pip
```

At the time of writing, GitHub Actions doesn't really support templates
like Azure Pipelines does.
