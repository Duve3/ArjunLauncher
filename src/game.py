import pygame
from lib import ui
from lib import menu
from lib import config
import math


def build_arjun() -> ui.CUIGroup:
    group = ui.CUIGroup((75, 200))

    group.add_obj(ui.CCircle((20, 20), 20, ui.CUColor.BLACK(), draw_width=10))

    group.add_obj(ui.CLine((20, 39), (20, 111), ui.CUColor.BLACK(), width=10))

    return group


class Arjun(pygame.Surface):
    def __init__(self, air_friction, gravity, ground_friction):
        super().__init__((75, 200))

        # Arjun
        self.arjun = build_arjun()

        self.force = [0, 0]

        self.draw_degree = 0

        self.gravity = gravity
        self.air_friction = air_friction

        self.hit_ground = False
        self.ground_friction = ground_friction

    def tick(self, dt, camera: ui.CGCamera):
        dt /= 1000  # because its in milliseconds
        camera.x += self.force[0] * dt
        camera.y -= self.force[1] * dt

        print(self.force)
        print(self.air_friction)
        print(self.gravity)
        print(dt)

        # angle calculations
        try:
            self.draw_degree = -(math.degrees(math.atan(self.arjun.pos[1] + self.force[1]/self.arjun.pos[0] - self.force[0])) * 1000) % 360
            # if self.draw_degree > 350 or self.draw_degree < 120:
            #     self.draw_degree = 350
            #
            # elif 180 > self.draw_degree > 120:
            #     self.draw_degree = 180
            # TODO:
            #   (above) still incorrect somehow, rotates in a circle fashion, set max/min?
        except ZeroDivisionError:
            self.draw_degree = 0

        # force calculations
        self.force[0] -= self.air_friction * dt  # * (self.force[0]/1000) - makes air friction based on velo \n
        # The above doesn't use air friction based on velo (currently) due to it being either too high or too low
        # TODO:
        #  Make force[0] -= self.air_friction * dt and * (self.force[0]/1000) <= the 1000 needs to be tuned to good
        if not self.hit_ground:
            self.force[1] -= self.gravity * dt
        else:
            if self.force[1] != 0:
                self.force[1] = 0
            self.force[0] -= self.ground_friction * dt * (self.force[0] / 100)  # makes ground friction based on velo

        if self.force[0] <= 0:
            self.force[0] = 0

        # by commenting the following, it allows the character to start going downwards
        # notTODO: make sure to check somewhere else that the character isn't going below ground!
        # if self.force[1] <= 0:
        #     self.force[1] = 0

    def move(self, x, y):
        self.arjun.pos[0] += x
        self.arjun.pos[1] += y

    def set_pos(self, x, y):
        self.arjun.pos[0] = x
        self.arjun.pos[1] = y


class ModsSidebar(pygame.Surface):
    def __init__(self):
        super().__init__((200, 600), flags=pygame.SRCALPHA)

        self.show = True

        self.fill(ui.CUColor.GREY().darken(20))  # basically dark gray

        self.divider = ui.CLine((0, 0), (0, 600), color=ui.CUColor.BLACK(), width=5)

        self.manager = ui.CUIManager([])

    def draw(self, screen: ui.CScreen):
        pass


class Game(menu.MenuType):
    def __init__(self, screen: ui.CScreen, settings: config.Settings):
        super().__init__(screen)
        # because of how this entire thing will work, all objects will be positioned globally, and inputted
        # through a camera that handles where to actually put the objects on the screen based on the current coords.
        self.settings = settings

        self.aboveSurface = pygame.Surface((1000, 600))
        self.aboveSurface.fill(ui.CUColor((25, 200, 254)))

        self.belowSurface = pygame.Surface((1000, 600))
        self.belowSurface.fill(ui.CUColor((30, 72, 86)))

        self.camera = ui.CGCamera(self.screen)

        self.FONT_coords = ui.CUIFont(settings.POPPINS_REGULAR, 20, ui.CUColor.BLACK())
        self.LABEL_coords = ui.CUILabel(660, 60, self.FONT_coords,
                                        "Coordinates:\nx: {0}\ny: {1}".format(self.camera.x, self.camera.y))

        self.background = pygame.transform.smoothscale(pygame.image.load(settings.BACKGROUND).convert_alpha(),
                                                       (800, 600))

        self.starterPosition = [100, 365]
        self.starterForce = [200, 20]

        self.arjun = Arjun(30, 9.8, 60)  # TODO: find a real air resistance value (and more accurate gravity).
        self.arjun.set_pos(*self.starterPosition)

        self.SIDEBAR_mods = ModsSidebar()

        self.FONT_launch = ui.CUIFont(self.settings.POPPINS_REGULAR, 20, ui.CUColor.BLACK())

        self.BUTTON_launch = ui.CUITextButton(490, 10, 100, 50, ui.CUColor.GREEN(), self.FONT_launch, "LAUNCH",
                                              draw_border_radius=5)

        # debug (never actually used unless enabled, probably will be removed in prod-based builds)
        self.LABEL_angle = ui.CUILabel(100, 10, self.FONT_coords, "angle: \n{0}".format(self.arjun.draw_degree))
        self.LABEL_force = ui.CUILabel(100, 200, self.FONT_coords, "force: \n{0}".format(self.arjun.force))

        def stop():
            self.SIDEBAR_mods.show = True
            self.arjun.set_pos(*self.starterPosition)
            self.arjun.draw_degree = 0
            self.camera.x, self.camera.y = 0, 0
            self.BUTTON_launch.defaultColor = ui.CUColor.GREEN()
            self.BUTTON_launch.pressedColor = ui.CUColor.GREEN().darken(20, retColor=True)
            self.BUTTON_launch.highlightColor = ui.CUColor.GREEN().darken(40, retColor=True)
            self.BUTTON_launch.text = "LAUNCH"
            self.BUTTON_launch.x, self.BUTTON_launch.y = 490, 10
            self.BUTTON_launch.text_pos = (
                self.BUTTON_launch.centerx - self.BUTTON_launch.font.get_rect(self.BUTTON_launch.text,
                                                                              size=self.BUTTON_launch.font.size).width // 2,
                self.BUTTON_launch.centery - self.BUTTON_launch.font.get_rect(self.BUTTON_launch.text,
                                                                              size=self.BUTTON_launch.font.size).height // 2)

            self.BUTTON_launch.func = launch

        def launch():
            self.SIDEBAR_mods.show = False
            self.BUTTON_launch.defaultColor = ui.CUColor.RED()
            self.BUTTON_launch.pressedColor = ui.CUColor.RED().darken(20, retColor=True)
            self.BUTTON_launch.highlightColor = ui.CUColor.RED().darken(40, retColor=True)
            self.BUTTON_launch.text = "STOP"
            self.BUTTON_launch.x, self.BUTTON_launch.y = 690, 10
            self.BUTTON_launch.text_pos = (
                self.BUTTON_launch.centerx - self.BUTTON_launch.font.get_rect(self.BUTTON_launch.text,
                                                                              size=self.BUTTON_launch.font.size).width // 2,
                self.BUTTON_launch.centery - self.BUTTON_launch.font.get_rect(self.BUTTON_launch.text,
                                                                              size=self.BUTTON_launch.font.size).height // 2)

            self.BUTTON_launch.func = stop

            self.arjun.force = self.starterForce
            self.arjun.hit_ground = False

        self.BUTTON_launch.func = launch

        self.manager = ui.CUIManager([self.BUTTON_launch])

        self.run()

    def run(self):
        fader = pygame.Surface((800, 600), flags=pygame.SRCALPHA)
        fader.fill(ui.CUColor.BLACK())

        transition = 255

        while True:
            dt = self.screen.tick()
            events = pygame.event.get()
            self.manager.tick(events)
            for event in events:
                if event.type == pygame.QUIT:
                    self.screen.close(kill=True)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        self.settings.DEBUG = not self.settings.DEBUG
                        self.settings.write()

            if self.camera.y >= 50:
                self.arjun.hit_ground = True

            self.screen.draw(self.aboveSurface, (-100, 0))
            if self.camera.y > 0:
                self.screen.draw(self.belowSurface, (-100, 500))

            # background stuff
            x = (self.camera.x // 800) * 800
            self.camera.render(self.background, (0 + x, 0))
            self.camera.render(self.background, (800 + x, 0))
            self.camera.render(self.background, (1600 + x, 0))

            if transition > 0:
                transition -= 9

                fader.set_alpha(transition)
                self.screen.draw(fader, (0, 0))

            if self.SIDEBAR_mods.show:
                self.screen.draw(self.SIDEBAR_mods, (600, 0))
            else:
                self.arjun.tick(dt, self.camera)

                # coordinates
                self.LABEL_coords.text = "Coordinates:\n   x: {0}\n   y: {1}".format(round(self.camera.x),
                                                                                     round(-self.camera.y))
                self.screen.draw(self.LABEL_coords)

                if self.settings.DEBUG:
                    self.LABEL_angle.text = "angle: \n{0}".format(self.arjun.draw_degree)
                    self.LABEL_force.text = "force: \n{0}".format(self.arjun.force)

                    self.screen.draw(self.LABEL_angle)
                    self.screen.draw(self.LABEL_force)

            # always drawn as it is the stop button
            self.screen.draw(self.BUTTON_launch)

            self.arjun.arjun.rotate(self.arjun.draw_degree)
            self.arjun.arjun.draw(self.screen)

            pygame.display.flip()
