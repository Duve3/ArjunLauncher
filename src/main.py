"""
main.py
Contains all the main files.
"""
from lib import ui, config
from mainMenu import MainMenu


def main():
    ui.init()  # inits most things
    screen = ui.CScreen(caption="Arjun Launcher", scrap=False, clock=True)
    settings = config.Settings()

    # WARN: following uses constants for file name, may result in errors later.
    settings.NUNITO_SANS = settings.ASSET_DIR + "NunitoSans.ttf"  # Won't be put into settings, but still transferred.
    settings.PROTEST_RIOT = settings.ASSET_DIR + "ProtestRiot.ttf"
    settings.POPPINS_REGULAR = settings.ASSET_DIR + "Poppins_R.ttf"
    settings.BACKGROUND = settings.ASSET_DIR + "background.jpg"

    MainMenu(screen, settings)


if __name__ == "__main__":
    main()
