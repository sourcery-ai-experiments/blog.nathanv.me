

## Windows

First, you need to install GPG on Windows.
The easiest way to do this is to use
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

## WSL

Now, on WSL, install the following:

```bash
sudo apt install gpg gnupg2 socat
```

Configure GPG to use the pin entry program installed in Windows and reload
the agent.

```bash
git config --global gpg.program /mnt/c/Program\ Files/Git/usr/bin/gpg.exe
echo pinentry-program /mnt/c/Program\ Files/Git/usr/bin/pinentry.exe > ~/.gnupg/gpg-agent.conf
gpg-connect-agent reloadagent /bye
```

When you commit in WSL, this will use the pin entry program installed in Windows.

## Combined

Now, configure `git` to use GPG to sign commits:

```bash
gpg --list-secret-keys --keyid-format LONG
# Get the key ID
# The line after rsa4096/<key id>
git config --global user.signingkey <key id>
git config --global commit.gpgsign true
```
