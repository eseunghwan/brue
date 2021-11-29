<p style="text-align:center;">
<img src="https://raw.githubusercontent.com/eseunghwan/brue/master/test/basic/assets/splash.png" width="200px" height="200px" title="brue_logo"></img><br>
<font size="7">brue</font><br>
<a href="https://pypi.python.org/pypi/brue"><image src="https://img.shields.io/pypi/v/brue.svg" /></a><hr>
<font size="4">write in python, transpile to js, run in browser</font>
</p>
<br><br><br><br><br><br>


# Install
## using pip(stable)
```powershell
pip3 install brue
```
## using git(dev)
```powershell
pip3 install https://github.com/eseunghwan/brue.git
```
<br><br>

# Cli
### create project with cli
```powershell
brue-cli init [dest(default = "./")]

// example
brue-cli init ./test2
[output]
extracting files...
brue project initialized in [dest]
```
<br>

### run with server
```powershell
brue-cli serve [port(default = 8080)]

// example
brue-cli --serve 8080
[output]
Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
```
<br>

### build project file to standalone .html and .js
```powershell
brue-cli build [dest(default = "./build")]

// example
brue-cli --build ./build
[output]
copying public files...
copying asset files...
compiling component files...
...
Compiled file [dest]
```
<br><br>


# Component define
### component python file
```python
from brue import brueElement
from brue.decorators import defineElement

@defineElement("app-elm")# register element as [name]
class App(brueElement):
    def __init__(self):
        super().__init__()# must be called

    def created(self):# evalute when component created(initialized)
        print("created")

    def mounted(self):# evalute when componet rendered in html
        print("mounted")

    def render(self):# define render template as html-string
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
```
<br>

### condition(if)
```python
...
state = {
    "is_flag": True
}
{ "flag!" if self.state.is_flag else "not flag!" }
...

[expected output]
<if is_flag>
flag!
<else>
not flag!
```
<br>

### repeat(for)
```python
...
state = {
    "columns": [ "A", "B", "C", "D" ]
}
...
{repeat(self.state.columns, lambda c: f"<th>{c}</th>")}
...

[expected output]
<th>A</th>
<th>B</th>
<th>C</th>
<th>D</th>
```
<br>


