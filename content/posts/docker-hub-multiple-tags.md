---
author: Nathan Vaughn
date: "2019-11-23"
description: Writing a custom build hook for Docker Hub to apply multiple tags to
  a Docker image
tags:
- Docker
- Docker Hub
- bash
title: Docker Hub Build Hook to Apply Multiple Image Tags
---

## Background

While working on my
[Docker image for webtrees](https://github.com/NathanVaughn/webtrees-docker),
I ran into a peculiar issue. I had setup automated builds in Docker Hub for every
tagged commit in my git repository.
At first, I wanted to be able to have multiple tags for
each image build, so that each build could be version tagged (like `1.7.15`) and
have the `latest` tag applied as well.
Using an [undocumented feature](https://github.com/docker/hub-feedback/issues/341#issuecomment-551808767),
I was able to get that to work. However, problems arose once I wanted to also properly
[label my image](https://medium.com/@chamilad/lets-make-your-docker-image-better-than-90-of-existing-ones-8b1e5de950d).
Specifically, I was trying to add the `BUILD_DATE` and `VCS_REF` labels. 
With Docker Hub, this requires
you to add your own [build hook](https://docs.docker.com/docker-hub/builds/advanced/)
in order to pass in the needed build arguments.
Using [an example I found](https://medium.com/microscaling-systems/labelling-automated-builds-on-docker-hub-f3d073fb8e1),
I added my own build hook to my repository.

```bash
#!/bin/bash

docker build --build-arg VCS_REF=`git rev-parse — short HEAD` \
  --build-arg BUILD_DATE=`date -u +”%Y-%m-%dT%H:%M:%SZ”` \
  -t $IMAGE_NAME .
```

This is where everything fell apart. My image builds started failing!

{{< figure src="/img/docker-hub-multiple-tags/build_fail.jpg" alt="Docker Hub build failure" position="center" style="border-radius: 8px;" caption="Oh no" captionPosition="center" >}}

## Issue

After some head scratching and debugging, I discovered the two-part problem.

### Environment Variable

The first part of the problem was the `IMAGE_NAME`
[environment variable](https://docs.docker.com/docker-hub/builds/advanced/#environment-variables-for-building-and-testing).
Normally, this environment variable provides a value like 
`index.docker.io/username/repo:tag`. However, when you abuse
Docker Hub's tagging system to do multiple tags like I was doing, 
you instead get a value like `index.docker.io/username/repo:tag1,tag2`.

### Build Hook

With the aforementioned malformed environment variable, the simple build hook
script example I found completely falls flat, as this is not valid syntax.

Mysteriously, if you don't use
a custom build script, this *does* in fact work, so Docker must be able to handle
this in their own scripts, with logic they don't share.

## Workaround

To fix this, you need to write your own build hook script that can handle multiple
tags being passed to it. You can either tag the image during the `build` 
command (easier) or build the the image first, then `docker tag` it multiple times 
(a bit more difficult, since you have to reference the image properly). 
I was unable to find anyone else who has done this, so I wrote my own.
This is what I have come up with and seems to work:

```bash
#!/bin/bash

IFS=',' read -ra tags <<< "$DOCKER_TAG"
TAG_COMMAND=""

for tag in "${tags[@]}"
do
    TAG_COMMAND="$TAG_COMMAND -t $DOCKER_REPO:$tag"
done

docker build --build-arg BUILD_DATE=`date -u +"%Y-%m-%dT%H:%M:%SZ"` \
             --build-arg VCS_REF=`git rev-parse --short HEAD` \
             $TAG_COMMAND .
```

This script takes in the `DOCKER_TAG` environment variable 
(which provides a comma-separated list of tags), splits it by comma, then builds
the `-t` tagging argument for the `build` command. There is no harm in
using this for an image with only a single tag, as this will still work perfectly
fine.

{{< figure src="/img/docker-hub-multiple-tags/build_success.jpg" alt="Docker Hub build success" position="center" style="border-radius: 8px;" caption="Success!" captionPosition="center" >}}

## Conclusion

With a bit of abuse of some undocumented features, I was able to get my Docker image
to build automatically on Docker Hub with all of the
[labels and tags](https://microbadger.com/images/nathanvaughn/webtrees) I wanted.

{{< figure src="/img/docker-hub-multiple-tags/microbadger_labels.jpg" alt="Microbadger labels" position="center" style="border-radius: 8px;" caption="Microbadger labels" captionPosition="center" >}}

This adventure though has really made me question my usage of Docker Hub's
image building. It seems like I could have avoided a lot of this hassle if I
had set up builds with a different CI provider like GitHub Actions, and then just
push to Docker Hub, instead of dealing with all of these weird, undocumented
limitations. I also don't know if or when this workaround will stop functioning.

## References
- [https://docs.docker.com/docker-hub/builds/advanced/](https://docs.docker.com/docker-hub/builds/advanced/)
- [https://medium.com/microscaling-systems/labelling-automated-builds-on-docker-hub-f3d073fb8e1](https://medium.com/microscaling-systems/labelling-automated-builds-on-docker-hub-f3d073fb8e1)
- [https://github.com/docker/hub-feedback/issues/341#issuecomment-551811075](https://github.com/docker/hub-feedback/issues/341#issuecomment-551811075)
- [https://microbadger.com/images/nathanvaughn/webtrees](https://microbadger.com/images/nathanvaughn/webtrees)