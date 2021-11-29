# -*- coding: utf-8 -*-
from brue import brueElement
from brue.decorators import defineElement

@defineElement("view-counter")
class Counter(brueElement):
    state = {
        "count": 0
    }

    def __init__(self):
        super().__init__()

    def count_up(self):
        self.state.count += self.store.count_num

    def count_down(self):
        if self.state.count > 0:
            self.state.count -= self.store.count_num

    def render(self):
        return f"""
        <div class="column">
            <input type="text" :model="self.store.count_num">
            <label>clicked {self.state.count} times!</label>
            <label>{ "up" if self.state.count > 10 else "down" }</label>
            <div class="row">
                <button :on-click="self.count_up" style="flex:1;">up!</button>
                <button :on-click="self.count_down" style="flex:1;">down!</button>
            </div>
        </div>
        """
