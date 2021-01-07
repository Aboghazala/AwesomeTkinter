#!/usr/bin/env python
"""
    AwesomeTkinter, a new tkinter widgets design using custom styles and images

    :copyright: (c) 2020 by Mahmoud Elshahat.

    module description:
        this is the main module which get executed when running command python -m awesometkinter
"""


import sys
import os

if __package__ is None and not hasattr(sys, 'frozen'):
    # direct call of __main__.py
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

    __package__ = 'awesometkinter'

    # load awesometkinter
    import awesometkinter

from .__init__ import main


if __name__ == '__main__':
    main() 
