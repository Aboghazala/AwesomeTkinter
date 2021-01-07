"""
    AwesomeTkinter, a new tkinter widgets design using custom styles and images

    :copyright: (c) 2020 by Mahmoud Elshahat.

"""
import tkinter as tk
from tkinter import ttk
from .utils import *


class SimpleScrollbar(ttk.Scrollbar):
    """Scrollbar without arrows"""
    style = []

    def __init__(self, parent, orient='horizontal', bg=None, slider_color=None, width=None, **options):
        """intialize scrollbar

        Args:
            orient (srt): 'horizontal' or 'vertical'
            bg (str): trough color
            slider_color (str): slider color
            width (int): slider width
        """

        # initialize super class
        ttk.Scrollbar.__init__(self, parent, **options)

        s = ttk.Style()
        self.bg = bg or 'white'
        self.slider_color = slider_color or 'blue'
        self.width = width or 5

        if orient == 'horizontal':
            # h_scrollbar
            custom_style = f'sb_{len(SimpleScrollbar.style)}.Horizontal.TScrollbar'
            s.layout(custom_style, [('Horizontal.Scrollbar.trough', {'sticky': 'we', 'children':
                                   [('Horizontal.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})]})])
        else:
            # v_scrollbar
            custom_style = f'sb_{len(SimpleScrollbar.style)}.Vertical.TScrollbar'
            s.layout(custom_style, [('Vertical.Scrollbar.trough', {'sticky': 'ns', 'children':
                                   [('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})]})])

        SimpleScrollbar.style.append(custom_style)

        s.configure(custom_style, troughcolor=self.bg, borderwidth=1, relief='flat', width=self.width)
        s.map(custom_style, background=[('', self.slider_color)])  # slider color

        self.config(orient=orient, style=custom_style) 
