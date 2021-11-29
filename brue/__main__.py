# -*- coding: utf-8 -*-
import os, sys, argparse, json, shutil, minify_html, jsmin, zipfile
from glob import glob
from ._utils import transpile_directory, transpile
from . import __path__


def read_config() -> dict:
    if os.path.exists(os.path.join(os.getcwd(), "config.json")):
        with open(os.path.join(os.getcwd(), "config.json"), "r", encoding = "utf-8-sig") as cr:
            config = json.load(cr)
    else:
        config = {
            "build": {
                "target": "./build"
            },
            "serve": {
                "port": 8080
            }
        }

    return config

# functions
def build_project_raw(build_dir:str, verbose:bool, minify_output:bool = True):
    source_dir = os.getcwd()
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)

    os.mkdir(build_dir)

    with open(os.path.join(__path__[0], "assets", "script.js"), "r", encoding = "utf-8-sig") as sfr:
        script_text = sfr.read()

    if verbose:
        print("copying public files...")

    for file in glob(os.path.join(source_dir, "public", "*.*")):
        file_name = os.path.basename(file)
        if file_name == "index.html":
            with open(file, "r", encoding = "utf-8-sig") as ir:
                index_html = ir.read().replace("{project_name}", os.path.basename(source_dir)).replace('<!-- auto generation do not edit -->', '<script type="text/javascript" src="script.js"></script>')
        else:
            shutil.copyfile(file, os.path.join(build_dir, file_name))

    asset_dir = os.path.join(source_dir, "assets")
    if os.path.exists(asset_dir):
        if verbose:
            print("\ncopying asset files...")

        shutil.copytree(asset_dir, os.path.join(build_dir, "assets"))

    if verbose:
        print("\ncompiling component files...")

    script_text += transpile_directory(os.path.join(source_dir, "components", "[!_]*.py"), build_dir, verbose = verbose)

    if verbose:
        print("\ncompiling view files...")

    script_text += transpile_directory(os.path.join(source_dir, "views", "[!_]*.py"), build_dir, remove_settings = True, verbose = verbose)

    store_file = os.path.join(source_dir, "store.py")
    if os.path.exists(store_file):
        if verbose:
            print("\ncompiling store file...")
        script_text += transpile(store_file, os.path.join(build_dir, "store.js"), remove_settings = True, remove_dest = True, verbose = verbose)

    route_file = os.path.join(source_dir, "routes.py")
    if os.path.exists(route_file):
        if verbose:
            print("\ncompiling route file...")
        script_text += transpile(route_file, os.path.join(build_dir, "routes.js"), remove_settings = True, remove_dest = True, verbose = verbose)

    if verbose:
        print("\ncompiling App files...")

    script_text += transpile(os.path.join(source_dir, "main.py"), os.path.join(build_dir, "main.js"), remove_settings = True, remove_dest = True, verbose = verbose)
    script_text += transpile(os.path.join(source_dir, "App.py"), os.path.join(build_dir, "App.js"), remove_settings = True, remove_dest = True, verbose = verbose)

    ifw = open(os.path.join(build_dir, "index.html"), "w", encoding = "utf-8-sig")
    sfw = open(os.path.join(build_dir, "script.js"), "w", encoding = "utf-8-sig")

    if minify_output:
        ifw.write(minify_html.minify(index_html, remove_processing_instructions = True))
        sfw.write(jsmin.jsmin(script_text))
    else:
        ifw.write(index_html)
        sfw.write(script_text)

    ifw.close()
    sfw.close()

    if verbose:
        print(f"build finished in {build_dir}")

def init_project(args):
    init_dir = os.path.realpath(args["target"])
    template_zip = zipfile.ZipFile(os.path.join(__path__[0], "assets", "template.zip"))
    if not os.path.exists(init_dir):
        os.mkdir(init_dir)

    print("extracting files...")
    template_zip.extractall(init_dir)
    template_zip.close()
    print(f"brue project initialized in {init_dir}\n")

def serve_project(args):
    config = read_config()["serve"]

    host, port = "0.0.0.0", config["port"] if args["port"] is None else args["port"]
    serve_dir = os.path.realpath("./.serve")
    build_project_raw(serve_dir, False, False)
    os.chdir(serve_dir)
    try:
        os.system(f"{sys.executable} -m http.server {port} --bind {host}")
    except KeyboardInterrupt:
        pass

    shutil.rmtree(serve_dir)

def build_project(args):
    config = read_config()["build"]

    build_dir = config["target"] if args["target"] is None else args["target"]
    build_project_raw(os.path.realpath(build_dir), True)


parser = argparse.ArgumentParser(
    description = "cli for brue executions",
    prog = "brue-cli"
)
sparser = parser.add_subparsers()

init_parser = sparser.add_parser("init")
init_parser.add_argument("--target", default = "./")
init_parser.set_defaults(func = init_project)

serve_parser = sparser.add_parser("serve")
serve_parser.add_argument("--port", default = None)
serve_parser.set_defaults(func = serve_project)

build_parser = sparser.add_parser("build")
build_parser.add_argument("--target", default = None)
build_parser.set_defaults(func = build_project)

def run_cli():
    args = parser.parse_args()
    args.func(vars(args))


if __name__ == "__main__":
    run_cli()
