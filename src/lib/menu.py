"""
menu.py
Rewrites MenuType from pygame_wrapper to be better and more effective.
(I wrote pygame_wrapper long ago and don't feel like updating it, so I'll just rewrite it in my code)
"""
from .ui import CScreen  # noqa:RELATIVE ; it worked so it doesnt matter


class MenuType:
    def __init__(self, screen: CScreen):  # noqa:super ; its
        self.screen = screen

    def run(self):
        pass
