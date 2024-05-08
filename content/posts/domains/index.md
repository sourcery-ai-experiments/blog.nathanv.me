---
author: Nathan Vaughn
date: "2024-05-06"
description: Let's talk about domain names
tags:
  - DNS
  - domains
title: "Domains"
---

Let's talk about domain names. Despite being a strictly digital creation,
they are intertwined with the social and political complexities of the real world.

## Domain Structure

In the beginning, there were six top-level domains (TLDs):

- `.com`
- `.net`
- `.org`
- `.edu`
- `.mil`
- `.gov`

Wait, what is a top-level domain? Let's back up and talk about the parts of a domain
name. As an example, let's use the domain for this site: `blog.nathanv.me`.

`blog.nathanv.me` has 3 parts, seperated by 2 dots (more on that in a second).
From right-to-left:

- `me`: This is referred to as the top-level domain
- `nathanv`: This is the second-level domain, often referred to as just the "domain" or "root domain"
- `blog`: This is known as the subdomain

Notice how we went right-to-left? While English speakers read left-to-right,
domain names are actually heirarchical, with each segment becoming more specific
as you move left [^1]. So for `blog.nathanv.me`,
the name `blog` is a subdomain of `nathanv`, which is a subdomain of the
Montegro registry `me`.

As there are dots seperating the parts of a domain name, there is actually
an implied dot at the end of any domain name, as the top-level domain `me`
is actually a child of the DNS root `.`. So, you can write
`blog.nathanv.me.` and it will still work just the same.
Try it in your browser! Usually this is left off as us pesky humans are lazy
when the last character of a domain name is always the same.

## History

So, back to top-level domains. On January 1st 1985, the DNS (Domain Name System)
was born. The history is complicated, and Wikipedia goes into great detail about it,
but the short version is that six original top-level domains were created. These were:
`.com` meant for companies, `.net` meant for networks, `.org` meant for organizations,
`.edu` reserved for educational institutions, `.mil` reserved for the US military,
and `.gov` reserved for the US government. These are collectively called
the original generic top-level domains (gTLDs).

In classic American fashion, the creators didn't account for other countries at first.
Since DNS was meant to be a global system, country-specific top-level domains were
added. It was decided that the simplest way to accomplish this was to follow
ISO 3166-1 alpha-2, a standard for 2-character country codes created
by the International Organization for Standardization
(this also avoided the problem of deciding which "countries" are countries,
which is it's own complicated subject).
This means *any two-letter top-level domain is managed by a country or territory.*
Of course, the United States had to start first with `.us` in
February of 1985, but other countries quickly followed. These are now
referred to as country-code top-level domains (ccTLDs).

Some countries benefitted quite a bit from these top-level domains. For example,
`.tv` is for the island of Tuvalu, and `.tv` domain registrations makes up an
appreciable portion of the government's revenue. Similarly, `.io` is for the British
Indian Ocean Territory, and `.io` domains are (or at least used to be) quite popular.
As of late, Anguilla has been profiting off of `.ai` domains.

Now, every country is free to manage their own top-level domain as they see fit.
While many smaller countries don't want to look a gift horse in the mouth, some
countries impose restrictions on their domains. For example, `.us` domains are
limited to US citizens, residents, organizations, corporations, or some other
presence in the United States. `.it` domains are similarly restricted to Italian
citizens, residents, or companies. Monaco goes even, only
allowing companies with a trademark registered in Monaco to claim a `.mc` domain.

This intermingling of the digital and physical world introduces
problems at times:

- Despite the collapse of the Soviet Union, `.su` domains are still active and available
for purchase.
- `.ly` domains are managed by Libya. In 2010, the country
[revoked `vb.ly`](https://www.zdnet.com/article/libyan-authorities-seize-vb-ly-domain/)
for being associated with adult content.
- Similarly, `.af` domains are managed by Afghanistan. The Taliban
[revoked `queer.af`](https://akko.erincandescent.net/notice/AenvYJ0yiHfspKM8uW)
in 2024.
- `.ac` is currently for Ascension Island which was being considered
for the ISO standard at the time of creation but ultimately never made the cut.
- `.cs` was for Czechoslovakia, but after the country split into the Czech Republic
and Slovakia, the top-level domain was deleted and `.cz` and `.sk` were created to
replace it.
- Despite not being a country, the European Union has the `.eu` top-level domain. After
Brexit, UK residents who owned `.eu` domains were forced to give them up.

In 1998, the Internet Corporation for Assigned Names and Numbers (ICANN) was created
to manage the global DNS system. In 2000, ICANN decided there were not enough
generic top-level domains and announced seven new ones:

- `.aero`
- `.biz`
- `.coop`
- `.info`
- `.museum`
- `.name`
- `.pro`

Since 2000, there were several more rounds of new gTLDs. However in 2012, ICANN
began accepting applications for new gTLDs from companies. With a compelling enough
pitch, and a nice pile of cash, you too could have your own top-level domain.
This has created an explosion in top-level domains, with examples including
`.bridgestone` (yes, the tire company), `.irish`, `.zip`, `.mint` and more.
At the time of writing, there are over 1,500 top-level domains.

## Software

You likely know that your computer takes a domain name and turns it into an IP address.
But how exactly does it do that? Well, your computer asks a DNS server, such
as [`1.1.1.1`](https://one.one.one.one/), [`8.8.8.8`](https://dns.google/)
or one that your ISP provides. But (ignoring caching) these servers don't actually know
the IP address of the domain you're asking for. Instead, they have to ask the
**Root Name Servers**.

The Root Name Servers bootstrap the global DNS system.
There are 13 of them, named A through M,
run by different organizations, such as NASA, University of Maryland, ICANN, and others.
They have their own second-level domain, `root-servers.net`.
The IP addresses of these servers are well-known and hardcoded into just about every
piece of DNS software (so that you don't have a cyclical problem of trying to
resolve `a.root-servers.net`).

So, the DNS server talks to a randomly selected Root Name Server. But the Root Name
Server doesn't know the IP address of every domain in the world. Instead,
they know what server to talk to for each top-level domain.
Again, let's use this site, `blog.nathanv.me`, as an example:

```bash
$ dig @a.root-servers.net blog.nathanv.me

; <<>> DiG 9.18.18-0ubuntu0.22.04.2-Ubuntu <<>> @a.root-servers.net blog.nathanv.me
; (2 servers found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 61755
;; flags: qr rd; QUERY: 1, ANSWER: 0, AUTHORITY: 5, ADDITIONAL: 11
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;blog.nathanv.me.               IN      A

;; AUTHORITY SECTION:
me.                     172800  IN      NS      b0.nic.me.
me.                     172800  IN      NS      a0.nic.me.
me.                     172800  IN      NS      c0.nic.me.
me.                     172800  IN      NS      a2.nic.me.
me.                     172800  IN      NS      b2.nic.me.

;; ADDITIONAL SECTION:
b0.nic.me.              172800  IN      A       199.253.60.1
b0.nic.me.              172800  IN      AAAA    2001:500:54::1
a0.nic.me.              172800  IN      A       199.253.59.1
a0.nic.me.              172800  IN      AAAA    2001:500:53::1
c0.nic.me.              172800  IN      A       199.253.61.1
c0.nic.me.              172800  IN      AAAA    2001:500:55::1
a2.nic.me.              172800  IN      A       199.249.119.1
a2.nic.me.              172800  IN      AAAA    2001:500:47::1
b2.nic.me.              172800  IN      A       199.249.127.1
b2.nic.me.              172800  IN      AAAA    2001:500:4f::1

;; Query time: 50 msec
;; SERVER: 198.41.0.4#53(a.root-servers.net) (UDP)
;; WHEN: Mon May 06 20:12:04 CDT 2024
;; MSG SIZE  rcvd: 353
```

We can see here that we asked a Root Name Server about `blog.nathanv.me`, and it
didn't give us the IP address, but instead tells us that we need to talk to one of
`b0.nic.me`, `a0.nic.me`, `c0.nic.me`, `a2.nic.me`, or `b2.nic.me` in order to get
the next level of the domain, `nathanv.me`.
It also helpfully provides the IP addresses of these servers so we don't have to
figure that out as well and get stuck in a loop.

Now let's ask `b0.nic.me`:

```bash
$ dig @b0.nic.me blog.nathanv.me

; <<>> DiG 9.18.18-0ubuntu0.22.04.2-Ubuntu <<>> @b0.nic.me blog.nathanv.me
; (2 servers found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 1860
;; flags: qr rd; QUERY: 1, ANSWER: 0, AUTHORITY: 2, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;blog.nathanv.me.               IN      A

;; AUTHORITY SECTION:
nathanv.me.             3600    IN      NS      terin.ns.cloudflare.com.
nathanv.me.             3600    IN      NS      deb.ns.cloudflare.com.

;; Query time: 80 msec
;; SERVER: 199.253.60.1#53(b0.nic.me) (UDP)
;; WHEN: Mon May 06 20:15:47 CDT 2024
;; MSG SIZE  rcvd: 99
```

Again, we can see that the name server `b0.nic.me` still doesn't know the IP address of
`blog.nathanv.me` but it *does* know who to talk to next, `terin.ns.cloudflare.com`
or `deb.ns.cloudflare.com`. These are the name servers for the domain `nathanv.me`.
Usually these are provided by your domain registrar, or in my case, Cloudflare.
Finally, we can ask `terin.ns.cloudflare.com` for the IP address of `blog.nathanv.me`:

```bash
$ dig @deb.ns.cloudflare.com blog.nathanv.me

; <<>> DiG 9.18.18-0ubuntu0.22.04.2-Ubuntu <<>> @deb.ns.cloudflare.com blog.nathanv.me
; (6 servers found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 11690
;; flags: qr aa rd; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;blog.nathanv.me.               IN      A

;; ANSWER SECTION:
blog.nathanv.me.        300     IN      A       104.21.52.60
blog.nathanv.me.        300     IN      A       172.67.195.246

;; Query time: 30 msec
;; SERVER: 108.162.192.92#53(deb.ns.cloudflare.com) (UDP)
;; WHEN: Mon May 06 20:17:41 CDT 2024
;; MSG SIZE  rcvd: 76
```

At last, we have learned that the IP address for `blog.nathanv.me` is either
`104.21.52.60` or `172.67.195.246`. A DNS server that performs these actions is
called a "recursive resolver" as it has to recursively figure out who to ask for
each part of the domain name.

You may be wondering, "Who do these Root Name Servers think they are?
There's nothing special giving them their power other than
collective agreement. I want my own DNS root!"

{{< figure src="img/alt_dns_root.png" alt="Bender from Futurama saying 'We'll make our own DNS root with blackjack and hookers'" >}}

Well, you wouldn't be the first. There are multiple groups that have
created [alternate DNS roots](https://en.wikipedia.org/wiki/Alternative_DNS_root)
with their own Root Name Servers.  Much like cryptocurrency trying to displace the US
dollar, none of them have gained any widespread adoption.

## Applications of DNS

While the above was a simple example of looking for the IP address of a domain name,
there's a lot you can do with DNS. For example, you can use it for load balancing.
If you have multiple servers to run your application, you can configure your DNS
server to randomly return a different IP address each time. Additionally,
one of the most popular uses of DNS for consumer use is ad-blocking. With a server
like [Pi-Hole](https://pi-hole.net/), you can run a DNS server that lies and pretends
that domains that are known to serve ads don't exist. Projects like
[DNS Toys](https://www.dns.toys/) exist that can provide useful information over
the DNS protocol.

DNS can also be used for nefarious purposes. For example, you can use DNS
for data exfiltration. Imagine making a DNS request for
`abcdefghijklmnopqrstuvwxyz.example.com`. Even though this may not be a real domain,
the `example.com` nameserver can log this request. Assuming you control the
`example.com` nameserver, you can later view these requests to non-existent domains.
Replace `abcdefghijklmnopqrstuvwxyz` with sensitive information like credentials
or file contents, and you can easily get data out of a network in a way that is
hard to detect and unlikely to be blocked.

Additionally,
[DNS amplification attacks](https://www.cloudflare.com/learning/ddos/dns-amplification-ddos-attack/)
can be a problem. Basically, an attacker sends a DNS request to a server
and spoofs the IP address that the response should be sent to. As you can see
in the `dig` commands above, the data size of the query is much smaller than the size
of the response, so by sending lots of small queries to a large public DNS server,
an attacker can "amplify" the volume of data they are sending and overwhelm their
target.

## Conclusion

Hopefully you learned something out of this. Wikipedia has lots of information
about the history of DNS and all the weird edge cases that have come up over the years.
I also highly recommend this video by Nill:

{{< youtube 4ZtFk2dtqv0 >}}

Other weird DNS facts:

- `.nato` was created for NATO, but NATO quickly transitioned to using `nato.int`
and it was deleted shortly after, basically unused.
- A lot of people got very upset when Google created the `.dev` top-level domain
as they were using it for development purposes. [RFC 2606](https://datatracker.ietf.org/doc/rfc2606/)
reserves `.example`, `.invalid`, `.localhost`, and `.test` for this purpose,
so they were playing with fire to begin with. `.local` and `.onion` have also
been added to this list. While `.home` and `.corp` are not officially reserved,
they are in pratice as ICANN has rejected proposals to register them.
- A lot of people also got upset when Google created the `.zip` top-level domain
as they feared it would be used to spread malware with applications like Twitter
that recognize URLs without a proceeding `http://` or `https://`.
- The email address [`dot@dotat.at`](https://dotat.at/) is my favorite
[domain hack](https://en.wikipedia.org/wiki/Domain_hack) (read it aloud if you don't
understand it).
- Antarctica has it's own top-level domain, `.aq`.
- `.edu` domains used to have fewer restrictions than they do today. For example,
`merit.edu` was registered and is still active despite not actually being an accredited
educational institution. Most of these domains have been grandfathered in.
- In definace of God and man and all things holy, certain top-level domains
allow emojis. See: <https://mailoji.com/>

## Further Reading

- <https://en.wikipedia.org/wiki/List_of_Internet_top-level_domains>
- <https://en.wikipedia.org/wiki/Root_name_server>
- <https://en.wikipedia.org/wiki/.com>
- <https://www.icann.org/history>

## Footnotes

[^1]:
     Some usages of domain names do write the segments left-to-right.
     A notable example of this are Android package names.
     This site as an Android package would be `me.nathanv.blog`. Humans tend to
     find this less intuitive, but it makes it easier for computers to parse.
