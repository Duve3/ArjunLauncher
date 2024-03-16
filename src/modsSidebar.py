import pygame
from lib import ui, config


class ModsSidebar(pygame.Surface):
    def __init__(self, settings: config.Settings, pos, gref):
        super().__init__((200, 600), flags=pygame.SRCALPHA)

        self.gref = gref
        self.pos = pos

        self.camera = ui.CGCamera(self)

        self.show = True

        self.oldgrav = 0

        self.FONT_default = ui.CUIFont(settings.POPPINS_REGULAR, 20, ui.CUColor.BLACK())
        self.FONT_bigDefault = ui.CUIFont(settings.POPPINS_REGULAR, 30, ui.CUColor.BLACK())

        self.divider = ui.CLine((0, 0), (0, 600), color=ui.CUColor.BLACK(), width=5)

        self.LABEL_title = ui.CUILabel(self.FONT_default.get_center(self, "Modifications:").x, 20, self.FONT_default, "Modifications:")

        self.BUTTON_gravity = ui.CUITextButton(20, 60, 160, 50, ui.CUColor((35, 155, 65)), self.FONT_default,
                                               "Gravity: ON", draw_border_radius=5)

        def grav_off():
            self.BUTTON_gravity.text = "Gravity: OFF"
            self.BUTTON_gravity.defaultColor = ui.CUColor((155, 35, 40))
            self.oldgrav = self.gref.arjun.gravity
            self.gref.arjun.gravity = 0

            self.BUTTON_gravity.func = grav_on

        def grav_on():
            self.BUTTON_gravity.text = "Gravity: ON"
            self.BUTTON_gravity.defaultColor = ui.CUColor((35, 155, 65))
            self.gref.arjun.gravity = self.oldgrav

            self.BUTTON_gravity.func = grav_off

        self.BUTTON_gravity.func = grav_off

        self.LABEL_force = ui.CUILabel(self.FONT_bigDefault.get_center(self, "Forces:").x, 130, self.FONT_bigDefault, "Forces:")

        self.objects = [self.divider, self.BUTTON_gravity, self.LABEL_title, self.LABEL_force]
        self.manager = ui.CUIManager([self.BUTTON_gravity], onSurface=True, pos=pos)

    def draw(self, screen: ui.CScreen):
        self.fill(ui.CUColor.GREY().lighten(20))  # basically dark gray

        for o in self.objects:
            o.draw(self)

        screen.draw(self, self.pos)
