+++
title = "Deploying a Static Site with GitHub Actions"
date = "2019-10-15"
author = "Nathan Vaughn"
tags = ["GitHub", "GitHub Actions", "continuous delivery", "Hugo"]
description = "How I used GitHub Actions to completely automate the building and deployment of my personal site (and this blog)"
+++

## Background

A little while back, GitHub released their
[Actions](https://github.com/features/actions)
integrated CI/CD (continuous integration and delivery) platform.
I signed up for the beta and managed to get in. This article will cover
how I used GitHub Actions to completely automate the building and deployment
of my personal site (and this blog).

## Actions Introduction

GitHub Actions is a continuous
[integration](https://en.wikipedia.org/wiki/Continuous_integration) and
[delivery](https://en.wikipedia.org/wiki/Continuous_delivery) product. It's
similar to [Travis CI](https://travis-ci.org/) or
[Circle CI](https://circleci.com/) or other similar existing providers.
In simple terms, it means that on every commit, pull request,
or whatever else you setup, scripts run. These can be to run tests to make sure
your commit doesn't break anything (integration), or to automatically format code,
or to deploy your software (delivery), or anything else you want.

In the case of GitHub Actions,
[these scripts](https://help.github.com/en/articles/configuring-a-workflow)
are defined in `.yml` files placed
in the folder `.github/workflows/` in the root of your repository
([example](https://github.com/NathanVaughn/nathanv.me/blob/master/.github/workflows/main.yml)).
The workflows you setup can be run on repository events (push, pull request, etc.),
webhook events (forking, wiki update, etc.), scheduled events (a cron schedule),
or external events (external webhook). These workflows run on
[premade Docker containers](https://help.github.com/en/articles/software-in-virtual-environments-for-github-actions)
for a variety of operating systems, which include a lot of useful
software already installed (like Python 3, webpack, MySQL, etc.).

However, if you need more functionality than what is available in the workflows,
or want to make something reusable, you can create your own
[Docker container](https://help.github.com/en/articles/creating-a-docker-container-action)
or [JavaScript](https://help.github.com/en/articles/creating-a-javascript-action)
action. These are automatically executed within the existing Docker container your
action runs in, seamlessly.

Arguably, the best part of Actions, is the
[Marketplace](https://github.com/marketplace?type=actions). With the GitHub marketplace,
people can make their custom actions available for others to use, and you can import
them into your workflows easily. GitHub also publishes some of
[their own actions](https://github.com/actions)
with some basic, yet widely used functionality.

## My Website Setup

My website is built with the
[Hugo](https://gohugo.io) static site generator, using a theme I made for myself.
I admit, my website doesn't exactly have the cleanest structure. While Hugo is meant
to be used with Markdown files (like this blog), I wanted *extremely* structured
content for my website. In order to do this, I used Hugo's
[data templates](https://gohugo.io/templates/data-templates/)
([example](https://github.com/NathanVaughn/nathanv.me/blob/master/data/workexperience.yml)).

Because the theme and actual content are extremely coupled together,
I decided not to release the theme separately, and just tie it into my
main Hugo site repo. This means that I'm not using git submodules,
and my npm scripts for the HTML/CSS are in the same `package.json` file as
my scripts for Hugo.

Anyways, this was my build process for my site previously:

1. Make content/theme update
2. Run `npm run svgmin` to minify SVG files (if needed)
3. Run `npm run critical` to generate new [critical CSS](https://www.sitelocity.com/critical-path-css-generator) (if needed)
4. Run `npm run build:css` to polyfill and minify the CSS (if needed)
5. Run `npm run build:js` to minify the JS (if needed)
6. Run `hugo` to actually build the site's contents
7. Run `npm run beautify` to beautify the output HTML because whitespace with HTML
templates is surprisingly difficult
8. Run `npm run deploy` to actually commit and push the changes

While I did basically have steps 4-7 clumped together into a single `build` script,
it was clunky and I'd always inevitably forget to run something. No more!

## My Website Actions Workflow

With the help of GitHub Actions, I was able to automate every single step of this
process, plus steps I hadn't even automated previously.

My workflow file (at time of writing):

```yml
name: Build

on:
  push:
    branches:
    - master

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@master
      with:
        submodules: true
    - name: Install Node
      uses: actions/setup-node@master
    - name: Install dependencies
      run: npm install
    - name: Build Critical CSS
      run: npm run critical
    - name: Build Site
      run: npm run build
    - name: Deploy Site
      uses: peaceiris/actions-gh-pages@master
      if: success()
      env:
        ACTIONS_DEPLOY_KEY: ${{ secrets.ACTIONS_DEPLOY_KEY }}
        PUBLISH_BRANCH: gh-pages
        PUBLISH_DIR: ./public
    - name: Purge Cache
      uses: nathanvaughn/actions-cloudflare-purge@master
      if: success()
      env:
        CLOUDFLARE_ZONE: ${{ secrets.CLOUDFLARE_ZONE }}
        CLOUDFLARE_AUTH_KEY: ${{ secrets.CLOUDFLARE_AUTH_KEY }}
    - name: Load Site
      run: curl $(echo $GITHUB_REPOSITORY | cut -d "/" -f 2-) --location --output /dev/null
```

### Breakdown

```yml
on:
  push:
    branches:
    - master
```

I want this workflow to run on every single push to the master branch. I don't have
this set to *every* branch, because I publish the output HTML to the `gh-pages` branch
for [GitHub Pages](https://pages.github.com/) (how I host the site). Plus, if I want to work on a separate branch and not have the changes deployed, I can do so.

```yml
jobs:
  build:

    runs-on: ubuntu-latest
```

You can define multiple "jobs" per workflow, but mine just has one called "build".
I want it to run on the latest build of Ubuntu.

```yml
    steps:
    - name: Checkout code
      uses: actions/checkout@master
      with:
        submodules: true
```

This is where the steps of the job start. To begin, I use the latest copy of the premade
[checkout](https://github.com/actions/checkout) action to `git clone` my repository
and initialize all submodules (though I don't use any submodules currently for my main
site).

```yml
    - name: Install Node
      uses: actions/setup-node@master
```

Next I use the premade [setup-node](https://github.com/actions/setup-node) action
to setup NodeJS and npm.

```yml
    - name: Install dependencies
      run: npm install
```

After that, I simply run the `npm install` command to install all the dependencies.
Since I'm using the [hugo-bin](https://www.npmjs.com/package/hugo-bin) package,
this also sets up Hugo for me. While I *could* run a different script
to download and install Hugo, doing it in one shot with npm just makes things easier.

```yml
    - name: Build Critical CSS
      run: npm run critical
```

Next, I run my npm script to start the Hugo server, and generate the critical CSS.

```yml
    - name: Build Site
      run: npm run build
```

Then, I run my npm script to build the site (CSS, JS, Hugo) as described above.

```yml
    - name: Deploy Site
      uses: peaceiris/actions-gh-pages@master
      if: success()
      env:
        ACTIONS_DEPLOY_KEY: ${{ secrets.ACTIONS_DEPLOY_KEY }}
        PUBLISH_BRANCH: gh-pages
        PUBLISH_DIR: ./public
```

Afterwards, I use [an action](https://github.com/peaceiris/actions-gh-pages)
from the Marketplace to automatically commit and push all the changes to the `./public` directory
to my `gh-pages` branch. The `if: success()` statements means this step will only run
if the previous step ran successfully. This is important, as I don't want to commit a
broken site build.

```yml
    - name: Purge Cache
      uses: nathanvaughn/actions-cloudflare-purge@master
      if: success()
      env:
        CLOUDFLARE_ZONE: ${{ secrets.CLOUDFLARE_ZONE }}
        CLOUDFLARE_AUTH_KEY: ${{ secrets.CLOUDFLARE_AUTH_KEY }}
```

This uses a custom action
[I made](https://github.com/nathanvaughn/actions-cloudflare-purge) to purge
Cloudflare's cache of my site. Otherwise, old CSS or JS can get cached for too
long leading to things breaking. This uses
[repository secrets](https://help.github.com/en/articles/virtual-environments-for-github-actions#creating-and-using-secrets-encrypted-variables)
passed in as environment variables to securely store important tokens.

```yml
    - name: Load Site
      run: curl $(echo $GITHUB_REPOSITORY | cut -d "/" -f 2-) --location --output /dev/null
```

To finish it off, I do a `curl` pull of my site to ensure it's working properly.

The `echo $GITHUB_REPOSITORY | cut -d "/" -f 2-` command is simply taking the
`GITHUB_REPOSITORY` environment variable, which gives the author and repository name
as a single string (like `nathanvaughn/nathanv.me`) and returns everything
past the first `/`.

The `--location` flag tells `curl` to follow redirects
(since my site redirects to HTTPS) and `--output /dev/null` just prevents
the return HTML from being spit out to the console.

## My Blog Actions Workflow

While the above covered how I setup my website with Actions, the workflow for
my blog is extremely similar. As I don't use my own theme for my blog,
I don't use any npm scripts. Therefore, to build the site with Hugo,
I use someone else's [custom action](peaceiris/actions-hugo). The other steps are all the same.

## Other Uses

There's all sorts of stuff you can do with Actions too.

I currently have a repository for a Dockerfile of a web app I use.
I have a [workflow setup](https://github.com/NathanVaughn/webtrees-docker/blob/master/.github/workflows/main.yml)
which checks the latest version
of the underlying web app, and if a new version
has been released (stable, beta, or alpha), it automatically updates the Dockerfile
to reflect the new version on the appropriate branch of my repo, and commits
the change. This will cause Docker Hub to automatically build, tag, and publish the
image. No more subscribing to RSS release feeds and doing updates manually
(to be fair, most of this is done with a Python script run on a schedule by Actions).

Another example is my main website again. I have a [separate workflow](https://github.com/NathanVaughn/nathanv.me/blob/master/.github/workflows/linkchecker.yml)
setup which runs weekly, and checks all the links on the site to see if they're broken,
and automatically creates GitHub issues for the links that don't work.

## Conclusion

GitHub Actions is extremely powerful, flexible, and best of all, **free**
(for public repos).
There are tons of possibilities, such as running tests, automating administrative tasks,
doing deployments, or anything else. I'm excited to see where GitHub and the community
take the product.

## References
- https://help.github.com/en/categories/automating-your-workflow-with-github-actions
- https://help.github.com/en/articles/events-that-trigger-workflows
- https://help.github.com/en/articles/contexts-and-expression-syntax-for-github-actions
- https://github.com/sdras/awesome-actions