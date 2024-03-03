---
author: Nathan Vaughn
date: "2024-03-03"
description:
  Four hours of my life wasted to implied port numbers
tags:
  - Octoprint
  - Cura
  - Authentik
  - 3D Printing
title: Making Authentik work with OctoPrint and Cura
---

## Introduction

When using the Cura OctoPrint plugin
([GitHub](https://github.com/fieldOfView/Cura-OctoPrintPlugin)/[Ultimaker](https://marketplace.ultimaker.com/app/cura/plugins/fieldofview/OctoPrintPlugin))
I found that my [Authentik](https://goauthentik.io/) proxy in front of OctoPrint
was returning 404 errors, despite allowing `\/api\/.*`.

## Solution

After four hours of debugging, I found the reason was that the way the
Qt network library that Cura uses works, it made Authentik think the requests were
coming from a different hostname by including the port number and
therefore not match any known proxy providers.

When using the OctoPrint web UI and using other tools like `curl`, the hostname
would register as `octoprint.nathanv.app`, however Qt would make it appear as
`octoprint.nathanv.app:443`. The fix was to setup a duplicate proxy provider
and application in Authentik with the port number as part of the hostname.

{{< figure src="img/2024-03-03-16-44-31.png" caption="Duplicate proxy provider in Authentik." captionPosition="center" >}}

Now the OctoPrint web UI and Cura all work correctly with extra authentication.

It seems most tools and web browsers automatically strip the ports 80 or 443 from the
hostname when using `http://` or `https://`, respectively, but I guess Qt
just has to be different.
