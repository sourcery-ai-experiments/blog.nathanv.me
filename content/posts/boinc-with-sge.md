+++
title = "Integrating BOINC with Sun Grid Engine"
date = "2019-07-05"
author = "Nathan Vaughn"
tags = ["High-Performance Computing", "Sun Grid Engine", "BOINC"]
description = "Getting BOINC to work on a High-Performance Cluster that uses Sun Grid Engine for job scheduling to donate extra compute time"
+++

## Background

Recently, I setup a small High-Performance Computing (HPC) cluster for Iowa State's
solar car team. This cluster was primarily used for running
Computational Fluid Dynamics (CFD) and MATLAB code. However, whenever the team
was in the build phase and not actively designing the next car, the cluster
sat idle the vast majority of the time. We decided that we should donate the extra
compute time to scientific research.

## Introducing BOINC

We decided that BOINC would be the best way to donate our extra compute time.
In case you're not aware, [BOINC](https://boinc.berkeley.edu/) stands for
Berkeley Open Infrastructure for Network Computing. Basically,
it's a way for people to have their personal computers
donate extra computational capacity to various scientific research projects and
is run by University of California, Berkeley. Being designed for home computers
will prove to be problematic.

## Installing BOINC

The first challenge was simply installing BOINC. To avoid as many configuration changes
as possible, we prefer to install applications to our network file share rather than
locally on each compute node. Also, all of our compute nodes are headless, and BOINC
usually ships with a GUI manager. This quickly rules out simply using the
package manager and the prebuilt binaries available are severely out-of date. This
leaves us with compiling from source.

```bash
# change directories to network file share
cd /share/apps
# clone repo
git clone https://github.com/BOINC/boinc
# move into repo
cd boinc
# run setup script
./_autosetup
# run configure script with file share path, and disable GUI BOINC manager
./configure --prefix="/share/apps/boinc" --disable-manager
# run make multithreaded
make -j
```

## Creating Account(s)

In order to use BOINC, you need to create an account with each project you want
to contribute to and attach your hosts to it. This can be extremely tedious,
so using a service like [BOINC Account Manager](https://boincstats.com/en/bam/) (BAM)
is highly recommended. Once you select some projects, you can also check the option
"Attach new host by default?" so that everything is automatic.

The only issue I've had with BAM, is that my work profile was not being added to new
hosts by default.

## Configuring SGE

The next challenge was that BOINC is designed to only be run on a single computer
and is *not* built around Message Passing Interface (MPI) like most applications that
run on HPC clusters. To get around this, we created a separate queue in our job
scheduler (Son of Grid Engine (SGE, an open-source fork of Sun Grid Engine)) with a
single slot per compute node, so that if a BOINC job got scheduled on a node,
it would be reserved the entire node. Make sure that the user account you will be
using for BOINC has access to this queue and the compute nodes.

### Important Setting

An important setting needs to be set in SGE so that other jobs have higher priority.
For every other queue that you have, set the BOINC-specific queue to be a subordinate
with a max slot count as 1. That way, if **any** other jobs come into the queue, they
will take priority over the BOINC job.

## Starting BOINC

Next, we need to setup how BOINC will be launched.

### Array Job

Launching a job across multiple hosts is easy with SGE with array jobs. We can write
a small Bash script to parse how many slots are available in the BOINC queue
and launch an array job for that many:

```bash
#!/bin/bash

BOINC_SLOTS=`qstat -g c -q boinc.q | tail -1 | sed -e "s/ [ ]*/ /g" | cut --delim=\  -f 5`

qsub -q boinc.q -t 1-${BOINC_SLOTS} -o boinc_out.txt -j y -cwd -N Boinc /home/boinc/runBoinc.sh
```

### BOINC Client

Launching the client is trickier. BOINC doesn't like sharing a directory with other
running instances, so each host needs it's own directory to work out of. Also, we want
to attach each instance to our account manager. Lastly, we need to launch the client
in interactive mode so the job is considered running by SGE. If you let BOINC
launch in the background like it wants to by default, SGE will think the job
has completed and mark the node as available.

Example script:

```bash
#!/bin/bash

USERNAME=yourusername
PASSWORD=yourpassword
HOST=`hostname -s`

CLIENT_BASE=/share/apps/boinc/client/
DATA_BASE=/home/boinc/boinc_data

DATA_DIR=$DATA_BASE/$HOST

# stop any existing instances
pkill boinc_client

echo "Creating data directory $DATA_DIR"
mkdir -p $DATA_DIR

echo "Clearing lockfile"
rm -f $DATA_DIR/lockfile

# start the client
echo "Starting BOINC client"
$CLIENT_BASE/boinc_client --daemon --dir $DATA_DIR

# wait for client to start
echo "Waiting for BOINC client to start"
sleep 5

cd $DATA_DIR
# make sure account is joined
echo "Attaching account manager"
$CLIENT_BASE/boinccmd --join_acct_mgr http://bam.boincstats.com $USERNAME $PASSWORD || true
# sync
echo "Syncing account manager"
$CLIENT_BASE/boinccmd --acct_mgr sync

# stop client from daemon mode and restart on interactive
echo "Stopping BOINC client"
$CLIENT_BASE/boinccmd --quit

# give the client time to stop
sleep 60
pkill boinc_client

echo "Restarting BOINC client in interactive mode"
$CLIENT_BASE/boinc_client --dir $DATA_DIR

```

## Conclusion

That's it! You should now be able to run your array job submission script which will
start a BOINC process on each available host. If any new jobs come in, the BOINC
jobs will be paused until the entire host is available again.

### References

  - [https://boinc.berkeley.edu/wiki/Boinccmd_tool#Miscellaneous](https://boinc.berkeley.edu/wiki/Boinccmd_tool#Miscellaneous)
  - [http://wiki.gridengine.info/wiki/index.php/Integrating\_BOINC\_and\_Grid\_Engine](https://web.archive.org/web/20151225051901/http://wiki.gridengine.info/wiki/index.php/Integrating\_BOINC\_and\_Grid\_Engine)
  - [https://boinc.berkeley.edu/wiki/Client\_configuration_#Command-line\_options](https://boinc.berkeley.edu/wiki/Client\_configuration\_#Command-line_options)