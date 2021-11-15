# -*- coding: utf-8 -*-
from brue import brue
from store import store
from routes import routes

brue.use(store)
brue.use(routes)
