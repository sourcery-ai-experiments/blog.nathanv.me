---
author: Nathan Vaughn
date: "2023-04-15"
description: Properly configuring your Hugo site's base URL when using Cloudflare Pages.
tags:
  - Hugo
  - Cloudflare
title: "Hugo Base URL with Cloudflare Pages"
---

## Introduction

I've been using [Cloudflare Pages](https://pages.cloudflare.com/) for a while now,
after migrating from GitHub pages. The limits are more generous, the preview
deployments are super handy, and I was already using Cloudflare.

After recently redoing my [homepage](https://nathanv.me), I realized that a lot of
links and images would be wrong when making a pull request.
They were pointing to the live site rather than the preview deployment for that pull
request.

## Problem

The problem lies with the Hugo
[`baseURL`](https://gohugo.io/getting-started/configuration/#baseurl) setting.
When absolute URLs are created in templates, the path is appended to the end
of the base URL. As Cloudflare Pages uses a new domain name for every deployment,
this is not a static value.

## Solution

While I would love to just set the base URL to be "/" and be done,
some places like the contents of the sitemap or
[canonical URL](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
MUST be an absolute URL (`https://example.com/page` rather than `/page`).

My first recommendation is to convert as many links as possible to relative URLs
rather than absolute URLs. This solves most of the problems. If you're using
a third party theme, you may be able to create some patches to help. I like
[this](https://www.npmjs.com/package/patch-package) package a lot. More about that
[here]({{< relref "hugo-resources/#using-resources-in-third-party-themes" >}}).

- [`absURL`](https://gohugo.io/functions/absurl/) -> [`relURL`](https://gohugo.io/functions/relurl/)
- [`absLangURL`](https://gohugo.io/functions/abslangurl/) -> [`relLangURL`](https://gohugo.io/functions/rellangurl/)
- `.Permalink` -> `.RelPermalink`

What I also ended up doing was to leave the `baseURL` setting to "/",
so when developing locally everything worked. I then made a quick script that
checked if the build was running on a deployment build, or the main branch.
If running on a deployment build, it would use the value from the `CF_PAGES_URL`
environment variable, which gives the full URL of the deployment. If the build
is running on the main branch, I hardcoded the URL, since the `CF_PAGES_URL`
environment variable always gives the `<commit>.<project>.pages.dev` domain, even if
you have a custom domain setup.

This culminates to this:

package.json

```json
{
  "dependencies": {
    "cross-spawn": "^7.0.3",
    "hugo-extended": "^0.111.3"
  },
  "scripts": {
    "build": "node build.js",
    "postinstall": "patch-package"
  }
}
```

build.js

```javascript
const spawn = require("cross-spawn");
const fs = require("fs");
var base_url = "/";

if (process.env.CF_PAGES_BRANCH === "main") {
  base_url = "https://blog.nathanv.me/";
} else if (process.env.CF_PAGES_URL) {
  base_url = process.env.CF_PAGES_URL;
}

console.log(`Using base url "${base_url}"`);
cmd = spawn.sync(
  "hugo",
  ["--cleanDestinationDir", "--minify", "-b", base_url],
  { encoding: "utf8" }
);

if (cmd.error) {
  console.log("ERROR: ", cmd.error);
}

console.log(cmd.stdout);
console.error(cmd.stderr);

process.exit(cmd.status);
```

While not pretty, it works mostly. If you have more than one custom domain
(like a `www` version), that one will just exclusively point to the custom domain
you choose as "most" canonical.

| Environment                                 | Works |
| ------------------------------------------- | ----- |
| Latest Main (custom domain)                 | Yes   |
| Alternative Latest Main (www.custom domain) | Kinda |
| Older Main (\<commit>.\<project>.pages.dev) | No    |
| Preview (\<commit>.\<project>.pages.dev)    | Yes   |
| Locally                                     | Yes   |
