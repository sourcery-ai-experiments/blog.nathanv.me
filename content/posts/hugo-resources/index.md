---
author: Nathan Vaughn
date: "2023-04-15"
description: Using resources in Hugo to automatically process static site assets.
tags:
  - Hugo
title: "Hugo Resources"
---

## Introduction

This is a quick overview of how to use Hugo's
[resources feature](https://gohugo.io/hugo-pipes/introduction/)
to automatically process site assets.

## Getting Resources

First off, you need to instruct Hugo to load the resource. This has a number of
different syntaxes depending on the situation, and the documentation can be quite
confusing. If a resource cannot be found, the function will return `nil`, which
can tell you that you're doing something wrong.

### Sitewide

If you have a resource that you want to use for the entire site, such as a CSS file,
JavaScript, or cover image, place this in the `assets` directory of your site project.
Use the `resources.get` function to get one of these resources, by passing it
a relative path to the resource inside the `assets` directory.

```go-html-template
{{ $js := resources.Get "js/main.js" }}
```

### Page Specific

If you have a resource that is specific to a page, place it in a
[page bundle](https://gohugo.io/content-management/page-bundles/), and then
get it with the `.Page.Resources.get` function.

```go-html-template
{{ $image := .Page.Resources.Get "myimage.jpg" }}
```

In some weird circumstances, I've found that getting the resource from the parent
page may be required:

```go-html-template
{{ $image := .Page.Parent.Resources.Get "myimage.jpg" }}
```

### Remote

Lastly, if you want to live life on the edge a little bit more, you can also reference
a resource from a remote URL, with the `resources.getRemote` function.

```go-html-template
{{ $jquery := resources.GetRemote "https://code.jquery.com/jquery-3.6.0.min.js" }}
```

I generally don't recommend this, since you won't be able to build your site
if the remote source is offline, but obviously it depends on your use case.

This does automatically cache the resource depending on the response headers,
so don't feel bad if you're constantly running `hugo`. You're not repeatedly
downloading the same file over and over.

## Fingerprinting

One very useful feature of resources is the ability to add a fingerprint to them.
What this means is that Hugo can automatically add a hash to a filename.

```go-html-template
{{ $css := resources.Get "css/style.css" | resources.Fingerprint }}
<link rel="stylesheet" href="{{ $css.RelPermalink }}" />
<!-- This will produce something like /css/styles.fa61de5858ec4fba3617c9d81d66046547755a44aa5efda6e7727872b3ee6daa.css -->
```

The advantage of this is cache busting. If you screw up your cache policies,
and replace the contents of a file on your website, the user's browser may continue
to use the old cached copy. The user's browser fetches the HTML for the page,
sees a file with the same name, and depending on how long the cache expiration
was set for, may just use its local copy. By adding a hash to the filename, whenever
the contents of the file change, the file gets a new name, and the browser will
be forced to download a new copy.

This can also be used for
[subresource integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity#how_browsers_handle_subresource_integrity),
particularly with JavaScript assets, with the `.Data.Integrity` property.

```go-html-template
<script type="text/javascript" src="{{ $bundle.RelPermalink }}" integrity="{{ $bundle.Data.Integrity }}"></script>
```

If you do this, make sure this is the last function in your sequence.

### Examples

Here are a few examples I've put together that are modified from templates I've made
for my own websites recently.

## CSS

Here is an example of how you can use Hugo resources to minify CSS and create a
source map. One thing to note, is that generating source maps is most easily done
(without needing to install external tools and things), with the
[`resources.ToCSS`](https://gohugo.io/hugo-pipes/transform-to-css/)
function. If your source CSS code is not Sass or SCSS, just change the file extension.

```go-html-template
{{ $css := resources.Get "css/style.scss" }}
{{ $css := $css | resources.ToCSS (dict "targetPath" "css/styles.css" "enableSourceMap" true) | resources.Minify | resources.Fingerprint }}
<link rel="stylesheet" href="{{ $css.RelPermalink }}" />
```

## JS

This example shows how you can combine multiple JavaScript files into one, and
then minify them and create a source map. The function
[`js.build`](https://gohugo.io/hugo-pipes/js/) does use
[ESBuild](https://github.com/evanw/esbuild) and I have found that this can break
certain libraries, that make a global variable available like `$` for jQuery.
If this is the case, you may want to use
[`resources.Babel`](https://gohugo.io/hugo-pipes/babel/) instead, though this requires
Babel to be installed.

```go-html-template
{{ $menu := resources.Get "js/menu.js" }}
{{ $prism := resources.Get "js/prism.js" }}
{{ $theme := resources.Get "js/theme.js" }}
{{ $bundle := slice $menu $prism $theme | resources.Concat "js/bundle.js" | js.Build (dict "sourceMap" "external" ) | resources.Minify | resources.Fingerprint }}
<script type="text/javascript" src="{{ $bundle.RelPermalink }}" integrity="{{ $bundle.Data.Integrity }}"></script>
```

## Images

Images are where Hugo's asset processing capabilities really shine. Images are often
the largest files on a static site, so resizing and compressing them appropriately
can significantly decrease the loading time of a page. In the past, this has been ...
_challenging_. I always found manually resizing images hard because I had to manually
try to keep the dimensions consistent and then I would often forget to keep a copy
of the original uncompressed image. Additionally, .webp is frequently recommended now,
but some browsers still do not support it, and many desktop image editors don't either.
This usually lead me to giving up trying to do this, and just serve the original image
instead.

Hugo lets you resize images automatically, and convert them to different formats
automatically at build time. This is _amazing_. You can keep the original source image
in the site repository and only serve smaller resized versions to users. By being
able to also convert the images to different formats, you can easily serve
optimized versions to browsers that support it.

See [this page](https://gohugo.io/content-management/image-processing/)
for all the options, but I generally use the `.Fit` function, since it resizes
the image to fit inside a given box while maintaining the aspect ratio.

Here is an example template I made to overwrite
`layouts/_default/_markup/render-image.html` to automatically resize and convert
images in a Markdown image tag, utilizing the `alt` text as a caption:

```go-html-template
{{ $image := .Page.Resources.Get .Destination }}
{{ $image_webp := false }}
{{ $image_fit := false }}

{{ if not $image }}
    {{ errorf "Image %q not found on page %q" .Destination .Page }}
{{ end }}

{{/* Can only resize raster images */}}
{{ if ne $image.MediaType.SubType "svg" }}
  {{ $image_fit = $image.Fit "1000x1000" | resources.Fingerprint }}
  {{ $image_webp = $image.Fit "1000x1000 webp" | resources.Fingerprint }}
{{ end }}

{{ $image = $image | resources.Fingerprint }}

<figure>
    <picture>
        {{ with $image_webp }}
        <source loading="lazy" srcset="{{ $image_webp.Permalink }}" type="image/webp" alt="{{ .Text }}">
        {{ end }}

        {{ if $image_fit }}
        <img loading="lazy" src="{{ $image_fit.Permalink }}" alt="{{ .Text }}">
        {{ else}}
        <img loading="lazy" src="{{ $image.Permalink }}" alt="{{ .Text }}">
        {{ end }}
    </picture>

    {{ with .Text}}
    <figcaption class="center">{{ . | markdownify }}</figcaption>
    {{ end }}
</figure>
```

The weird `{{ if ne $image.MediaType.SubType "svg" }}` statements are because
vector images cannot be resized or converted.

Do note that Hugo still copies the original image into your final output,
even if you resize or convert it. In some deployment environments like GitHub Pages,
this may quickly balloon your website size past limits. In that case,
you may want to think about not worrying about it, or writing a script
to purge unused images.

## Using Resources in Third Party Themes

While I've become a big fan of resources, a lot of Hugo themes don't support them
or properly implement them yet. One of my personal pet peeves are themes that
use JS/CSS from multiple different CDNs. I personally prefer to host all of my site
assets myself, so I like to rewrite these templates. However, these changes to the
templates are often small, yet the entire template can be quite large, and I don't
want to overwrite the entire thing. To get around this, I install the theme as an npm
package and then use the [patch-package](https://www.npmjs.com/package/patch-package)
package.

package.json

```json
{
  "dependencies": {
    "hello-friend": "github:panr/hugo-theme-hello-friend#3.0.0",
    "hugo-extended": "^0.111.3",
    "patch-package": "^6.5.1"
  },
  "scripts": {
    "postinstall": "patch-package"
  }
}
```

config/hugo.toml

```toml
themesDir = "node_modules"
theme     = "hello-friend"
```

Now, I can edit the theme directly in the `node_modules/hello-friend` directory,
and then run `npx patch-package hello-friend`. This will create a patch file in
the `patches/` directory, and will automatically apply it after any `npm install`.

Along with not needing to copy/paste large templates and overwrite a single line,
GitHub dependabot can now also automatically create pull requests for new theme
versions at the same time as any other npm packages.

Here is an example that I made for this blog at time of writing:

```diff
diff --git a/node_modules/hello-friend/layouts/partials/footer.html b/node_modules/hello-friend/layouts/partials/footer.html
index 7b7f8c6..e7ffed2 100644
--- a/node_modules/hello-friend/layouts/partials/footer.html
+++ b/node_modules/hello-friend/layouts/partials/footer.html
@@ -18,10 +18,10 @@
   </div>
 </footer>

-{{ $menu := resources.Get "js/menu.js" | js.Build }}
-{{ $prism := resources.Get "js/prism.js" | js.Build }}
-{{ $theme := resources.Get "js/theme.js" | js.Build }}
-{{ $bundle := slice $menu $prism $theme | resources.Concat "bundle.js" | resources.Minify }}
-<script type="text/javascript" src="{{ $bundle.RelPermalink }}"></script>
+{{ $menu := resources.Get "js/menu.js" }}
+{{ $prism := resources.Get "js/prism.js" }}
+{{ $theme := resources.Get "js/theme.js" }}
+{{ $bundle := slice $menu $prism $theme | resources.Concat "js/bundle.js" | js.Build (dict "sourceMap" "external" ) | resources.Minify | resources.Fingerprint }}
+<script type="text/javascript" src="{{ $bundle.RelPermalink }}" integrity="{{ $bundle.Data.Integrity }}"></script>

 {{- partial "extended_footer.html" . }}
diff --git a/node_modules/hello-friend/layouts/partials/head.html b/node_modules/hello-friend/layouts/partials/head.html
index 07938e1..6013e64 100644
--- a/node_modules/hello-friend/layouts/partials/head.html
+++ b/node_modules/hello-friend/layouts/partials/head.html
@@ -16,14 +16,16 @@

 <!-- Theme CSS -->
 {{ $res := resources.Get "css/style.scss" }}
-{{ $style := $res | resources.ToCSS }}
+{{ $style := $res | resources.ToCSS (dict "targetPath" "css/styles.css" "enableSourceMap" true) | resources.Minify | resources.Fingerprint }}
 <link rel="stylesheet" href="{{ $style.RelPermalink }}" />
 <!-- Custom CSS to override theme properties (/static/style.css) -->
-<link rel="stylesheet" href="{{ "style.css" | absURL }}" />
+{{ $custom_res := resources.Get "style.scss" }}
+{{ $custom_style := $custom_res | resources.ToCSS (dict "targetPath" "css/custom_styles.css" "enableSourceMap" true) | resources.Minify | resources.Fingerprint }}
+<link rel="stylesheet" href="{{ $custom_style.RelPermalink }}"/>

 <!-- Icons -->
-<link rel="apple-touch-icon-precomposed" sizes="144x144" href="{{ "img/apple-touch-icon-144-precomposed.png" | absURL }}" />
-<link rel="shortcut icon" href="{{ "img/favicon.png" | absURL }}" />
+<link rel="shortcut icon" href=https://nathanv.me/img/theme-colors/green.png>
+<link rel=apple-touch-icon href=https://nathanv.me/img/theme-colors/green.png>

 <!-- Fonts -->
 <link href="{{ (resources.Get "fonts/Inter-Italic.woff2").RelPermalink }}" rel="preload" type="font/woff2" as="font" crossorigin="">

```
