# -*- coding: utf-8 -*-

from setuptools import setup

__version__ = "2021.10.19"
__author__ = "Lee Seung Hwan"
__mail__ = "shlee0920@naver.com"

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
    entry_points = {
        "console_scripts": [
            "brue-cli=brue.cli:main"
        ]
    },
    name = "brue",
    license="MIT license",
    description = "modern web gui using python",
    long_description = readme,
    long_description_content_type = "text/markdown",
    packages = [ "brue", "brue/ui", "brue/assets" ],
    package_data = {
        "": [
            "*.zip", "*.html"
        ]
    },
    include_package_data = True,
    zip_fale = True
)
