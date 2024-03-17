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
    base = "https://nzzd5r-5000.csb.app/"  # doesn't really work until I can get a real API
    print("Checking for update")

    newest = requests.get(f"{base}current_version")
    if newest.status_code != 200:  # we can't risk bugging out because API offline
        print("Failure to connect to API! Assuming Server is offline!")
        return

    if newest.text != __VERSION__:
        print("Updating to new version.")
        if not os.path.isdir("./temp/"):
            os.mkdir("./temp/")
        new_url = requests.get(f"{base}new")
        urllib.request.urlretrieve(new_url.text, "./temp/source.zip")
        with zipfile.ZipFile("./temp/source.zip", "r") as zf:
            zf.extractall("./temp/")  # WARN: this could result in dangerous files if untrusted source

        if os.path.exists("./temp/ArjunLauncher-master/update.py"):
            print("Renaming self to update.py")
            if os.path.exists("./old_update.py"):
                os.remove("./old_update.py")

            os.rename("./update.py", "./old_update.py")

            print("Moving new update.py to ./update.py")
            shutil.move("./temp/ArjunLauncher-master/update.py", "./update.py")

        print("Copying new version over.")
        shutil.copytree("./temp/ArjunLauncher-master/src", "./src", copy_function=shutil.copyfile, dirs_exist_ok=True)

        print("You now have to rerun the build script.")
        input("")


if __name__ == "__main__":
    print("THIS IS NOT THE BUILD SCRIPT, simply used for testing updating")
    checkForUpdate()
