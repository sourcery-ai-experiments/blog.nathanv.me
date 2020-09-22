---
author: Nathan Vaughn
date: "2020-09-08"
cover: img/cover.png
description: How to install the Spin model checker on Windows
images:
- /posts/spin-windows/img/cover.png
tags:
- Windows
title: Spin Model Checker on Windows
userelativecover: true
---

## Introduction

For a class, I was trying to install the [Spin](https://spinroot.com/)
formal verification tool *somehow* on my Windows computer. I couldn't find
a good guide, so this is what I figured out.

While you *can* do this with WSL or Cygwin, Spin now has prebuilt Windows
binaries available, so I think this is easier.

## Prerequisites

You'll need the following software installed:

- [7zip](https://www.7-zip.org/)

The following will make life easier:

- [Git for Windows](https://git-scm.com/download/win)
- [Everything](https://www.voidtools.com/)

## Downloading/Extracting Spin

First, go to the Spin [GitHub page](https://github.com/nimble-code/Spin). If you 
already have Git installed, you can just clone this. Or, if you'd like,
you can go to `Bin` directory, and click on the latest version of
`spin<ver>_windows64.exe.gz`. Click "Download" on the right side to get
only this file.

{{< figure src="img/download_spin.jpg" alt="Download the latest prebuilt version of Spin" position="center" style="border-radius: 8px;" caption="Download the latest prebuilt version of Spin" captionPosition="center" >}}

Once that's downloaded, use 7zip to extract the archive.

{{< figure src="img/extract_spin.jpg" alt="Extract the archive with 7zip" position="center" style="border-radius: 8px;" caption="Extract the archive with 7zip" captionPosition="center" >}}

Inside the directory it extracted into will be an executable. Rename this to `spin.exe`.
Now, if you only want the command-line version of Spin, you're basically done.
You'll just need to use the full path to the `spin.exe` executable (unless you
[add `spin.exe` to your PATH](https://www.howtogeek.com/118594/how-to-edit-your-system-path-for-easy-command-line-access/)).
If you want to use Spin with the GUI, you ***MUST*** add it to your PATH.

## gcc

Next, Spin needs a `gcc` compiler in order to turn your Promela code into C.
The easiest way to get this is with [MinGW](https://osdn.net/projects/mingw/releases/)
which is a project that has ported `gcc` to Windows. Just download
and run the installer, and select the base MinGW package (this includes GCC).

{{< figure src="img/mingw_install.jpg" alt="Install the base MinGW package" position="center" style="border-radius: 8px;" caption="Install the base MinGW package" captionPosition="center" >}}

You may need to [add `C:\MinGW\bin\` to your PATH](https://www.howtogeek.com/118594/how-to-edit-your-system-path-for-easy-command-line-access/) after it installs GCC.

## GUI

Now, if you'd like to use the GUI, complete the following steps.

First, you'll need to download
[`ispin.tcl`](https://github.com/nimble-code/Spin/blob/master/optional_gui/ispin.tcl)
from the `optional_gui` directory on the Spin GitHub page. The easiest way to do
this is to right-click "Raw" and then "Save link as".

{{< figure src="img/download_ispin.jpg" alt="Download the GUI file for Spin" position="center" style="border-radius: 8px;" caption="Download the GUI file for Spin" captionPosition="center" >}}

Save this wherever you like.
The next problem is getting [Tcl/Tk](https://www.tcl.tk/) installed,
which is needed to run this file.

### Git for Windows

If you have installed Git for Windows,
it likely already has Tcl/Tk installed
(or another program may have installed it).
An easy way to check is to open up Everything, and look for `wish.exe`.

{{< figure src="img/everything_wish.jpg" alt="wish.exe showing up in Everything" position="center" style="border-radius: 8px;" caption="Tcl/Tk is often included with Git for Windows" captionPosition="center" >}}

All you need to do is right-click on `ispin.tcl`, choose "Open With",
and select the `wish.exe` you found. Make sure to set
"Always use this app to open .tcl files".

{{< figure src="img/tcl_wish.jpg" alt="Selecting a default program association for .tcl files" position="center" style="border-radius: 8px;" caption="Selecting a default program association for .tcl files" captionPosition="center" >}}

With that, you should be able to launch the GUI for Spin
by double-clicking on `ispin.tcl`.

{{< figure src="img/ispin.jpg" alt="Spin GUI" position="center" style="border-radius: 8px;" caption="Spin GUI" captionPosition="center" >}}

### Tcl/Tk Distributions

Let's say you don't have Git installed. There's other ways to get Tcl/Tk.
The easiest is [ActiveTCL](https://www.activestate.com/products/tcl/downloads/) as
this will automatically setup all the proper file associations. However, they require
you to create an account to download it.

Another option is
[Magicsplat](https://www.magicsplat.com/tcl-installer/index.html#downloads),
but this does not setup the file associations, so you'll have to do it manually, like
I described above, after finding `wish.exe`.

## Conclusion

This is all you need to run Spin with the GUI on Windows! While it may
seem a bit complicated, this is likely far easier than trying to deal with Cygwin,
or setting up all the prerequisites on WSL and configuring an X11 server.
