# -*- coding: utf-8 -*-
from brue import Brue, BrueDOM
from App import App
from store import store
from routes import routes


Brue.create_store(store)
Brue.set_routes(routes)
BrueDOM.mount(App, "app-main")
