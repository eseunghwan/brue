# -*- coding: utf-8 -*-
from setuptools import setup
from brue import __author__, __mail__, __version__

with open("requirements.txt", "r", encoding = "utf-8-sig") as reqr:
    requires = reqr.read().split("\n")

with open("README.md", "r", encoding = "utf-8-sig") as rmr:
    readme = rmr.read()


setup(
    author = __author__,
    author_email = __mail__,
    url = "https://github.com/eseunghwan/brue",
    version = __version__,
    python_requires = ">=3.7",
    install_requires = requires,
    setup_requires = requires,
    entry_points = {
        "console_scripts": [
            "brue-cli=brue.__main__:run_cli"
        ]
    },
    name = "brue",
    license="MIT license",
    description = "modern web gui using python",
    long_description = readme,
    long_description_content_type = "text/markdown",
    packages = [ "brue", "brue/assets" ],
    package_data = {
        "": [
            "*.zip", "*.js"
        ]
    },
    include_package_data = True,
    zip_fale = True
)
