# -*- coding: utf-8 -*-
from brue import brueElement
from brue.decorators import defineElement
from brue.directives import repeat

@defineElement("data-grid")
class DataGrid(brueElement):
    state = {
        "columns": [ "A", "B", "C", "D" ],
        "datas": [ [1, 2, 3, 4], [5, 6, 7, 8] ]
    }

    def __init__(self):
        super().__init__()

    def render(self):
        return f"""
        <div>
            <table>
                <thead>
                    {repeat(self.state.columns, lambda c: f"<th>{c}</th>")}
                </thead>
                <tbody>
                    {repeat(self.state.datas, lambda it: f'''<tr>{repeat(it, lambda d: f"<td>{d}</td>")}</tr>''')}
                </tbody>
            </table>
        </div>
        """
