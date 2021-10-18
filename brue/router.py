# -*- coding: utf-8 -*-
from browser import html
from typing import Union
from .ui._base import Base, global_state


class RouterLink(Base, html.A):
    def __init__(self, text:str = None, to:Union[str, dict] = "/", name:str = "default"):
        html.A.__init__(self, "" if text is None else text, href = "#")
        Base.__init__(self)

        if isinstance(to, str):
            self.target_url, self.comp_attrs, self.router_name = to, {}, name
        else:
            self.target_url = to.pop("url", "/")
            self.comp_attrs = to.pop("props", {})
            self.router_name = to.pop("name", name)

        self.bind("click", self.change_route_view)

    def change_route_view(self, ev):
        route_info = global_state.registered_routes[self.router_name]
        router_view = route_info["target"]

        current_layout = global_state.current_layout
        router_view.clear()
        global_state.current_layout = router_view
        route_info["urls"][self.target_url](**self.comp_attrs)

        global_state.current_layout = current_layout

class RouterView(Base, html.DIV):
    def __init__(self, name:str = "default"):
        html.DIV.__init__(self)
        Base.__init__(self)

        if name in global_state.registered_routes.keys():
            global_state.registered_routes[name]["target"] = self

            current_layout = global_state.current_layout
            global_state.current_layout = self
            global_state.registered_routes[name]["urls"]["/"]()

            global_state.current_layout = current_layout
