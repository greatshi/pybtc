#coding=utf-8
from distutils.core import setup
import py2exe

# Usage: python 2exe.py py2exe

setup(
    options = {'py2exe': {
        'bundle_files': 1
    }},
    console = [{'script': 'strategy.py'}],
    zipfile = None
)