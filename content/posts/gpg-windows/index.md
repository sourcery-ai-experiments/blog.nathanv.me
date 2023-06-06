---
author: Nathan Vaughn
date: "2023-06-06"
description: Signing commits on Windows with GPG in Windows, WSL, and Dev Containers
tags:
  - Git
  - GPG
title: GPG Commit Signing on Windows
---

## Background

I like to sign my git commits with my GPG key, as it adds some extra verification that
it truly is me writing code. Git takes the `user.name` and `user.email` field at
face-value, and I've definitely had instances where the origin of a commit was unclear
due to misconfiguration. By signing commits, it is without a doubt me that created
that commit. Also I get a nice "Verified" icon in GitHub.

{{< figure src="img/2023-06-06-18-06-02.png" caption="[https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits)" captionPosition="center" >}}

I really struggled to get GPG signing set up on Windows with some of my workflows.
While Windows itself wasn't too hard, getting WSL to work took some struggling,
and then using [Dev Containers](https://containers.dev/)
(one of my favorite tools lately) was even more pain with minimal documentation
available.

Below is what I have figured out and have working for myself.

## Windows

First, you need to install GPG on Windows. The easiest way to do this is to use
[winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/)
and install git:

```powershell
winget install git.git
```

The GPG program will be available at `"C:\Program Files\Git\usr\bin\gpg.exe"`.
Tell `git` this with:

```powershell
git config --global gpg.program "C:\Program Files\Git\usr\bin\gpg.exe"
```

Finally, either generate or load existing keys.

Generate a key:

```powershell
& "C:\Program Files\Git\usr\bin\gpg.exe" --full-generate-key
> RSA and DSA
> 4096
> Don't Expire
> Name
> Email
> No comment
```

Load a key:

```powershell
& "C:\Program Files\Git\usr\bin\gpg.exe" --import "path\to\key\key.privkey"
```

## WSL

In order to get Dev Containers to work, GPG will
also need to be installed in WSL, as the keys loaded in WSL
get copied into Dev Containers. Install the following:

```bash
sudo apt install gpg gnupg2 socat
```

Configure GPG to use the pin entry program installed in Windows and reload
the agent.

```bash
echo pinentry-program /mnt/c/Program\ Files/Git/usr/bin/pinentry.exe > ~/.gnupg/gpg-agent.conf
gpg-connect-agent reloadagent /bye
```

When you commit in WSL, this will use the pin entry program installed in Windows.
Otherwise I've found it will not work with Dev Containers.

Now, load the same key you loaded in Windows:

```bash
gpg --import "/mnt/c/Users/path/to/key.privkey"
```

## Windows/WSL

For both Windows and WSL, configure `git` to use your GPG key to sign commits:

```bash
gpg --list-secret-keys
# Get the key ID
git config --global user.signingkey <key id>
git config --global commit.gpgsign true
```

## Dev Container

Lastly, to be able to sign commits in a Dev Container, you'll need to install GPG
in the container, and override your git config to point at that installation.

For `apt`-based images:

```bash
apt update && apt install gnupg2 -y && git config gpg.program gpg2
```

For `apk`-based images:

```bash
apk add gnupg && git config gpg.program gpg
```

As your keyring and git config from WSL get copied in to the container,
this should work automatically.

Do be warned that this changes the git config for the current repo. If this is
a repo that you open both in a Dev Container and Windows/WSL, this will cause havoc.
I highly recommend using the "Clone in Volume" option when creating the Dev Container
to avoid this.

{{< figure src="img/2023-06-06-18-12-50.png" captionPosition="center" >}}

## Conclusion

With all of this set up, you should now be able to sign your commits while developing
on Windows no matter if you're using Windows directly, WSL, or a Dev Container.

{{< figure src="img/2023-06-06-17-57-28.png" alt="GPG passphrase entry dialog" captionPosition="center" >}}
