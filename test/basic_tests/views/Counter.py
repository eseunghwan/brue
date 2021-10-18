# -*- coding: utf-8 -*-
from brue.core import Component
from brue.ui.layouts import ColumnLayout, RowLayout, Slot
from brue.ui.widgets import Label
from brue.ui.controls import Entry, Button

@Component.register("view-counter")
class Counter(Component):
    state = { "count": 0 }

    def count_up(self, ev):
        self.state.count += self.store.Counter.count_num

    def count_down(self, ev):
        if self.state.count > 0:
            self.state.count -= self.store.Counter.count_num

    def render(self):
        with ColumnLayout():
            Entry(model = "self.state.count")
            with RowLayout():
                Button("up!", on_click = self.count_up)
                Button("down!", on_click = self.count_down)

                Slot()
