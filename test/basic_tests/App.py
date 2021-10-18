# -*- coding: utf-8 -*-
from brue.core import Component
from brue.ui.layouts import ColumnLayout, RowLayout
from brue.ui.widgets import Label
from brue.router import RouterLink, RouterView


class App(Component):
    css = """
    """
    state = {
        "test": 1
    }

    def render(self):
        with ColumnLayout():
            with RowLayout(style = { "borderBottom": "1px solid black" }):
                RouterLink("Welcome", to = { "url": "/", "props": {"name": "Lee Seung Hwan"}, "name": "route1" })
                Label("|")
                RouterLink("Counter", to = "/Counter", name = "route1")
                Label("|")
                RouterLink("Widgets", to = "/Widgets", name = "route1")

            RouterView(name = "route1")
