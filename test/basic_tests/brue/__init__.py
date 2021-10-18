# -*- coding: utf-8 -*-
from typing import List, Dict, Any
from browser import webcomponent, html, window
from .ui._base import global_state, event_names
from . import router


class Store:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, dict):
                setattr(self, key, Store(**value))
            else:
                setattr(self, key, value)

class Brue:
    @staticmethod
    def create_store(source:dict) -> Store:
        global_state.store = Store(**source)

        return global_state.store

    @staticmethod
    def set_routes(routes:List[Dict[str, Any]]):
        for route in routes:
            if not "name" in route.keys():
                route["name"] = "default"

            global_state.registered_routes[route["name"]] = { "urls": { info["path"]: info["component"] for info in route["urls"] } }
    
        print(global_state.registered_routes)


class BrueDOM:
    @staticmethod
    def mount(comp, name:str = None, register_as_main_app:bool = True):
        if register_as_main_app:
            name = "app-main"
        else:
            if name is None:
                raw_comp_name = list(comp.__name__)
                upper_char_idx = [ idx for idx, char in enumerate(raw_comp_name) if not idx == 0 and char.isupper() ]
                for idx in sorted(upper_char_idx, reverse = True):
                    raw_comp_name.insert(idx, "-")
                
                name = "".join(raw_comp_name)

        global_state.registered_components[name.lower()] = comp.__name__
        webcomponent.define(name.lower(), comp)

        return comp

    @staticmethod
    def parse_to_element(self, object, root = None):
        tag_name = object.tagName.upper()
        if hasattr(html, tag_name):
            cls = getattr(html, tag_name)
        elif tag_name.startswith("ROUTER-"):
            tag_name = "".join([ item[0] + item[1:].lower() for item in tag_name.split("-") ])
            cls = getattr(router, tag_name)
        else:
            cls = html.maketag(tag_name)

        attributes, events = {}, {}
        for key, value in object.attrs.items():
            if value.startswith("self."):
                value = eval(value)
            elif value.strip().startswith("{") and value.strip().endswith("}"):
                value = eval(value)

            if key.startswith("on_"):
                may_event_name = key[3:]
                if may_event_name in event_names:
                    events[may_event_name] = eval(value) if isinstance(value, str) else value
            elif key == "model":
                # print(key, value)
                pass
            else:
                attributes[key] = value

        if len(object.children) == 0 and not cls.__name__ in ("RouterView",):
            element = cls(eval(f"f'''{object.textContent}'''"), **attributes)
        else:
            inner_text = object.textContent
            element = cls(**attributes)

        for child in object.children:
            BrueDOM.parse_to_element(self, child, element)

        if root is None:
            return element
        else:
            root <= element
