"""
build.py
Builds the Project, using pyinstaller
Requires python 3.11 or higher, requires python to also be on path.
"""
import subprocess
import os
import shutil


def main():
    print("This script will build Arjun Launcher from source. If you have any issues please report them!")
    print("Building...")

    # while I could check, its very difficult because of environments
    print("Installing pyinstaller via python -m pip")
    subprocess.run(["python", "-m", "pip", "install", "pyinstaller", "--upgrade"])

    print("Executing pyinstaller build")
    subprocess.run(["pyinstaller", "./src/main.py", "--onefile"])  # before? ("python", "-m",)

    print("Building complete directory")
    if not os.path.isdir("./output/"):
        os.mkdir("./output/")

    with open("./output/settings.json", "w") as sf:
        sf.write('{\n"ASSET_DIR":"./assets/"\n}')  # hopefully works?
        sf.truncate()

    print("Moving from ./dist/main.exe to ./output/main.exe")
    shutil.move("./dist/main.exe", "./output/main.exe")

    print("Creating assets directory (and checking)")
    if not os.path.isdir("./output/assets/"):
        os.mkdir("./output/assets/")

    print("Moving assets")
    filenames = next(os.walk("./assets/"), (None, None, []))[2]

    for file in filenames:
        print(f"Moving {file}")
        shutil.copy(f"./assets/{file}", f"./output/assets/{file}")

    print("Build complete!")
    print("Run main.py in the output directory (should be in the same one as this one!")


if __name__ == "__main__":
    main()
