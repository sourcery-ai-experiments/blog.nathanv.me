---
author: Nathan Vaughn
date: "2020-12-31"
description: A deep dive in how I started my own SAAS business
tags:
- Linkspring
- serverless
- AWS
- flask
- python
title: "How I Built Linkspring"
draft: true
---

## Background

Earlier this year, I publicly released my first ever public web app,
[Linkspring](https://lksg.me). I built every part of it myself.
This took months of effort, and I learned a ton and I wanted to write about it
some. I found that a lot of web app
tutorials online are focused around very small "Hello World" applications,
and don't really explain much about larger application architectures. Most of
what I figured out what just experimentation and figuring out what worked best
for me.

## Objectives

To begin with, let me explain my goals for Linkspring. I knew that I wanted to create
a web app to allow users to create a single page to list social media links.
I had the idea for this seeing lots of YouTube descriptions looking like this:

{{< figure src="img/tested-links.jpg" alt="A long list of links on a Tested video" position="center" style="border-radius: 8px;" caption="A long list of links on a Tested video" captionPosition="center" >}}

I now realize this idea is
[far from original](https://alternativeto.net/software/linktree/), but oh well.

The major reason I wanted to do this was to learn about
[serverless computing](https://aws.amazon.com/serverless/), and build
a true "serverless" application. Ideally, doing this would keep costs low.
I also just really want to teach myself full-stack web app development by doing
a project.

With that out of the way, I had some requirements/goals for myself,
primarily made up of pet peeves.

- Allow users to delete account. Way too many websites don't let
you delete an old account, and I've got tons cluttering up my password manager.
- Allow users to change username at any time.
[Relevant StackOverflow Discussion](https://security.stackexchange.com/questions/175802/is-it-good-or-bad-practice-to-allow-a-user-to-change-their-username)
- Support two-factor authentication. You *have* to get security right the first time,
so I opted to only allow social sign-in.
Then I never have to touch a password, deal with reset emails, TOTP tokens, etc.
- No CSS framework. I wanted to build this from the ground up.
- As much server-side rendering as possible. I hate client-side rendering. It's
almost always slower, and puts the burden on the client.
- Infrastructure as code. I wanted to be able to clone a repo, run a few commands,
and have everything be deployed.
- Testing. I had never done automated testing in any of my own projects despite
working on writing automated tests for avionics software for close to 6 months.
- Not support Internet Explorer. Internet Explorer is a disease to the world of web dev,
and I from the start decided that it was never getting any support.

## Frameworks

Selecting the tooling and frameworks and things for a project I think
is more important than some people think. It's almost a form of vendor lock-in.
I ended up using a *ton* dependencies, but here is the high-level overview.

### Back-end

For the back-end language,
I went with Python and [Flask](https://palletsprojects.com/p/flask/).
The reason for this is that I really like Python, and am comfortable with it.
I didn't want to be fighting to learn a backend language along with front-end work.
That's about it.

In terms of Python web frameworks, Flask one of the most popular.
I choose not to go with [Django](https://www.djangoproject.com/),
as its quite opinionated, and more oriented towards a SQL-based database,
which I didn't want to go with, to keep things serverless.
Flask is definitely more "DIY" than Django, but I kind
of wanted that, in order to have full control. I had also used Flask
before, so I had some experience with it.

For Python packages and Flask extensions, the major ones are
[Flask-Login](https://flask-login.readthedocs.io/en/latest/),
[Flask-Caching](https://flask-caching.readthedocs.io/en/latest/),
[pynamodb](https://pynamodb.readthedocs.io/en/latest/), and
[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html).
Flask-Login, pretty obviously, helps handle the authentication of pages
and the user session. As there are no passwords on Linkspring, OAuth
sign-in is handled by a separate library. Flask-Caching is another major
dependency, as this handles all the server-side caching. Pynamodb is a
Python ORM that I use to help interact with the DynamoDB that I use to
store persistent information. Lastly, I use the boto3 library to interact with
[S3](https://aws.amazon.com/s3/) to store images and
[SNS](https://aws.amazon.com/sns/) to send internal application notifications.

TODO serverless

In terms of the cloud back-end, I chose to go with AWS. While I could have built
Linkspring with nearly any cloud provider (they all basically offer the major services
I needed), I chose to go with AWS primarily because their
[cold-start time is the best](https://dashbird.io/blog/ultimate-serverless-benchmark-2019/).
Also, AWS is undoubtedly the king of the clouds right now, so I figured it
would be best to learn their platform. Google Cloud was a close second due
to their [Cloud Firestore](https://cloud.google.com/firestore) product, but
everything I read about Cloud Functions was that it was still sort of buggy and not as
good as Lambda.

For a database, with AWS selected, [DynamoDB](https://aws.amazon.com/dynamodb/) was the
clear choice. I mean, I *wanted* so badly to use a SQL database backend,
(and I nearly threw in the towel at one point)
but it was going to triple my operating costs. I needed to learn about NoSQL databases,
and it's pricing is cheap.

### Front-end

This section is actually a lot shorter.

#### CSS

I didn't want to use a CSS framework since they add so much bloat, and I wanted
to get better at CSS. I opted to try out
[Tailwind](https://tailwindcss.com/) which is an interesting CSS
"framework". It's not a fully-featured design language like Bootstrap or something.
It just provides lots of utility classes that allows you to "write" CSS in HTML.
Examples:

```css
.bg-white {
    background-color: white;
}

.mb-2 {
    margin-botton: 2rem;
}
```

This has two major disadvantages.

1) Your CSS file is huge
2) Your HTML is very markup heavy.

Number 1 is manageable with [PurgeCSS](https://purgecss.com/),
which Tailwind actually ships with in recent versions. This a program that scans
all of your HTML and JS files, and automatically removes any CSS in your CSS file
that isn't used anywhere. This helps to control the size of your final CSS file
while allowing you to import lots of ready-made CSS.

For number 2, Tailwind does allow you to define your own custom
classes made up of other Tailwind classes to help alleviate this. This also really does
encourage reusable templates and components to avoid redefining code.

#### JS

The front-end JavaScript is really minimal so there's no framework or anything.
The only external dependencies I have are [Modernizr](https://modernizr.com/) and
[VanillaToasts](https://github.com/AlexKvazos/VanillaToasts). I wanted
to create some toasts but also didn't want anything that was going to require lots of
dependencies. Almost all of the JS toasts libraries I could find required large
dependencies likes [jQuery](https://jquery.com/).

Modernizr is a feature detection framework. I only use it to check if the requisite
CSS and JS features are available and if not, prompt the user to upgrade their browser.

## Project Structure

{{< figure src="img/folder-structure.png" alt="Linkspring folder structure" position="center" style="border-radius: 8px;" caption="Linkspring folder structure" captionPosition="center" >}}

## Tooling

Dev scripts

PurgeCSS

Parcel

Beautifies

## Business

## Thoughts


### CDN

### Database Consistency

### Caching

### Issues