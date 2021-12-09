# -*- coding: utf-8 -*-
import os, sys, subprocess
from glob import glob

def transpile(source:str, dest:str, remove_dest:bool = False, search_css:bool = False, verbose:bool = True) -> str:
    subprocess.call([ sys.executable, "-m", "metapensiero.pj", source, "-o", dest ], stdout = sys.stdout if verbose else subprocess.DEVNULL)
    with open(dest, "r", encoding = "utf-8-sig") as rt:
        lines = []
        for line in rt.read().split("\n"):
            if remove_dest:
                cond = not line.strip().startswith("import {") and not line.strip().startswith("import *") and not line.strip().startswith("//# sourceMappingURL")
            else:
                cond = not line.strip().startswith("//# sourceMappingURL")

            if cond:
                lines.append(line)

        rtt = "\n".join(lines).strip()

    # rtt = rtt.split("_pj_snippets(_pj);")[-1]

    if search_css:
        try:
            class_name = [ line for line in rtt.split("\n") if line.strip().endswith("extends brueElement {") ][0].split("extends")[0][5:].strip()
            css_file = os.path.splitext(source)[0] + ".css"
            if os.path.exists(css_file):
                with open(css_file, "r", encoding = "utf-8-sig") as cr:
                    crt = cr.read()

                lines = rtt.split("\n")
                rtt = "\n".join(lines[:-1]) + '\nObject.defineProperty(' + class_name + ', "css_string", {"value": `' + crt + '`, "enumerable": false, "configurable": false, "writable": false});' + f"\n{lines[-1]}"
        except IndexError:
            pass

    if remove_dest:
        os.remove(dest)

    os.remove(dest + ".map")

    return rtt


def transpile_directory(source_patterns:str, dest_dir:str, ext:str = "js", merge_file:str = None, verbose:bool = False):
    texts = []

    dir_pattern = os.path.dirname(source_patterns)
    file_pattern = os.path.basename(source_patterns)

    files_to_transpile = glob(source_patterns) + glob(os.path.join(dir_pattern, "**", file_pattern))
    for idx, file in enumerate(files_to_transpile):
        file_name = os.path.splitext(os.path.basename(file))[0]
        texts.append(transpile(file, os.path.join(dest_dir, f"{file_name}.{ext}"), remove_dest = merge_file is None, search_css = True, verbose = verbose))

    if merge_file is not None:
        with open(os.path.join(dest_dir, "script.js"), "a", encoding = "utf-8-sig") as sw:
            sw.write("\n".join(texts))
    else:
        return "\n".join(texts)
