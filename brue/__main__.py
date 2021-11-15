# -*- coding: utf-8 -*-
import os, sys, argparse, shutil, minify_html, jsmin, zipfile
from glob import glob
from ._utils import transpile_directory, transpile
from . import __path__


parser = argparse.ArgumentParser(
    description = "cli for brue executions",
    prog = "brue-cli"
)

parser.add_argument("--init", dest = "init_dir", default = False)
parser.add_argument("--serve", type = int, dest = "serve_port", default = False)
parser.add_argument("--build", dest = "build_dir", default = False)


def build_project(build_dir:str, verbose:bool, minify_output:bool = True):
    source_dir = os.getcwd()
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)

    os.mkdir(build_dir)

    with open(os.path.join(__path__[0], "assets", "script.js"), "r", encoding = "utf-8-sig") as sfr:
        script_text = sfr.read()

    for file in glob(os.path.join(source_dir, "public", "*.*")):
        file_name = os.path.basename(file)
        if file_name == "index.html":
            with open(file, "r", encoding = "utf-8-sig") as ir:
                index_html = ir.read().replace("{project_name}", os.path.basename(source_dir)).replace('<!-- auto generation do not edit -->', '<script type="text/javascript" src="script.js"></script>')
        else:
            shutil.copyfile(file, os.path.join(build_dir, file_name))

    asset_dir = os.path.join(source_dir, "assets")
    if os.path.exists(asset_dir):
        shutil.copytree(asset_dir, os.path.join(build_dir, "assets"))

    script_text += transpile_directory(os.path.join(source_dir, "components", "[!_]*.py"), build_dir, verbose = verbose)
    script_text += transpile_directory(os.path.join(source_dir, "views", "[!_]*.py"), build_dir, remove_settings = True, verbose = verbose)

    store_file = os.path.join(source_dir, "store.py")
    if os.path.exists(store_file):
        script_text += transpile(store_file, os.path.join(build_dir, "store.js"), remove_settings = True, remove_dest = True, verbose = verbose)

    route_file = os.path.join(source_dir, "routes.py")
    if os.path.exists(route_file):
        script_text += transpile(route_file, os.path.join(build_dir, "routes.js"), remove_settings = True, remove_dest = True, verbose = verbose)

    script_text += transpile(os.path.join(source_dir, "main.py"), os.path.join(build_dir, "main.js"), remove_settings = True, remove_dest = True, verbose = verbose)
    script_text += transpile(os.path.join(source_dir, "App.py"), os.path.join(build_dir, "App.js"), remove_settings = True, remove_dest = True, verbose = verbose)

    ifw = open(os.path.join(build_dir, "index.html"), "w", encoding = "utf-8-sig")
    sfw = open(os.path.join(build_dir, "script.js"), "w", encoding = "utf-8-sig")

    if minify_output:
        ifw.write(minify_html.minify(index_html, remove_processing_instructions = True))
        sfw.write(jsmin.jsmin(script_text))
    else:
        ifw.write(index_html)
        ifw.write(script_text)

    ifw.close()
    sfw.close()

def run_cli():
    args = vars(parser.parse_args())

    if args["init_dir"]:
        init_dir = os.path.realpath(args["init_dir"])
        template_zip = zipfile.ZipFile(os.path.join(__path__[0], "assets", "template.zip"))
        if not os.path.exists(init_dir):
            os.mkdir(init_dir)

        template_zip.extractall(init_dir)
        template_zip.close()
    elif args["serve_port"]:
        host, port = "0.0.0.0", args["serve_port"]
        serve_dir = os.path.realpath("./.serve")
        build_project(serve_dir, False)
        os.chdir(serve_dir)
        try:
            os.system(f"{sys.executable} -m http.server {port} --bind {host}")
        except KeyboardInterrupt:
            pass

        shutil.rmtree(serve_dir)
    elif args["build_dir"]:
        build_project(os.path.realpath(args["build_dir"]), True)


if __name__ == "__main__":
    run_cli()
