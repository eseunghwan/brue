# -*- coding: utf-8 -*-
from views.Welcome import Welcome
from views.Counter import Counter
from views.Widgets import Widgets

routes = [
    {
        "name": "route1",
        "urls": [
            { "path": "/", "component": Welcome },
            { "path": "/Counter", "component": Counter },
            { "path": "/Widgets", "component": Widgets }
        ]
    }
]
