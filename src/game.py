import pygame
from lib import ui
from lib import menu
from lib import config


def build_arjun() -> ui.CUIGroup:
    group = ui.CUIGroup((75, 200))

    group.add_obj(ui.CCircle((10, 10), 20, ui.CUColor.BLACK(), draw_width=10))

    group.add_obj(ui.CLine((10, 29), (10, 101), ui.CUColor.BLACK(), width=10))

    return group


class Arjun(pygame.Surface):
    def __init__(self, air_friction, gravity):
        super().__init__((75, 200))

        self.arjun = build_arjun()

        self.force = [0, 0]

        self.gravity = gravity
        self.air_friction = air_friction

    def tick(self, dt, camera: ui.CGCamera):
        dt /= 1000  # because its in milliseconds
        camera.x += self.force[0] * dt
        camera.y -= self.force[1] * dt

        print(self.force)

        # self.move(self.force[0] * dt, self.force[1] * dt)
        print(self.air_friction)
        print(self.gravity)
        print(dt)
        self.force[0] -= (self.air_friction * dt)
        self.force[1] -= (self.gravity * dt)

        if self.force[0] <= 0:
            self.force[0] = 0

        # by commenting the following, it allows the character to start going downwards
        # TODO: make sure to check somewhere else that the character isn't going below ground!
        # if self.force[1] <= 0:
        #     self.force[1] = 0

    def move(self, x, y):
        self.arjun.move(x, y)

    def set_pos(self, x, y):
        self.arjun.set_pos(x, y)


class ModsSidebar(pygame.Surface):
    def __init__(self):
        super().__init__((200, 600), flags=pygame.SRCALPHA)

        self.show = True

        self.fill(ui.CUColor.GREY().darken(20))  # basically dark gray

        line = ui.CLine((0, 0), (0, 600), color=ui.CUColor.BLACK(), width=5)

        line.draw(self)

        self.manager = ui.CUIManager([])


class Game(menu.MenuType):
    def __init__(self, screen: ui.CScreen, settings: config.Settings):
        super().__init__(screen)
        # because of how this entire thing will work, all objects will be positioned globally, and inputted
        # through a camera that handles where to actually put the objects on the screen based on the current coords.
        self.settings = settings

        self.camera = ui.CGCamera(self.screen)

        self.background = pygame.transform.smoothscale(pygame.image.load(settings.BACKGROUND).convert_alpha(), (800, 600))

        self.starterPosition = [200, 220]

        self.arjun = Arjun(30, 9.8)  # TODO: find a real air resistance value (and more accurate gravity).
        self.arjun.set_pos(*self.starterPosition)

        self.SIDEBAR_mods = ModsSidebar()

        self.FONT_launch = ui.Font(self.settings.POPPINS_REGULAR, 20, ui.CUColor.BLACK())

        self.BUTTON_launch = ui.CUITextButton(490, 10, 100, 50, ui.CUColor.GREEN(), self.FONT_launch, "LAUNCH",
                                              draw_border_radius=5)

        def stop():
            self.SIDEBAR_mods.show = True
            self.arjun.set_pos(*self.starterPosition)
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
            self.BUTTON_launch.x, self.BUTTON_launch.y = 590, 10
            self.BUTTON_launch.text_pos = (
                self.BUTTON_launch.centerx - self.BUTTON_launch.font.get_rect(self.BUTTON_launch.text,
                                                                              size=self.BUTTON_launch.font.size).width // 2,
                self.BUTTON_launch.centery - self.BUTTON_launch.font.get_rect(self.BUTTON_launch.text,
                                                                              size=self.BUTTON_launch.font.size).height // 2)

            self.BUTTON_launch.func = stop

            self.arjun.force = [200, 30]

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

            # if pygame.key.get_pressed()[pygame.K_w]:
            #     self.camera.y -= 10
            #
            # if pygame.key.get_pressed()[pygame.K_s]:
            #     self.camera.y += 10
            #
            # if pygame.key.get_pressed()[pygame.K_a]:
            #     self.camera.x -= 10
            #
            # if pygame.key.get_pressed()[pygame.K_d]:
            #     self.camera.x += 10

            self.screen.fill(ui.CUColor.CYAN())
            self.camera.render(self.background, (0, 0))

            if transition > 0:
                transition -= 9

                fader.set_alpha(transition)
                self.screen.draw(fader, (0, 0))

            if self.SIDEBAR_mods.show:
                self.screen.draw(self.SIDEBAR_mods, (600, 0))
            else:
                self.arjun.tick(dt, self.camera)

            # always drawn as it is the stop button
            self.screen.draw(self.BUTTON_launch)

            self.screen.draw(self.arjun.arjun)

            pygame.display.flip()
