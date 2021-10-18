# -*- coding: utf-8 -*-
from browser import html, document
from ._base import Base, global_state


class Container(Base, html.DIV):
    is_layout = True

    def __init__(self, **attrs):
        html.DIV.__init__(self)
        Base.__init__(self, **attrs)

class Fieldset(Base, html.FIELDSET):
    is_layout = True

    def __init__(self, title:str, **attrs):
        html.FIELDSET.__init__(self)
        Base.__init__(self, **attrs)

        self <= html.LEGEND(title)

    def __exit__(self, _t, _b, _tb):
        super().__exit__(_t, _b, _tb)

        # if len(self.children) == 2:
            # subs = f'calc({self.style["marginInlineStart"]} + {self.style["marginInlineEnd"]} + {self.style["paddingBlockStart"]} + {self.style["paddingInlineStart"]} + {self.style["paddingInlineEnd"]} + {self.style["paddingBlockEnd"]} + {self.style["borderWidth"]})'
            # self.children[1].style["height"] = f"calc({self.clientHeight}px - 6px - 2em)"

class RowLayout(Base, html.DIV):
    is_layout = True

    def __init__(self, spacing:int = 5, **attrs):
        html.DIV.__init__(self)
        Base.__init__(self, **attrs)

        self.spacing = spacing

        self.style["display"] = "flex"
        self.style["flexFlow"] = "row"

    def __exit__(self, _t, _b, _tb):
        super().__exit__(_t, _b, _tb)

        for child in self.children[:-1]:
            child.style["marginRight"] = f"{self.spacing}px"

class ColumnLayout(Base, html.DIV):
    is_layout = True

    def __init__(self, spacing:int = 5, **attrs):
        html.DIV.__init__(self)
        Base.__init__(self, **attrs)

        self.spacing = spacing

        self.style["display"] = "flex"
        self.style["flexFlow"] = "column"

    def __exit__(self, _t, _b, _tb):
        super().__exit__(_t, _b, _tb)

        for child in self.children[:-1]:
            child.style["marginBottom"] = f"{self.spacing}px"

class GridLayout(Base, html.DIV):
    is_layout = True

    def __init__(self, row_size:int = 3, column_size:int = 3, spacing:int = 5, **attrs):
        html.DIV.__init__(self)
        Base.__init__(self, **attrs)

        self.style["display"] = "grid"
        self.style["grid-template-rows"] = f"repeat({column_size}, 1fr)"
        self.style["grid-template-columns"] = f"repeat({row_size}, 1fr)"
        self.style["gap"] = f"{spacing}px"


class Slot:
    def __init__(self):
        global_state.current_component.slot_element = document.createElement("slot")
        global_state.current_layout <= global_state.current_component.slot_element
