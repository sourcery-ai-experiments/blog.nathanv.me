import glob
import os
import shutil
import subprocess
import sys
import time


def main():
    os.chdir("public")
    subprocess.call(["git", "submodule", "update"])
    time.sleep(1)
    subprocess.call(["git", "reset", "--hard", "master"])
    time.sleep(1)
    os.chdir("..")
    delete_folder_contents("public")
    time.sleep(1)
    subprocess.call(["hugo"])

def delete_folder_contents(folder):
    pattern = folder + '/*'
    r = glob.glob(pattern)
    for i in r:
        if os.path.isfile(i):
            os.remove(i)
        elif os.path.isdir(i):
            shutil.rmtree(i)

if __name__ == "__main__":
    main()
