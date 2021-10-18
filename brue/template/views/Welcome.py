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
        width: 100%;
        height: 300px;
        max-width: 700px;
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
            Image(src = "./assets/splash.png", Class = "splash")

            Label("brue", Class = "title")
            Label("modern web gui using python", Class = "subtitle")
