# -*- coding: utf-8 -*-
from brue import brueElement
from brue.decorators import defineElement

@defineElement("app-elm")
class App(brueElement):
    def __init__(self):
        super().__init__()

    def created(self):
        print("created")

    def mounted(self):
        print("mounted")

    def render(self):
        return """
        <div>
            <div>
                <router-link url="/">Welcome</router-link>
                <router-link url="/counter">Counter</router-link>
                <router-link url="/datagrid">DataGrid</router-link>
            </div>
            <router-view />
        </div>
        """
