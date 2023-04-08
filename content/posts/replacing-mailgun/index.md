---
author: Nathan Vaughn
date: "2020-02-09"
description: Replacing Mailgun with SendGrid and ForwardEmail
tags:
  - email
  - DNS
title: Replacing Mailgun
---

## Background

For the past few years, I've used [Mailgun](https://www.mailgun.com) to send and
receive email for my `nathanv.me` domain. I intentionally signed up Mailgun because it
was part of the
[GitHub Student Developer Pack](https://education.github.com/pack/offers)
and it worked great. I could send email from applications and my personal
Gmail account using SMTP credentials and forward
any inbound mail to my Gmail account, all in the free tier. This allowed me to send
receive email to and from the `@nathanv.me` domain,
all while never actually having an actual email account for it. I really liked this,
since it gave me the vanity email address, `nathan@nathanv.me`
that I could put on my resume.
However, just a few days ago, I received this email from Mailgun:

{{< figure src="img/mailgun-email.jpg" alt="Mailgun email" caption="Mailgun plan changes" captionPosition="center" >}}

Okay... does this affect me at all?

{{< figure src="img/mailgun-plans.jpg" alt="Mailgun plans" caption="<i>Crap...</i>" captionPosition="center" >}}

As you can see in the picture above, inbound emails are no longer included in the free
plan (and now costs $75/month) and after 3 months I'll have to actually pay for the
emails I send. I don't care about the cost of emails. They're cheap after all, and
I understand that running email servers costs money. However, now charging $75/month
for the ability to receive email is not something I want to pay for. Time for a new
solution.

## Options

Here are some potential options I considered.

### Other Transactional Email Services

I looked into a _bunch_ of different transactional email providers (SendGrid, AWS SES,
PostSpark, etc.) and they all fell into a combination of three categories:

1. No support for inbound email
2. Inbound email is an expensive tier
3. Inbound email can only be sent to webhook

I couldn't find any providers that could forward email like Mailgun lets you.
The closest thing I could find was a
[blog post from AWS](https://aws.amazon.com/blogs/messaging-and-targeting/forward-incoming-email-to-an-external-destination/),
explaining how to setup inbound email forwarding, but this requires additional code,
setup, and AWS services.

### Google Domains Email Forwarding

As I register all of my domain names through Google Domains,
another option I considered was using Google Domain's free inbound email forwarding.
However, this only works if you set the domain's name servers to Google's, so they
can setup the records.

{{< figure src="img/google-domains-email-forwarding.jpg" alt="Google Domains email forwarding" caption="Google Domains email forwarding" captionPosition="center" >}}

Unfortunately, I really like Cloudflare for DNS and caching. While I think I could just
swap the name server to Google, setup the email forward, and then swap it back to
Cloudflare, I don't want to run the risk of Google figuring out my ruse, and stop
delivering my emails.

Also, this still doesn't solve my problem for outbound emails.

### ForwardEmail.net/ImprovMX

While researching my problem, I also discovered
[ForwardEmail.net](https://forwardemail.net/en) and
[ImprovMX](https://improvmx.com/), which both offer free email forwarding.
Again though, these only forward inbound emails, and don't offer a way to send email.

## What I Went With

I initially attempted to get things setup with AWS using SES, S3, and Lambda.
However, after discovering that by default, you can only send emails to verified
addresses without contacting support, and I had a lot of trouble dealing with IAM
and permissions, I gave up and went with ForwardEmail and SendGrid.

I choose SendGrid for outbound emails as it was part of the GitHub Student Developer
Pack. It was very simple to setup with just a few `CNAME` records to setup DKIM/SPF.

{{< figure src="img/sendgrid_dns.jpg" alt="SendGrid dNS" caption="SendGrid DNS" captionPosition="center" >}}

Setting up ForwardEmail was a little bit harder. There are a lot more
[DNS records](https://forwardemail.net/en/faq#how-do-i-get-started-and-set-up-email-forwarding)
you need to setup.

{{< figure src="img/fordwardemail_dns.jpg" alt="ForwardEmail DNS" caption="ForwardEmail DNS" captionPosition="center" >}}

The actual DNS records makes sense. I understand why they need
a `MX` record for the incoming mail servers and a
`TXT` record for what email address to forward to.
I'm very confused why they want you to add a `TXT` record for SPF, as I thought
it was only needed for _sending_ emails which this service doesn't do.
ImprovMX [explains this](https://improvmx.com/guides/improvmx-spf-support/) for
their similar service. ForwardEmail has
[a guide](https://forwardemail.net/en/faq#how-to-send-mail-as-using-gmail)
on how to "Send Mail As" with Gmail, but my understanding of that is it is still
being sent by Google's email servers, so I still don't understand why this is needed.
If someone can explain this better, please leave a comment below.

## Conclusion

While I'm sad to see Mailgun go, since it did everything I wanted for free,
I was able to replace it with multiple services, with just DNS changes.
The most painful part of this change will be changing all of my SMTP
credentials on all of my servers and applications that send emails.
The setup was more complicated, but hopefully it'll work better longer term,
and will be easier to replace an individual component if it ever needs to
change in the future.

As always, it was DNS.

{{< figure src="img/its_always_dns.png" alt="DNS Haiku" caption="It was DNS" captionPosition="center" >}}

## References

- [https://www.mailgun.com](https://www.mailgun.com)
- [https://forwardemail.net/en](https://forwardemail.net/en)
- [https://improvmx.com/](https://improvmx.com/)
- [https://sendgrid.com/docs/ui/account-and-settings/how-to-set-up-domain-authentication/](https://sendgrid.com/docs/ui/account-and-settings/how-to-set-up-domain-authentication/)
