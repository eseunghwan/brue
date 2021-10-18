# -*- coding: utf-8 -*-
import os, sys, zipfile, subprocess, shutil
from . import __path__


def init_project(dest_directory:str):
    template = zipfile.ZipFile(os.path.join(__path__[0], "assets", "template.zip"))

    if not os.path.exists(dest_directory):
        os.mkdir(dest_directory)

    template.extractall(dest_directory)

    brython_dist = os.path.join(__path__[0], "brython_files")
    if not os.path.exists(brython_dist):
        os.mkdir(brython_dist)

    os.chdir(brython_dist)
    subprocess.call([ "echo", "N", "|", "brython-cli", "--install" ])

    os.chdir(dest_directory)
    subprocess.call([ sys.executable, "-m", "pip", "install", "virtualenv" ])
    subprocess.call([ sys.executable, "-m", "virtualenv", os.path.join(dest_directory, "env") ])
    subprocess.call([ os.path.join(__path__[0], "env", "Scripts" if sys.platform == "win32" else "bin", "python"), "-m", "pip", "install", "pip", "pylint", "brue", "--upgrade" ])

def serve_project(host:str, port:int, run_http_server:bool = True, remove_temp:bool = True) -> str:
    project_root = os.getcwd()
    serve_temp = os.path.join(project_root, ".serve")
    if os.path.exists(serve_temp):
        shutil.rmtree(serve_temp)

    os.mkdir(serve_temp)

    for file in [ file for file in os.listdir(project_root) if not file.startswith(".") ]:
        if not file in ("env",):
            source = os.path.join(project_root, file)
            dest = os.path.join(serve_temp, file)

            if os.path.isdir(source):
                shutil.copytree(source, dest)
            else:
                shutil.copyfile(source, dest)

    os.mkdir(os.path.join(serve_temp, "brue"))
    for file in os.listdir(__path__[0]):
        if not file in ("template.zip", "brython_files"):
            source = os.path.join(__path__[0], file)
            dest = os.path.join(serve_temp, "brue", file)

            if os.path.isdir(source):
                shutil.copytree(source, dest)
            else:
                shutil.copyfile(source, dest)

    for file in ("brython.js", "brython_stdlib.js"):
        shutil.copyfile(os.path.join(__path__[0], "brython_files", file), os.path.join(serve_temp, file))

    if run_http_server:
        try:
            os.chdir(serve_temp)
            subprocess.call([ sys.executable, "-m", "http.server", str(port), "--bind", host ])
        except KeyboardInterrupt:
            pass

    if remove_temp:
        shutil.rmtree(serve_temp)

    return serve_temp

def build_project(dist_directory:str):
    serve_temp = serve_project("127.0.0.1", 8000, False, False)

    os.chdir(serve_temp)
    subprocess.call([ sys.executable, "-m", "brython", "--modules" ])

    with open(os.path.join(serve_temp, "brython.js"), encoding = "utf-8-sig") as br:
        with open(os.path.join(serve_temp, "brython_modules.js"), encoding = "utf-8-sig") as bmr:
            with open(os.path.join(serve_temp, "script.js"), "w", encoding = "utf-8-sig") as sw:
                sw.write(br.read() + "\n\n" + bmr.read())

    for directory in ("brue", "components", "views"):
        shutil.rmtree(os.path.join(serve_temp, directory))

    for file in ("index.html", "main.py", "brython_stdlib.js", "brython_modules.js"):
        os.remove(os.path.join(serve_temp, file))

    shutil.copyfile(os.path.join(__path__[0], "assets", "build.html"), os.path.join(serve_temp, "index.html"))
    shutil.move(serve_temp, dist_directory)


def main():
    args = sys.argv[1:]
    job = args.pop(0)

    if job == "init":
        if len(args) == 0:
            dest = os.getcwd()
        else:
            dest = os.path.realpath(args[0])

        init_project(dest)

    elif job == "serve":
        if len(args) == 0:
            host, port = "127.0.0.1", 8000
        elif len(args) == 1:
            try:
                int(args[0])
                host, port = "120.0.0.1", args[0]
            except:
                host, port = args[0], 8000
        else:
            host, port = args[:2]

        serve_project(host, int(port))

    elif job == "build":
        if len(args) == 0:
            dest = os.path.join(os.getcwd(), "dist")
        else:
            dest = os.path.join(os.getcwd(), args[0])

        build_project(dest)
