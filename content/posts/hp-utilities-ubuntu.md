+++
title = "Installing HP ProLiant Utilities on Ubuntu Server"
date = "2019-07-21"
author = "Nathan Vaughn"
tags = ["Ubuntu", "HP", "ProLiant"]
description = "Installing HPE Linux Management Component Pack on Ubuntu on a Gen 5 server"
+++

## Background

As mentioned in my ["Self-Hosting with Docker and Argo Tunnel"](../self-host-docker)
post, I bought a HP DL360 G5 server a little while back. I'm most comfortable with Ubuntu Server,
so I opted to install that on the sever. I recently learned that HP has utilities
you can install on Linux to modify and view system-level settings and information, which
is pretty cool.

I wanted to try them out, however, my server being a Gen 5, has not been supported for a long time
and Ubuntu isn't part of the of the group of OSs (Red Hat and SUSE)
that get [Service Packs](https://downloads.linux.hpe.com/SDR/project/spp/).
So the documentation and support is minimal, and it took
me a bit of time to figure everything out.

**Disclaimer: I'm working on a Gen 5 server, so things may vary.**

## Installation

First, in order to install the utilities, you need to add the source to `apt`:

```bash
sudo echo "deb http://downloads.linux.hpe.com/SDR/repo/mcp bionic/current non-free" > /etc/apt/sources.list.d/mcp.list
```

Next, you need enroll HPE's public keys:

```bash
curl http://downloads.linux.hpe.com/SDR/hpPublicKey1024.pub | apt-key add -
curl http://downloads.linux.hpe.com/SDR/hpPublicKey2048.pub | apt-key add -
curl http://downloads.linux.hpe.com/SDR/hpPublicKey2048_key1.pub | apt-key add -
curl http://downloads.linux.hpe.com/SDR/hpePublicKey2048_key1.pub | apt-key add -
```

Now, you just need to update your `apt` sources, and install the utilities.

```bash
sudo apt update
sudo apt install hp-health hponcfg amsd ams ssacli ssaducli ssa
```

Despite the names of the packages listed on
[HPE's page](https://downloads.linux.hpe.com/SDR/project/mcp/),
I found that some of the packages simply didn't exist, or had different
names.

## Utilities Overview

All of these utilities require being run as root.

### hp-health

#### What Is It

"HPE System Health Application and Command line Utilities (Gen9 and earlier)"

Basically lets you view and adjust a lot of system-level settings from the command line.

#### Command

```bash
hpasmcli
```

#### Example

```
nathan@zeus:[~]$ sudo hpasmcli
HPE management CLI for Linux (v2.0)
Copyright 2015 Hewlett Packard Enterprise Development LP.

--------------------------------------------------------------------------
NOTE: Some hpasmcli commands may not be supported on all Proliant servers.
      Type 'help' to get a list of all top level commands.
--------------------------------------------------------------------------
hpasmcli> help
CLEAR  DISABLE  ENABLE  EXIT  HELP  NOTE  QUIT  REPAIR  SET  SHOW
hpasmcli> show temp
Sensor   Location              Temp       Threshold
------   --------              ----       ---------
#1        I/O_ZONE             48C/118F   65C/149F
#2        AMBIENT              24C/75F    40C/104F
#3        PROCESSOR_ZONE       30C/86F    95C/203F
#4        PROCESSOR_ZONE       30C/86F    95C/203F
#5        POWER_SUPPLY_BAY     35C/95F    60C/140F
#6        PROCESSOR_ZONE       30C/86F    95C/203F
#7        PROCESSOR_ZONE       30C/86F    95C/203F

hpasmcli>
```

### hponcfg

#### What Is It

"HPE RILOE II/iLO online configuration utility"

Command-line configuration for iLO

#### Command

```bash
hponcfg
```

#### Example

```
nathan@zeus:[~]$ sudo hponcfg -h
HP Lights-Out Online Configuration utility
Version 5.3.0 Date 3/21/2018 (c) 2005,2018 Hewlett Packard Enterprise Development LP
Firmware Revision = 1.61 Device type = iLO 2 Driver name = hpilo

USAGE:
  hponcfg  -?
  hponcfg  -h
  hponcfg  -m minFw
  hponcfg  -r [-m minFw]
  hponcfg  -b [-m minFw]
  hponcfg  [-a] -w filename [-m minFw]
  hponcfg  -g [-m minFw]
  hponcfg  -f filename [-l filename] [-s namevaluepair] [-v] [-m minFw] [-u username] [-p password]
  hponcfg  -i [-l filename] [-s namevaluepair] [-v] [-m minFw] [-u username] [-p password]

  -h,  --help           Display this message
  -?                    Display this message
  -r,  --reset          Reset the Management Processor to factory defaults
  -b,  --reboot         Reboot Management Processor without changing any setting
  -f,  --file           Get/Set Management Processor configuration from "filename"
  -i,  --input          Get/Set Management Processor configuration from the XML input
                        received through the standard input stream.
  -w,  --writeconfig    Write the Management Processor configuration to "filename"
  -a,  --all            Capture complete Management Processor configuration to the file.
                        This should be used along with '-w' option
  -l,  --log            Log replies to "filename"
  -v,  --xmlverbose     Display all the responses from Management Processor
  -s,  --substitute     Substitute variables present in input config file
                        with values specified in "namevaluepairs"
  -g,  --get_hostinfo   Get the Host information
  -m,  --minfwlevel     Minimum firmware level
  -u,  --username       iLO Username
  -p,  --password       iLO Password
```

### amsd

#### What Is It

"HPE Agentless Management Service (Gen10 only)"

#### Command

```bash
amsd
```

#### Example

¯\\\_(ツ)\_/¯

I have a Gen 5 server, so it doesn't do anything.

### ams

#### What Is It

"HPE Agentless Management Service (Gen9 and earlier)"

#### Command

```bash
ams
```

#### Example

¯\\\_(ツ)\_/¯

It requires an X server running, so I don't know what it does.

### ssacli

#### What Is It

"HPE Command Line Smart Storage Administration Utility"

Command-line utility to view/modify storage arrays.

#### Command

```bash
ssacli
```

#### Example

```sh
nathan@zeus:[~]$ sudo ssacli ctrl all show config

Smart Array E500 in Slot 1                (sn: PAFGH0K9XXXXXX)


   Port Name: 1E

   Port Name: 2E


Smart Array P400i in Slot 0 (Embedded)    (sn: PH87XXXXXX    )



   Internal Drive Cage at Port 1I, Box 1, OK


   Port Name: 1I

   Port Name: 2I

   Array A (SAS, Unused Space: 4  MB)

      logicaldrive 1 (136.67 GB, RAID 5, OK)

      physicaldrive 1I:1:1 (port 1I:box 1:bay 1, SAS HDD, 72 GB, OK)
      physicaldrive 1I:1:2 (port 1I:box 1:bay 2, SAS HDD, 72 GB, OK)
      physicaldrive 1I:1:3 (port 1I:box 1:bay 3, SAS HDD, 72 GB, OK)
```

### ssaducli

#### What Is It

"HPE Command Line Smart Storage Administration Diagnostics"

Command-line utility to diagnose storage arrays.

#### Command

```bash
ssaducli
```

#### Example

```bash
# Generates report
sudo ssaducli -adu -txt -f filename.txt
```

### ssa

#### What Is It

"HPE Array Smart Storage Administration Service"

This appears to do the same thing as the diagnostic tool plus a bit more.

#### Command

```bash
ssa
```

#### Example

```bash
# Generates report
sudo ssa -diag -txt -f filename.txt
```

## Conclusion

Despite some hiccups, With these utilities installed, I can now modify basically
all of the BIOS and iLO settings without needing a keyboard or monitor. I don't think
I have any need anymore to go into the BIOS maybe other than maybe modifying the
RAID array configuration (which would wipe everything).

### References

   - [https://downloads.linux.hpe.com/SDR/project/mcp/](https://downloads.linux.hpe.com/SDR/project/mcp/)
   - [https://downloads.linux.hpe.com/SDR/keys.html](https://downloads.linux.hpe.com/SDR/keys.html)
   - [https://binaryimpulse.com/2013/09/installing-hp-array-configuration-utility-hp-acu-on-ubuntu-12-04/](https://binaryimpulse.com/2013/09/installing-hp-array-configuration-utility-hp-acu-on-ubuntu-12-04/)