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

While you *can* do this with WSL, Spin has prebuilt Windows
binaries available, so I think this is easier than trying to get
X11 working ([as of Sept 2020](https://devblogs.microsoft.com/commandline/whats-new-in-the-windows-subsystem-for-linux-september-2020/#gui-apps)).

## Prerequisites

You'll need the following software installed:

- [7zip](https://www.7-zip.org/)

The following will make life easier:

- [Git for Windows](https://git-scm.com/download/win)
- [Everything](https://www.voidtools.com/)

If you're using [Chocolately](https://chocolatey.org/),
this can all be installed with:

```powershell
choco install 7zip git everything
```

## Downloading/Extracting Spin

First, go to the Spin [GitHub page](https://github.com/nimble-code/Spin). If you
already have Git installed, you can just clone this. Or, if you'd like,
you can go to [`Bin`](https://github.com/nimble-code/Spin/tree/master/Bin) directory,
and click on the latest version of
`spin<ver>_windows64.exe.gz`. Click "Download" on the right side to get
only this file.

{{< figure src="img/download_spin.jpg" alt="Download the latest prebuilt version of Spin" position="center" style="border-radius: 8px;" caption="Download the latest prebuilt version of Spin" captionPosition="center" >}}

Once that's downloaded, use [7zip](https://www.7-zip.org/) to extract the archive.

{{< figure src="img/extract_spin.jpg" alt="Extract the archive with 7zip" position="center" style="border-radius: 8px;" caption="Extract the archive with 7zip" captionPosition="center" >}}

Inside the directory it extracted into will be an executable. Rename this to `spin.exe`.

## GCC

Next, Spin needs the GCC compiler in order to compile the generated C verifier.
The easiest way to get this is with [MinGW](http://www.mingw.org/)
which is a project that has ported GCC to Windows.
Download and run [the installer](https://osdn.net/projects/mingw/releases/),
and select the base MinGW package (this includes GCC).

{{< figure src="img/mingw_install.jpg" alt="Install the base MinGW package" position="center" style="border-radius: 8px;" caption="Install the base MinGW package" captionPosition="center" >}}

You may need to [add `C:\MinGW\bin\` to your PATH](https://www.howtogeek.com/118594/how-to-edit-your-system-path-for-easy-command-line-access/) after it installs GCC.
You can verify it is setup correctly by running `gcc` in a shell and making sure
you don't get a "gcc not found" error.

If you're using [Chocolately](https://chocolatey.org/),
this can alternatively be installed with:

```powershell
choco install mingw
```

This will setup your PATH for you.

Now, if you only want the command-line version of Spin, you're basically done.
You'll need to use the full path to the `spin.exe` executable (unless you
[add `spin.exe` to your PATH](https://www.howtogeek.com/118594/how-to-edit-your-system-path-for-easy-command-line-access/)).

## GUI

Now, if you'd like to use the GUI, complete the following steps. Buckle up.

First, you'll need to download
[`ispin.tcl`](https://github.com/nimble-code/Spin/blob/master/optional_gui/ispin.tcl)
from the `optional_gui` directory on the Spin GitHub page. The easiest way to do
this is to right-click "Raw" and then "Save link as".

{{< figure src="img/download_ispin.jpg" alt="Download the GUI file for Spin" position="center" style="border-radius: 8px;" caption="Download the GUI file for Spin" captionPosition="center" >}}

Save this wherever you like.

Now, the GUI needs to know where `spin.exe` is. There are two options.

1. [Add `spin.exe` to your PATH](https://www.howtogeek.com/118594/how-to-edit-your-system-path-for-easy-command-line-access/). **Recommended**
2. Edit `ispin.tcl` on line 19 to replace
   ```bash
   set SPIN    spin   ;# essential
   ```
   with something like
   ```bash
   set SPIN	"C:/Program\ Files\ \(x86\)/spin650_windows64/bin/spin";# essential
   ```
   to point where ever you put `spin.exe`. Make sure properly escape the Windows path characters.

The next problem is getting [Tcl/Tk](https://www.tcl.tk/) installed,
which is needed to run this file.

### Git for Windows

If you have installed Git for Windows, it likely already has already installed Tcl/Tk 
(or another program may have installed it).
An easy way to check is to open up [Everything](https://www.voidtools.com/),
and look for `wish.exe`.

{{< figure src="img/everything_wish.jpg" alt="wish.exe showing up in Everything" position="center" style="border-radius: 8px;" caption="Tcl/Tk is often included with Git for Windows" captionPosition="center" >}}

All you need to do is right-click on `ispin.tcl`, choose "Open With",
and select the `wish.exe` you found. Make sure to set
"Always use this app to open .tcl files".

{{< figure src="img/tcl_wish.jpg" alt="Selecting a default program association for .tcl files" position="center" style="border-radius: 8px;" caption="Selecting a default program association for .tcl files" captionPosition="center" >}}

With that, you should be able to launch the GUI for Spin
by double-clicking on `ispin.tcl`.

{{< figure src="img/ispin.jpg" alt="Spin GUI" position="center" style="border-radius: 8px;" caption="Spin GUI" captionPosition="center" >}}

### Tcl/Tk Distributions

Let's say you don't have Git installed. There are other ways to get Tcl/Tk.
The easiest is [ActiveTCL](https://www.activestate.com/products/tcl/downloads/) as
this will automatically setup all the proper file associations. However, they require
you to create an account to download it.

Another option is
[Magicsplat](https://www.magicsplat.com/tcl-installer/index.html#downloads),
but this does not setup the file associations, so you'll have to do it manually, like
I described above, after finding `wish.exe`.

### Graphviz

This last part is optional. If you want the automata view to work, you'll need
to install [Graphviz](https://graphviz.org/). Go to the
[downloads](https://graphviz.org/download/) page and get the
[latest .zip file](https://www2.graphviz.org/Packages/stable/windows/10/msbuild/Release/Win32/).

Extract this and put it somewhere useful like `C:\Program Files (x86)\`.
You can add the `bin` directory to your PATH if you like.

If you're using [Chocolately](https://chocolatey.org/),
this can alternatively be installed with:

```powershell
choco install graphviz
```

Lastly, you'll need to edit `ispin.tcl` again. Comment out line 21, and uncomment
line 22, and adjust the path to `dot` as needed. For example:

```bash
#	set DOT     dot    ;# recommended, for automata view
	set DOT		"C:/Program\ Files\ \(x86\)/graphviz-2.44.1-win32/Graphviz/bin/dot";
```

*(Even if `dot.exe` is added to your PATH, I've found it will still not work without doing this)*

You should be all set now.

{{< figure src="img/automata_view.jpg" alt="Spin GUI automata view" position="center" style="border-radius: 8px;" caption="Spin GUI automata view" captionPosition="center" >}}

## Conclusion

This is all you need to run Spin with the GUI on Windows! While it may
seem a bit complicated, you should really only have to do this once.

I really do recommend using [Chocolately](https://chocolatey.org/) to make
installing everything easier. Installing the vast majority of the dependencies
becomes one command:

```powershell
choco install 7zip git everything mingw graphviz
```

If this seems like a lot of work, I've found another Spin GUI
available: [jspin](https://github.com/motib/jspin).
This has its own installation challenges (needing a Java runtime and requiring
some PATH configuration in its `config.cfg` file), but it seems
to work similarly and be far easier to get setup.