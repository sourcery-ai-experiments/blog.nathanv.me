import os
import shutil
import subprocess
import sys


def main():
    os.chdir("public")
    subprocess.call(["git", "submodule", "update"])
    subprocess.call(["git", "reset", "--hard", "master"])
    os.chdir("..")
    shutil.rmtree("public")
    subprocess.call(["hugo"])

    with open("public/CNAME", "w") as f:
        f.write("blog.nathanv.me")


if __name__ == "__main__":
    main()
