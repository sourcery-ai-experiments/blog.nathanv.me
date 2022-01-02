---
author: Nathan Vaughn
date: "2021-10-10"
description: Explaining the structure of Docker image names and the hidden defaults
tags:
  - Docker
  - Docker Hub
title: Docker Image Names for Dummies
---

# Introduction

One thing I've noticed in people starting to learn about Docker,
is that there is a lot of confusion about image names. What's the difference
between `python`, `python:latest`, and `docker.io/python:latest`?
I'm going to try and break it down.

# Image Names

The name of a Docker image is made of a number of pieces. The confusing part is
that nearly every piece is optional and can mixed and matched, along
with non-obvious defaults. I'm going to work left to right in the image name, with
the example of the [base `python` image](https://hub.docker.com/_/python).

## Registry

The first piece of any Docker image name is the registry. The registry is just the
server the image comes from (or at least tagged to). A whole discussion on Docker
registries is [here]({{< relref "quay-registry#what-is-a-registry" >}}).

By default, the registry `docker.io` is used, so the following two images are the same:

1. `docker.io/python`
2. `python`

Fun fact, for extra confusion, the registry `docker.io` is also available under
many different names including:

- `docker.io`
- `index.docker.io`
- `registry-1.docker.io`

Another point about the registry, is this it is just a web server so if you are running
your own, IP addresses and port numbers can also be used:

- `localhost:5000/python`
- `192.168.111.20/python`

## User

After the registry, followed by a `/`, comes the user.
The user is the person or organization that
owns the image. Like the registry, this is optional, and defaults to `library`,
so the following two images are the same:

1. `docker.io/library/python`
2. `docker.io/python`

This is also why in the web UI for Docker Hub, library images have a different URL than
non-library images:

- `https://hub.docker.com/_/python`
- `https://hub.docker.com/r/bitnami/python`

**_HOWEVER_**, this is not always the case, and actually varies by
server implementation. The default Docker Hub registry does this, but not
all registries do. For example, the
[Quay registry software](https://www.projectquay.io/) allows you to enable this
feature, but on the other hand as far as I'm aware,
[Azure Container registry](https://azure.microsoft.com/en-us/services/container-registry/)
does not do this and will let you name images with or without user names
and does not do any `/library/` shenanigans.

## Repository

After the user, followed again by a `/`, is now the image repository.
This is more or less the name of the image itself.
In our example, the repository is `python`. This is
the only piece of the image name that is actually required.

## Tag

Finally, is the tag of the image, which follows the repository name with a `:`.
This is basically the version specifier of the image.
The tag is optional, and defaults to `latest`. The `latest` tag has no
special properties, nor does it even have to be defined,
it's just by convention the most recent version of the image.
Once again in our example, the following two images are the same:

1. `docker.io/library/python:latest`
2. `docker.io/library/python`

Tags are user-defined and can be almost anything. In our
`python` example image, this includes things like `latest`, `3.10`, `3.10-buster`, etc.

A confusing part about tags is that unlike most package registries (npm, PyPi, etc.),
tags can be overwritten or deleted at any time. This how `latest` tags are usually used,
by always assigning it to the last image pushed. Additionally, an image can have
multiple tags. Once again in our example, the following two images are the same
(at time of writing):

1. `docker.io/library/python:latest`
2. `docker.io/library/python:3.10.0`

To help users select specific versions of images, large projects often tag things
in multiple ways, depending on how specific you want to be. For example:

- `python:latest`: The latest version of Python
- `python:3`: The latest version of Python 3
- `python:3.10`: The latest version of Python 3.10
- `python:3.10.0`: Python 3.10.0 exactly. Maybe receive security fixes to the image

## Digests

Okay, there is actually one last piece of the image name, which is the digest.
These are mutually exclusive to tags are not commonly used.
Instead of separating the repository and tag with a `:`, you separate a repository and
digest with a `@`. These reference a specific version of the image
based on a hash of the content of the image. Unlike user-defined tags,
these can not be changed. These take the form of (nearly always) `sha256:<hash>`.
Once again, these two images are the same (at time of writing):

1. `docker.io/library/python@sha256:dc7c3f207ec689940a1458d09c862f599c1cf5ca525ee28e18514df3735feea1`
2. `docker.io/library/python:latest`

# Conclusion

Today we've learned about Docker image names are constructed, and how all of the following
(at time of writing) are the exact same image:

- `python`
- `docker.io/python`
- `index.docker.io/python`
- `docker.io/library/python`
- `index.docker.io/library/python`
- `python:latest`
- `docker.io/python:latest`
- `index.docker.io/python:latest`
- `docker.io/library/python:latest`
- `index.docker.io/library/python:latest`
- `python:3.10.0`
- `docker.io/python:3.10.0`
- `index.docker.io/python:3.10.0`
- `docker.io/library/python:3.10.0`
- `index.docker.io/library/python:3.10.0`
- `python@sha256:dc7c3f207ec689940a1458d09c862f599c1cf5ca525ee28e18514df3735feea1`
- `docker.io/python@sha256:dc7c3f207ec689940a1458d09c862f599c1cf5ca525ee28e18514df3735feea1`
- `index.docker.io/python@sha256:dc7c3f207ec689940a1458d09c862f599c1cf5ca525ee28e18514df3735feea1`
- `docker.io/library/python@sha256:dc7c3f207ec689940a1458d09c862f599c1cf5ca525ee28e18514df3735feea1`
- `index.docker.io/library/python@sha256:dc7c3f207ec689940a1458d09c862f599c1cf5ca525ee28e18514df3735feea1`

Personally, I like to be explicit and specific as reasonably possible. In my Dockerfiles,
I would usually do something like:

```dockerfile
FROM docker.io/library/python:3.10.0
```
