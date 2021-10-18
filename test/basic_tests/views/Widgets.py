# -*- coding: utf-8 -*-
from brue.core import Component
from brue.ui.layouts import ColumnLayout, RowLayout, Fieldset, GridLayout
from brue.ui.tags import UL, OL, LI, DL, DT, DD
from brue.ui.widgets import Label, Image, ProgressBar, Table
from brue.ui.controls import Entry, Select, Option, Button, CheckBox, Radio, Range
from brue.ui.medias import Video, Audio


@Component.register("view-widgets")
class Widgets(Component):
    state = {
        "slide": 30,
        "checked1": True,
        "checked2": False,
        "checked3": False,
        "radio": "option1"
    }

    def render(self):
        with ColumnLayout():
            with Fieldset(title = "html tags"):
                with ColumnLayout():
                    Label("UL")
                    with UL():
                        for idx in range(3):
                            LI(f"item{idx + 1}")

                    Label("OL")
                    with OL(start = 3, reversed = True):
                        for idx in range(3):
                            LI(f"item{idx + 1}")

                    Label("DL")
                    with DL():
                        for idx1 in range(3):
                            DT(f"category{idx1 + 1}")

                            for idx2 in range(3):
                                DD(f"item{idx1 + 1}/{idx2 + 1}")

            with Fieldset(title = "widgets"):
                with GridLayout(row_size = 3, column_size = 2):
                    Label("I'm label")
                    Image(src = "https://media.vlpt.us/images/milkyway/post/4b6bec16-34ed-4d40-acb7-23d596bb497e/HTML%20logo.jpeg", height = 200)
                    ProgressBar(value = self.state.slide)

                    with Table(row_span = 3):
                        with Table.Header():
                            for idx in range(4):
                                Table.Column(f"column {idx + 1}")

                        with Table.Body():
                            for ridx in range(4):
                                with Table.Row():
                                    for cidx in range(4):
                                        Table.Item(f"cell {ridx + 1}/{cidx + 1}")

            with Fieldset(title = "controls"):
                with GridLayout(row_size = 3, column_size = 3):
                    Entry(value = "I'm entry")
                    with Select():
                        Option("option1")
                        Option("option2")
                        Option("option3")
                        Option("option4")

                    Button("I'm button")

                    CheckBox("I'm checked", model = "self.state.checked1")
                    CheckBox("I'm unchecked", model = "self.state.checked2")
                    CheckBox("I'm readonly", model = "self.state.checked3", readonly = True)

                    Radio("option1", model = "self.state.radio")
                    Radio("option2", model = "self.state.radio")
                    Radio("I'm disabled", model = "self.state.radio", disabled = True)

                    Range("self.state.slide", row_span = 2)
                    Range("self.state.slide", orient = "vertical")

            with Fieldset(title = "medias"):
                with RowLayout():
                    Audio(src = "./assets/Netrum - Pixie Dust.mp3", style = { "flex": 1 })
                    Video(src = "https://youtu.be/LYFciXBcXIQ", autoplay = True, style = { "flex": 1 })
