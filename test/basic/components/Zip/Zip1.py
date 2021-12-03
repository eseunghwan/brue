# -*- coding: utf-8 -*-
from brue import brueElement
from brue.decorators import defineElement

@defineElement("comp-zip1")
class Zip1(brueElement):
    props = {
        "name": str
    }

    def __init__(self):
        super().__init__()

    def render(self):
        return f"""
        <h3>Hello {self.props.name}!</h3>
        """
