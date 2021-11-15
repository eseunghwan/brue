
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
        self.state.count += 1

    def count_down(self):
        if self.state.count > 0:
            self.state.count -= 1

    def render(self):
        return f"""
        <div class="column">
            <label>clicked {self.state.count} times!</label>
            <div class="row">
                <button :click="self.count_up" style="flex:1;">up!</button>
                <button :click="self.count_down" style="flex:1;">down!</button>
            </div>
        </div>
        """
