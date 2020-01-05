---
author: Nathan Vaughn
cover: /img/sun-ultra-24-build/new_home.jpg
date: "2020-01-05"
description: Building a server inside an old Sun Ultra 24 case
images:
- /img/sun-ultra-24-build/new_home.jpg
tags:
- pc building
- self-hosting
title: Sun Ultra 24 Server Build
---

## Background

Early last year, I went to my university's surplus store. I was looking to
purchase an
[old Mac Pro tower](https://en.wikipedia.org/wiki/Mac_Pro#1st_generation_(Tower))
with the intent to do a case mod with it, since I knew the surplus store had a
few available for cheap and I thought it would be a fun project. 
However, while looking around, I spotted a beautiful
[Sun Ultra 24](https://en.wikipedia.org/wiki/Ultra_24) on the shelf. I quickly
decided to purchase that instead for two reasons.

1. The novelty value, as Sun Microsystems is long-gone.
2. It has standard ATX parts, while a Mac Pro was going to require liberal application
of a Dremel.

{{< figure src="/img/sun-ultra-24-build/from_surplus.jpg" alt="Sun Ultra 24 from surplus" position="center" style="border-radius: 8px;" caption="My Sun Ultra 24 after taking it home from surplus." captionPosition="center" >}}

## Build

Before I started my build, I did notice 
[ServeTheHome's build](https://www.servethehome.com/introducing-the-ultra-epyc-amd-powered-sun-ultra-24-workstation/)
in the exact same case. While I like their build a lot, I also wanted to
shoot for an as original appearance as possible with mine.

### Pre-Build Configuration

I kind of forgot to take pictures before I gutted the case, so below is
what a Sun Ultra 24 is supposed to look like. Mine looked about the same,
except a lot more dust, scratches, and missing parts.

{{< figure src="/img/sun-ultra-24-build/old_insides.jpg" alt="Brand-new Sun Ultra 24 insides" position="center" style="border-radius: 8px;" caption="Brand-new Sun Ultra 24 insides" captionPosition="center" >}}

{{< figure src="/img/sun-ultra-24-build/old_exterior.jpg" alt="Sun Ultra 24 exterior" position="center" style="border-radius: 8px;" caption="Sun Ultra 24 exterior" captionPosition="center" >}}

### Parts
While I initially was planning on swapping out the components of my desktop into
this case, I ended up building a server inside of it. I was getting _real_ tired
of the constant noise from my [HP ProLiant DL 360]({{< relref "self-host-docker.md" >}})
and thought it would be best to build a "new" machine. The perfect opportunity came
during Black Friday this year with a Ryzen 7 2700x for $159.00. I decided replace my
old i7-4790k with that, and use the old parts from my desktop to build a new server.

[PCPartPicker Part List](https://pcpartpicker.com/list/C7kfmg)

Type|Item|Status|
:----|:----|:----|
**CPU** | [Intel Core i7-4790K 4 GHz Quad-Core Processor](https://pcpartpicker.com/product/6vzv6h/intel-cpu-bx80646i74790k) | Already Owned|
**CPU Cooler** | [Cooler Master Hyper 212 EVO 82.9 CFM Sleeve Bearing CPU Cooler](https://pcpartpicker.com/product/hmtCmG/cooler-master-cpu-cooler-rr212e20pkr2) | Purchased|
**Motherboard** | [Asus Z97-AR ATX LGA1150 Motherboard](https://pcpartpicker.com/product/VfK7YJ/asus-motherboard-z97ar) | Already Owned|
**Memory** | [Patriot Viper 3 Low Profile Blue 8 GB (2 x 4 GB) DDR3-1600 Memory](https://pcpartpicker.com/product/bQFPxr/patriot-memory-pvl38g160c0kb) | Already Owned|
**Memory** | [Patriot Viper 3 Low Profile Black 8 GB (2 x 4 GB) DDR3-1600 Memory](https://pcpartpicker.com/product/kBNp99/patriot-memory-pvl38g160c0k) | Already Owned|
**Storage** | [Western Digital Caviar Blue 320 GB 3.5" 7200RPM Internal Hard Drive](https://pcpartpicker.com/product/rd7wrH/western-digital-internal-hard-drive-wd3200aajs) | Purchased|
**Power Supply** | [EVGA BR 450 W 80+ Bronze Certified ATX Power Supply](https://pcpartpicker.com/product/xDMwrH/evga-br-450w-80-bronze-certified-atx-power-supply-100-br-0450-k1) | Purchased|
**Case**| Sun Ultra 24 | Already Owned|

I also liberated the 4-port gigabit network card from my ProLiant.

### Post-Build Configuration

Here's the result, since I also forgot to take pictures during the build.

{{< figure src="/img/sun-ultra-24-build/new_insides.jpg" alt="Post-build computer" position="center" style="border-radius: 8px;" caption="My 'new' Sun Ultra 24" captionPosition="center" >}}

I know there's a mess of power supply cables at the top, but there's no window
on this case so I don't care.

## Problems

Oh my goodness, this was the most frustrating computer build I have ever done.
There were so many problems. Some, I had the foresight to anticipate. Some, not.
Here they are in no particular order.

### Power Supply Cable Length

I was initially hoping to use the power supply that came with the computer
since it was a perfectly adequate 530W supply. Unfortunately, it was made
specifically for that chassis, and the 24-pin ATX power cable was about 3 inches too
short. Thankfully, I had already purchased a new EVGA 450W power supply in the event
I wasn't able to use the old power supply.

### Power Supply Orientation

This wasn't really a problem, but I was surprised that unlike most modern cases,
the power supply only fits one direction. Thankfully, I didn't have 
[the problem](https://www.servethehome.com/introducing-the-ultra-epyc-amd-powered-sun-ultra-24-workstation/5/#attachment_32156) 
that ServeTheHome did with their power supply.

{{< figure src="/img/sun-ultra-24-build/new_power_supply.jpg" alt="New power supply installed" position="center" style="border-radius: 8px;" caption="New power supply installed" captionPosition="center" >}}

### Motherboard Rubber Standoff

Unfortunately, I didn't get a picture of this, but behind the motherboard are
two rubber standoffs. Well, with a new Hyper 212 EVO installed, one of these
rubber standoffs interferes with the mounting bracket. Thankfully, it was easily
ripped off.

### Front Panel Connector Cables

Most of the front panel connectors ended up being useless. My motherboard
doesn't even have FireWire headers so I removed those cables completely. The USB header
cable was barely long enough, but made it. On the other hand, the audio header cable was
nowhere near long enough. However, since I was only planning on using this
machine as a server, and this motherboard already had some audio issues from
a previous ESD incident, I decided to just remove this cable too.

### Missing PCIe Slot Covers

I already knew about this when I bought the system, but it was missing some PCIe
slot covers. Since I don't like missing pieces, I bought 
[some spares](https://www.amazon.com/gp/product/B07TXBGGDM) on Amazon,
but unfortunately they don't quite match.

{{< figure src="/img/sun-ultra-24-build/new_pcie_slots.jpg" alt="Mismatched PCIe slot covers" position="center" style="border-radius: 8px;" caption="Mismatched PCIe slot covers" captionPosition="center" >}}

### Missing Drive Sleds

I was also disappointed when I bought the system that either the computer never came
with all the drive sleds, or they were removed at some point. Either way, if I ever
want to add more hard drives, I'll need to source 
[some from eBay](https://www.ebay.com/itm/Lot-of-5-Sun-Microsystems-HDD-Hot-Swap-3-5-Hard-Drive-Disk-Tray-Caddy-20-screw/153755065494) 
or something. I haven't purchased any yet, since the cost of them would nearly equal
what I paid for the entire computer.

### Missing Ultra 24 Badge

As you can see in the [old exterior photo](/img/sun-ultra-24-build/from_surplus.jpg), 
a the bottom, the 
[Ultra 24 badge](https://www.servethehome.com/wp-content/uploads/2019/01/The-Ultra-EPYC-Cover.jpg) 
is missing. I'm going to try and 3D print a replacement at some point.

### Fan Noise

The whole point of this build was to have a quieter computer. I quickly discovered that
the rear case fan is _bloody_ loud, which defeated the entire purpose of this project.
This fan has a very weird mount which doesn't make it easy to just replace with a 
new fan. 

{{< figure src="/img/sun-ultra-24-build/old_fan.jpg" alt="Sun Ultra 24 rear case fan mount" position="center" style="border-radius: 8px;" caption="Sun Ultra 24 rear case fan mount" captionPosition="center" >}}

Thankfully, I was able to go into the BIOS and disable the fan until
the CPU reaches a pretty high temperature. With the minimal CPU load of this machine,
and the Hyper 212 EVO cooling the processor, the fan has yet to come on.

### Front Panel Header

This was the worst thing by far. I hadn't realized that the front panel header
(power switch, power LED, etc.) is not standardized.

This is the front panel header for the Sun Ultra 24.

{{< figure src="/img/sun-ultra-24-build/old_header.jpg" alt="Sun Ultra 24 front panel header" position="center" style="border-radius: 8px;" caption="Sun Ultra 24 front panel header" captionPosition="center" >}}

This is the front panel header for my Asus Z97-AR.

{{< figure src="/img/sun-ultra-24-build/asus_z97-ar_header.jpg" alt="Asus Z97-AR front panel header" position="center" style="border-radius: 8px;" caption="Asus Z97-AR front panel header" captionPosition="center" >}}

As you can see, the Ultra 24 has **more** pins than my Asus motherboard. In order to
rectify this, I bought some 
[jumper wire extensions](https://www.amazon.com/gp/product/B07BVS3FX7) from Amazon
and used some trial-and-error and help from 
[this forum post](https://forums.tomshardware.com/threads/front-panel-connector-pin-outs.3236564/) 
to connect everything.

{{< figure src="/img/sun-ultra-24-build/new_header.jpg" alt="New front panel header connection" position="center" style="border-radius: 8px;" caption="New front panel header connection" captionPosition="center" >}}

It's ugly but it works. 

Here is the pinout I figured out for reference:

Ultra 24|Connection|
:----|:----|
Red | Probably +12V|
Black | Probably GND|
Green | PWR LED +|
Blue | PWR LED -|
Yellow | PWR SW|
White | PWR SW|

The power switch is just shorting two pins, so positive versus negative doesn't matter.

## Conclusion

Overall, I'm happy with the build. Despite all the problems, it has ended up working
well, and it's nearly dead-silent. My only complaint is the power LED is 
incredibly bright, especially at night. I had some problems transferring my data
from my old server to it, but that's beyond the scope of this post.

{{< figure src="/img/sun-ultra-24-build/new_home.jpg" alt="Post-build computer" position="center" style="border-radius: 8px;" caption="The computer in it's new home" captionPosition="center" >}}
