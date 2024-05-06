Let's talk about domain names. Despite being a strictly digital creation,
they are intertwined with the social and political complexities of the real world.

## Domain Structure

In the beginning, there were six top-level domains (TLDs):

- .com
- .net
- .org
- .edu
- .mil
- .gov

Wait, what is a top-level domain? Let's back up and talk about the parts of a domain
name. As an example, let's use the domain for this site: `blog.nathanv.me`.

`blog.nathanv.me` has 3 parts, seperated by 2 dots (more on that in a second).
From right-to-left:

- `me`: This is referred to as the top-level domain
- `nathanv`: This is the second-level domain, often referred to as just the "domain" or "root domain"
- `blog`: This is known as the subdomain

Notice how we went right-to-left? While English speakers read left-to-right,
domain names are actually heirarchical, with each segment becoming more specific
as you move left. So for `blog.nathanv.me`, the name `blog` is a subdomain of `nathanv`,
which is a subdomain of the Montegro registry `me`.
Some usages of domain names do write the segments left-to-right to make it.
A notable example of this are Android package names.
This site as an Android package name would be `me.nathanv.blog`. Humans tend to
find this less intuitive, but it makes it easier to parse for computers.

As there are dots seperating the parts of a domain name, there is actually
an implied dot at the end of any domain name, as the top-level domain `me`
is actually a subdomain of the DNS root (more on that later). So, you can write
`blog.nathanv.me` as `blog.nathanv.me.` and it will still work just the same.
Try it in your browser! Usually this is left off as us pesky humans are lazy
when the last character of a domain name is always the same.

## History

So, back to top-level domains. On January 1st 1985, the DNS (Domain Name System)
was born. The history is complicated, and Wikipedia goes into great detail about it,
but the short version is that six original top-level domains were created. These were
`.com` meant for companies, `.net` meant for networks, `.org` meant for organizations,
`.edu` reserved for educational institutions, `.mil` reserved for the US military,
and `.gov` reserved for the US government.

In classic American fashion, the creators didn't account for other countries at first.
Since DNS was meant to be a global system, country-specific top-level domains were
added. It was decided that the simplest way to accomplish this was to follow
ISO 3166-1 alpha-2, a standard for 2-character country codes created
by the International Organization for Standardization
(this also avoided the problem of deciding which "countries" are countries,
which is a complicated subject).
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
citizens, residents, or companies.

This intermingling of the digital and physical world does introduce some interesting
problems at times:

- Despite the collapse of the Soviet Union, `.su` domains are still active and available
for purchase.
- `.ly` domains are managed by Libya. In 2010, the country
[revoked `vb.ly`](https://www.zdnet.com/article/libyan-authorities-seize-vb-ly-domain/)
for being associated with adult content.
- Similarly, `.af` domains are managed by Afghanistan. The Taliban
[revoked `queer.af`](https://akko.erincandescent.net/notice/AenvYJ0yiHfspKM8uW)
in 2024.
- `.ac` is for Ascension Island which was being considered for the ISO standard
but ultimately never made the cut.
- `.cs` was for Czechoslovakia, but after the country split into the Czech Republic
and Slovakia, the top-level domain was deleted and `.cz` and `.sk` were created to
replace it.
- Despite not being a country, the European Union has the `.eu` top-level domain. After
Brexit, UK residents who owned `.eu` domains were forced to give them up.

In 1998, the Internet Corporation for Assigned Names and Numbers (ICANN) was created
to manage the global DNS system. In 2000, ICANN decided there were not enough
generic top-level domains (gTLDs) and announced seven new ones:

- .aero
- .biz
- .coop
- .info
- .museum
- .name
- .pro

Since 2000, there were several more rounds of new gTLDs, however in in 2012, ICANN
began accepting applications for new gTLDs from companies. With a compelling enough
pitch, and a nice pile of cash, you too could have your own top-level domain.
This has created an explosion in top-level domains, with examples including
`.bridgestone` (yes, the tire company), `.irish`, `.zip`, `.mint` and more.

## Software

You likely know that your computer takes a domain name and turns it into an IP address.
But how exactly does it do that?