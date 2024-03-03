import pygame
from lib import menu
from lib import ui
from lib import config
from game import Game
from __about__ import __VERSION__


class MainMenu(menu.MenuType):
    def __init__(self, screen: ui.CScreen, settings: config.Settings):
        super().__init__(screen)
        self.settings = settings

        self.transitionEvent = pygame.event.Event(pygame.USEREVENT + 1)
        self.transitionType = pygame.USEREVENT + 1

        self.FONT_title = ui.CUIFont(settings.PROTEST_RIOT, 60, ui.CUColor.WHITE())
        self.LABEL_title = ui.CUILabel(self.FONT_title.get_center(self.screen.surface, "Arjun Launcher").x, 100, self.FONT_title, "Arjun Launcher")

        self.FONT_version = ui.CUIFont(settings.POPPINS_REGULAR, 20, ui.CUColor.WHITE())
        self.LABEL_version = ui.CUILabel(10, 570, self.FONT_version, __VERSION__)

        self.FONT_play = ui.CUIFont(settings.POPPINS_REGULAR, 30, ui.CUColor.WHITE())
        self.BUTTON_play = ui.CUITextButton(400 - 100, 300, 200, 50, ui.CUColor.WHITE().darken(50, retColor=True), self.FONT_play, "PLAY", draw_border_radius=5, onPress=lambda: pygame.event.post(self.transitionEvent))

        self.manager = ui.CUIManager(objects=[self.BUTTON_play])

        # fade stuff:
        self.darkSurface = pygame.Surface((800, 600), pygame.SRCALPHA)
        self.darkSurface.fill(ui.CUColor.BLACK())

        self.transition = 0

        self.run()  # this unfortunately cannot be done in the super call, as it will result in 0 variables being set.

    def run(self):
        while True:
            self.screen.tick()
            events = pygame.event.get()
            self.manager.tick(events)
            for event in events:
                if event.type == pygame.QUIT:
                    ui.CScreen.close(kill=True)

                elif event.type == self.transitionType:
                    self.transition = 1

            if self.transition > 0:
                self.transition += 9

            if self.transition > 255:
                Game(self.screen, self.settings)

            self.darkSurface.set_alpha(self.transition)

            self.screen.fill(ui.CUColor.BLUE().darken(50, retColor=True))

            self.screen.draw(self.LABEL_title)
            self.screen.draw(self.LABEL_version)
            self.screen.draw(self.BUTTON_play)

            self.screen.draw(self.darkSurface, (0, 0))

            pygame.display.flip()
