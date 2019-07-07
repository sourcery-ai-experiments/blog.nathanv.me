import os
import subprocess
import sys


def main():
    os.chdir("public")
    subprocess.call(["git", "checkout", "master"])
    subprocess.call(["git", "add", "."])
    subprocess.call(["git", "commit", "-m", sys.argv[1]])
    subprocess.call(["git", "push", "-f", "origin", "master"])

    os.chdir("..")
    subprocess.call(["git", "add", "."])
    subprocess.call(["git", "commit", "-m", sys.argv[1]])
    subprocess.call(["git", "push", "-f", "origin", "master"])

if __name__ == "__main__":
    main()
