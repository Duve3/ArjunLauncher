import subprocess
import os
from src.__about__ import __VERSION__
import urllib.request
import zipfile
import shutil

try:
    import requests
except ImportError:
    print("Installing Requests (required module)")
    subprocess.run(["python", "-m", "pip", "install", "requests"])
    import requests


def checkForUpdate():
    base = "https://nzzd5r-5000.csb.app/"
    print("Checking for update")

    newest = requests.get(f"{base}current_version")
    if newest.text != __VERSION__:
        print("Updating to new version.")
        if not os.path.isdir("./temp/"):
            os.mkdir("./temp/")
        new_url = requests.get(f"{base}new")
        urllib.request.urlretrieve(new_url.text, "./temp/source.zip")
        with zipfile.ZipFile("./temp/source.zip", "r") as zf:
            zf.extractall("./temp/")  # WARN: this could result in dangerous files if untrusted source

        if os.path.exists("./temp/ArjunLauncher-master/update.py"):
            print("Renaming self to old_update.py")
            if os.path.exists("./old_update.py"):
                os.remove("./old_update.py")
                os.rename("./update.py", "./old_update.py")

            print("Moving new update.py to ./update.py")
            shutil.move("./temp/ArjunLauncher-master/update.py", "./update.py")

        shutil.copytree("./temp/ArjunLauncher-master/", "./")

        print("You now have to rerun the build script.")
        input("Press enter to quit.")


if __name__ == "__main__":
    print("THIS IS NOT THE BUILD SCRIPT, simply used for testing updating")
    checkForUpdate()
