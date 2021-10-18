# -*- coding: utf-8 -*-
from typing import Any
from browser import html, window
from ._base import Base

# inputs
class _FormBase(Base):
    def __init__(self, model:str = None, value:Any = None, bind_name:str = "keyup", value_name:str = "value", set_value:bool = True, **attrs):
        Base.__init__(self, **attrs)
        self.model_name = model
        self.value_name = value_name

        readonly, disabled = attrs.pop("readonly", False), attrs.pop("disabled", False)

        if value is not None:
            self.value = value

        if model is not None:
            if set_value:
                self.removeAttribute(value_name)
                setattr(self, value_name, self.root.state.find_by_address(model))

            if not readonly and not disabled:
                self.bind(bind_name, self.on_form_changed)

        if readonly or disabled:
            self.setAttribute("disabled", "")

    def __exit__(self, _t, _b, _tb):
        super().__exit__(_t, _b, _tb)

        if self.is_layout and self.model_name is not None:
            setattr(self, self.value_name, self.root.state.find_by_address(self.model_name))

    def on_form_changed(self, ev):
        self.root.state.update_by_address(self.model_name, getattr(self, self.value_name))

class Entry(_FormBase, html.INPUT):
    def __init__(self, value:Any = None, model:str = None, **attrs):
        html.INPUT.__init__(self, type = "text")
        _FormBase.__init__(self, model, value, **attrs)

class Select(_FormBase, html.SELECT):
    is_layout = True
    option_values = []

    def __init__(self, model:str = None, **attrs):
        html.SELECT.__init__(self)
        _FormBase.__init__(self, model, bind_name = "change", **attrs)

        self.option_values = []

class Option(Base, html.OPTION):
    def __init__(self, value:Any):
        self.raw_value = value

        html.OPTION.__init__(self)
        Base.__init__(self)

        self.innerHTML = str(value)
        self.parent.option_values.append(value)

class CheckBox(Base, html.LABEL):
    class InnerCheck(_FormBase, html.INPUT):
        def __init__(self, model:str, checked:bool, **attrs):
            html.INPUT.__init__(self, type = "checkbox")
            _FormBase.__init__(self, model, checked, bind_name = "click", value_name = "checked", **attrs)

        def on_form_changed(self, ev):
            self.root.state.update_by_address(self.model_name, self.checked)

    def __init__(self, text:str, model:str = None, checked:bool = False, **attrs):
        html.LABEL.__init__(self)
        frame_attrs = {
            key: attrs.pop(key)
            for key in ("style",)
            if key in attrs.keys()
        }
        Base.__init__(self, **frame_attrs)

        self.inner_check = self.InnerCheck(model, checked, **attrs)
        self <= self.inner_check
        self <= text

class Radio(Base, html.LABEL):
    class InnerRadio(_FormBase, html.INPUT):
        def __init__(self, text:str, model:str, value:str, **attrs):
            html.INPUT.__init__(self, type = "radio")
            _FormBase.__init__(self, model, text if value is None else value, "click", set_value = False, **attrs)

            if model is not None:
                if self.value == self.root.state.find_by_address(model):
                    self.checked = True

    def __init__(self, text:str, model:str = None, value:str = None, **attrs):
        html.LABEL.__init__(self)
        frame_attrs = {
            key: attrs.pop(key)
            for key in ("style",)
            if key in attrs.keys()
        }
        Base.__init__(self, **frame_attrs)

        self.inner_check = self.InnerRadio(text, model, value, **attrs)
        self <= self.inner_check
        self <= text

class Range(_FormBase, html.INPUT):
    def __init__(self, model:str = None, value:int = 0, min:int = 0, max:int = 100, step:int = None, orient:str = "hirozintal", **attrs):
        html.INPUT.__init__(self, type = "range", min = min, max = max, step = int((max - min) / 10) if step is None else step)
        _FormBase.__init__(self, model, value, "change", **attrs)

        if orient.lower() == "vertical":
            self.attrs["orient"] = "vertical"
            self.style["writing-ode"] = "bt-lr"
            self.style["-webkit-appearance"] = "slider-vertical"


# buttons
class Button(Base, html.BUTTON):
    def __init__(self, text:str, **attrs):
        html.BUTTON.__init__(self, text)
        Base.__init__(self, **attrs)
