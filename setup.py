#!/usr/bin/env python
# coding: utf-8

# Python 2.7 Standard Library
import sys

# Third-Party Libraries
try:
    import setuptools
except ImportError:
    error = "pip is not installed, refer to <{url}> for instructions."
    raise ImportError(error.format(url="http://pip.readthedocs.org"))

# Setup-Time Dependencies
sys.path.insert(0,"lib")
import about

# Project Library
import wish

contents     = dict(py_modules = ["wish"])
requirements = dict(install_requires = ["setuptools"])
data         = dict(data_files = [("", ["README.md"])])
plugins      = dict()
tests        = dict(test_suite = "test.test_suite")

info = {}
info.update(contents)
info.update(requirements)
info.update(data)
info.update(plugins)
info.update(tests)

if __name__ == "__main__":
    about.setup(wish, **info)

