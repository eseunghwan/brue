# -*- coding: utf-8 -*-
from brue import brueElement
from brue.decorators import defineElement

@defineElement("view-welcome")
class Welcome(brueElement):
    def __init__(self):
        super().__init__()

    def test_click(self):
        print("test!")

    def render(self):
        return """
        <comp-hello name="eseunghwan" :on-click="self.test_click">
            <button>click me!</button>
        </comp-hello>
        """
