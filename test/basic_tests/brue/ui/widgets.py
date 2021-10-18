# -*- coding: utf-8 -*-
from typing import Union
from browser import html, window
from ._base import Base


class Label(Base, html.LABEL):
    def __init__(self, text:str, **attrs):
        html.LABEL.__init__(self, text)
        Base.__init__(self, **attrs)

class Image(Base, html.DIV):
    def __init__(self, src:str, width:Union[str, int] = "100%", height:Union[str, int] = "100%", **attrs):
        html.DIV.__init__(self)
        Base.__init__(self, **attrs)

        self.attrs["style"] = f"background-image:url('{src}');"

        if isinstance(width, int):
            self.style["width"] = width = f"{width}px"
            self.style["width"] = width

        if isinstance(height, int):
            self.style["height"] = height = f"{height}px"
            self.style["height"] = height

        self.style["backgroundSize"] = f"{width} {height}"

class ProgressBar(Base, html.PROGRESS):
    def __init__(self, max:int = 100, value:int = 0, **attrs):
        html.PROGRESS.__init__(self)
        Base.__init__(self, **attrs)

        self.attrs["max"] = max
        self.attrs["value"] = value


class Table(Base, html.TABLE):
    is_layout = True

    def __init__(self, **attrs):
        html.TABLE.__init__(self)
        Base.__init__(self, **attrs)

    class Header(Base, html.THEAD):
        is_layout = True

        def __init__(self, **attrs):
            html.THEAD.__init__(self)
            Base.__init__(self, **attrs)

        def __enter__(self):
            super().__enter__()

            self.row = Table.Row()
            self.row.__enter__()

        def __exit__(self, _t, _b, _tb):
            self.row.__exit__(_t, _b, _tb)
            super().__exit__(_t, _b, _tb)

    class Column(Base, html.TH):
        def __init__(self, text:str, **attrs):
            html.TH.__init__(self, text)
            Base.__init__(self, **attrs)

    class Body(Base, html.TBODY):
        is_layout = True

        def __init__(self, **attrs):
            html.TBODY.__init__(self)
            Base.__init__(self, **attrs)

    class Row(Base, html.TR):
        is_layout = True

        def __init__(self, **attrs):
            html.TR.__init__(self)
            Base.__init__(self, **attrs)

    class Item(Base, html.TD):
        def __init__(self, text:str, **attrs):
            html.TD.__init__(self, text)
            Base.__init__(self, **attrs)
