# -*- coding: utf-8 -*-
from brue.core import Component
from brue.ui.layouts import ColumnLayout
from brue.ui.widgets import Image, Label


@Component.register("view-welcome")
class Welcome(Component):
    css = """
    .root {
        align-items: center;
    }

    .splash {
        width: 300px;
        height: 300px;
    }

    .title {
        font-size: 50px;
    }

    .subtitle {
        font-size: 20px;
    }
    """
    def render(self):
        with ColumnLayout(Class = "root"):
            Image(src = "./assets/brython.png", Class = "splash")

            Label("brue", Class = "title")
            Label("MVVM UI Toolkit", Class = "subtitle")
