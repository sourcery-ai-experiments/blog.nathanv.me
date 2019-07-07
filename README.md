# blog.nathanv.me-hugo

## Cloning

```
git clone https://github.com/NathanVaughn/blog.nathanv.me-hugo.git
git submodule init
git submodule update
```

## Python scripts

### build.py

Cleans old version and builds site

```bash
python .\build.py
```

### deploy.py

Adds all changes and commits to both Hugo repo and site repo with the first argument
as the commit message.

```bash
python .\deploy.py "New post"
```