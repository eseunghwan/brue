# -*- coding: utf-8 -*-
from brue import brueRoute
from views.Welcome import Welcome
from views.Counter import Counter
from views.DataGrid import DataGrid

routes = brueRoute([
    { "path": "/", "component": Welcome },
    { "path": "/counter", "component": Counter },
    { "path": "/datagrid", "component": DataGrid }
])
