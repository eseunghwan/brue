# -*- coding: utf-8 -*-
from brue import brueElement
from brue.decorators import defineElement

@defineElement("view-welcome")
class Welcome(brueElement):
    def __init__(self):
        super().__init__()

    def render(self):
        return """
        <comp-hello name="eseunghwan"></comp-hello>
        """
