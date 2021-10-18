# -*- coding: utf-8 -*-
from brue.core import Component
from views.Welcome import Welcome


class App(Component):
    def render(self):
        Welcome()
