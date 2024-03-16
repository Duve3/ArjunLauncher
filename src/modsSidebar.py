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
        self.oldair = self.gref.arjun.air_friction

        self.FONT_default = ui.CUIFont(settings.POPPINS_REGULAR, 20, ui.CUColor.BLACK())
        self.FONT_bigDefault = ui.CUIFont(settings.POPPINS_REGULAR, 30, ui.CUColor.BLACK())
        self.FONT_charDefault = ui.CUIFont(settings.POPPINS_REGULAR, 50, ui.CUColor.BLACK())

        self.divider = ui.CLine((0, 0), (0, 600), color=ui.CUColor.BLACK(), width=5)

        self.LABEL_title = ui.CUILabel(self.FONT_default.get_center(self, "Modifications:").x, 20, self.FONT_default,
                                       "Modifications:")

        self.BUTTON_gravity = ui.CUITextButton(20, 50, 160, 60, ui.CUColor((35, 155, 65)), self.FONT_default,
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

        self.BUTTON_airFriction = ui.CUITextButton(20, 130, 160, 60, ui.CUColor((155, 35, 40)), self.FONT_default,
                                                   "Air Friction: OFF", draw_border_radius=5)

        def airFric_off():
            self.BUTTON_airFriction.text = "Air Friction: OFF"
            self.BUTTON_airFriction.defaultColor = ui.CUColor((155, 35, 40))
            self.oldair = self.gref.arjun.air_friction
            self.gref.arjun.air_friction = 0

            self.BUTTON_airFriction.func = airFric_on

        def airFric_on():
            self.BUTTON_airFriction.text = "Air Friction: ON"
            self.BUTTON_airFriction.defaultColor = ui.CUColor((35, 155, 65))
            self.gref.arjun.air_friction = self.oldair

            self.BUTTON_airFriction.func = airFric_off

        self.BUTTON_airFriction.func = airFric_on

        self.LABEL_force = ui.CUILabel(self.FONT_bigDefault.get_center(self, "Forces:").x, 200, self.FONT_bigDefault,
                                       "Forces:")

        def force_x_update(val):
            self.gref.starterForce[0] = int(val)

        self.INPUT_xForce = ui.CUITextInput(50, self.LABEL_force.y + 40, 130, 50, ui.CUColor.GREY(), self.FONT_default,
                                            "",
                                            allowedKeys=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                                            onTextUpdate=force_x_update)
        self.INPUT_xForce.text = self.gref.starterForce[0]
        self.LABEL_xForce = ui.CUILabel(10, self.LABEL_force.y + 48, self.FONT_charDefault, "X")

        def force_y_update(val):
            self.gref.starterForce[1] = int(val)

        self.INPUT_yForce = ui.CUITextInput(50, self.LABEL_force.y + 100, 130, 50, ui.CUColor.GREY(), self.FONT_default,
                                            "",
                                            allowedKeys=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                                            onTextUpdate=force_y_update)
        self.INPUT_yForce.text = self.gref.starterForce[1]
        self.LABEL_yForce = ui.CUILabel(10, self.LABEL_force.y + 108, self.FONT_charDefault, "Y")

        self.objects = [self.divider, self.BUTTON_gravity, self.BUTTON_airFriction, self.LABEL_title, self.LABEL_force, self.INPUT_xForce,
                        self.LABEL_xForce, self.INPUT_yForce, self.LABEL_yForce]
        self.manager = ui.CUIManager([self.BUTTON_gravity, self.INPUT_xForce, self.INPUT_yForce, self.BUTTON_airFriction], onSurface=True,
                                     pos=pos)

    def draw(self, screen: ui.CScreen):
        self.fill(ui.CUColor.GREY().lighten(20))  # basically dark gray

        for o in self.objects:
            self.camera.render(o)

        screen.draw(self, self.pos)
