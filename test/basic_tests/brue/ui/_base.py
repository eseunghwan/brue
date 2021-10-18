# -*- coding: utf-8 -*-
from browser import window

event_names = (
    # mouse events
    "click", "dblclick", "mouseenter", "mouseleave", "mouseover", "mouseout", "mousemove", "mousedown", "mouseup",
    # keyboard events
    "input", "keypress", "keyup",
    # focus events
    "blur", "focus",
    # drag events
    "drag", "drop", "dragstart", "dragend", "dragenter", "dragleave", "dragover"
)

class global_state:
    registered_components = {}
    registered_routes = {}
    store = None

    current_component = None
    current_layout = None

class Base:
    root = None
    is_layout:bool = False
    is_entered:bool = False

    def __init__(self, **attrs):
        self.root = global_state.current_component

        self.bind("focus", self.__on_focus)

        style = attrs.pop("style", {})
        if global_state.current_layout.__class__.__name__ == "GridLayout":
            spans = [ key for key in attrs.keys() if key.endswith("_span") ]
            for span in spans:
                direction = span[:-5]
                if direction == "row":
                    style["grid-column"] = f"span {attrs.pop(span)}"
                else:
                    style["grid-row"] = f"span {attrs.pop(span)}"

        if "width" in attrs.keys():
            raw_width = attrs.pop("width")
            self.style["width"] = f"{raw_width}px" if isinstance(raw_width, int) else raw_width

        if "height" in attrs.keys():
            raw_height = attrs.pop("height")
            self.style["height"] = f"{raw_height}px" if isinstance(raw_height, int) else raw_height

        for key, value in style.items():
            self.style[key] = value

        for key, value in attrs.items():
            if key.startswith("on_"):
                bind_name = key[3:]
                if bind_name in event_names:
                    self.bind(bind_name, value)
                else:
                    print(f"supported events are {event_names}!")
            else:
                self.attrs[key] = value

        if global_state.current_layout is not None:
            global_state.current_layout <= self

    def __enter__(self):
        if self.is_layout:
            global_state.current_layout = self
            self.is_entered = True

        return self

    def __exit__(self, _t = None, _b = None, _tb = None):
        if self.is_layout:
            global_state.current_layout = self.parentNode

    def __on_focus(self, ev):
        if self.root is not None:
            self.root.get_focus_address(self)
