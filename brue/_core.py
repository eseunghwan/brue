# -*- coding: utf-8 -*-

class brue:
    @staticmethod
    def use(cls):
        pass


class brueStore(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class brueRoute:
    def __init__(self, route_info:dict):
        pass


class brueElement:
    state:dict = {}
    props:dict = {}
    store:dict = {}
    refs:dict = {}

    def created(self):
        pass

    def mounted(self):
        pass

    def render(self) -> str:
        pass
