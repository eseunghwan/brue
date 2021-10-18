# -*- coding: utf-8 -*-
from typing import Dict, Any, Union
from browser import document, window
from .ui._base import global_state
from . import BrueDOM, Store

class State:
    is_init:bool = True

    def __init__(self, comp, state:dict):
        self.is_init = True
        self.comp = comp
        self.state_keys = list(state.keys())
        
        for key, value in state.items():
            if isinstance(value, dict):
                setattr(self, key, State(comp, value))
            else:
                setattr(self, key, value)

        self.is_init = False

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

        if hasattr(self, "state_keys") and not self.is_init and name in self.state_keys:
            self.comp.update()

    def find_by_address(self, address:str):
        if address.startswith("self.state"):
            address = address[11:]

        return getattr(self, address)

    def update_by_address(self, address:str, value):
        if address.startswith("self.state"):
            address = address[11:]

        value_type = type(self.find_by_address(address))
        setattr(self, address, value_type(value))

class Props:
    def __init__(self, comp, props:dict):
        for key, p_type in props.items():
            if key in comp.attrs.keys():
                setattr(self, key, p_type(comp.attrs[key]))
                del comp.attrs[key]
            else:
                setattr(self, key, p_type())

        setattr(self, "__setattr__", lambda: None)

class FakeComponent:
    def __enter__(self):
        return self

    def __exit__(self, _t, _b, _tb):
        pass

class Component:
    slot_element = None
    focus_address = []

    props:Union[Dict[str, Any], Props] = {}
    state:Union[Dict[str, Any], State] = {}
    css:str = ""

    @staticmethod
    def register(name:str = None):
        def decorator(comp):
            return BrueDOM.mount(comp, name, False)

        return decorator

    def __init__(self):
        self.attachShadow({"mode": "open"})
        self.state = State(self, self.state)

    def __new__(cls, **props) -> FakeComponent:
        comp_name = [ key for key, value in global_state.registered_components.items() if value == cls.__name__ ][0]
        element = document.createElement(comp_name)
        for key, value in props.items():
            element.setAttribute(key, value)

        global_state.current_layout <= element

        return FakeComponent()

    def __del__(self):
        self.disconnectedCallback()

    def get_focus_address(self, element):
        self.focus_address = []

        while True:
            if element.parentNode is None:
                break

            self.focus_address.insert(0, element.parentNode.children.index(element))
            element = element.parentNode

        if len(self.focus_address) == 1:
            self.focus_address.clear()

    @property
    def store(self) -> Store:
        return global_state.store

    def connectedCallback(self):
        self.props = Props(self, self.props)

        self.update()

    def disconnectedCallback(self):
        self.clear()

    def update(self):
        # parser = window.DOMParser.new()
        # self.shadowRoot <= BrueDOM.parse_to_element(self, parser.parseFromString(self.render(), "application/xml").firstChild)

        global_state.current_component = self

        self.shadowRoot.clear()
        if not self.css.strip() == "":
            style = document.createElement("style")
            style.innerHTML = self.css
            self.shadowRoot <= style

        global_state.current_layout = self.shadowRoot
        self.render()

        if not self.focus_address == []:
            element = self.shadowRoot.children[self.focus_address[0]]
            for address in self.focus_address[1:]:
                element = element.children[address]

            element.focus()

        if self.slot_element is not None:
            global_state.current_layout = self.slot_element
        else:
            global_state.current_layout = self.parentNode

    def render(self):
        return None
