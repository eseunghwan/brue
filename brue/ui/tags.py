# -*- coding: utf-8 -*-
from browser import html
from ._base import Base



class I(Base, html.I):
    def __init__(self, text:str = "", **attrs):
        html.I.__init__(self, text)
        Base.__init__(self, **attrs)

class UL(Base, html.UL):
    is_layout = True

    def __init__(self, **attrs):
        html.UL.__init__(self)
        Base.__init__(self, **attrs)

class OL(Base, html.OL):
    is_layout = True

    def __init__(self, start:int = 1, reversed:bool = False, **attrs):
        html.OL.__init__(self, start = start)
        Base.__init__(self, **attrs)

        if reversed:
            self.setAttribute("reversed", "")

class DL(Base, html.DL):
    is_layout = True

    def __init__(self, **attrs):
        html.DL.__init__(self)
        Base.__init__(self, **attrs)


class LI(Base, html.LI):
    is_layout = True

    def __init__(self, text:str = None, **attrs):
        html.LI(self)
        Base.__init__(self, **attrs)

        if text is not None:
            self.innerText = text

class DT(Base, html.DT):
    def __init__(self, text:str, **attrs):
        html.DT.__init__(self, text)
        Base.__init__(self, **attrs)

class DD(Base, html.DD):
    def __init__(self, text:str, **attrs):
        html.DD.__init__(self, text)
        Base.__init__(self, **attrs)
