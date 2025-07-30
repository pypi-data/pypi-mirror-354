# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

setup(
name = "q4nwin",
version = "0.1.1",
keywords = ("winpwn"),
description = "my windows pwntools",
license = "MIT Licence",

url = "https://github.com/Q4n/mywinpwn",
author = "Q4n",
author_email = "atq4n@qq.com",

packages = find_packages(),
include_package_data = True,
platforms = "Windows",
install_requires = ["six"]
)
