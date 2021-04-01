"""
    AwesomeTkinter, a new tkinter widgets design using custom styles and images

    :copyright: (c) 2020 by Mahmoud Elshahat.

"""

import tkinter as tk
from tkinter import ttk
from .utils import *
from .scrollbar import SimpleScrollbar


class ScrolledText(tk.Frame):
    """Scrolled multiline entry good for log output

    has both horizontal and vertical scrollbar

    auto-scroll vertically by default, if you move vertical scrollbar it will stop auto  scroll until vertical
    scroll bar moved back to bottom

    undo action disabled to save memory

    you can pass extra parameter to Text thru ScrolledText().text.config(**options)
    """

    def __init__(self, parent, bg='white', fg='black', bd=0, wrap=None, vscroll=True, hscroll=True, autoscroll=True,
                 max_chars=None, sbar_fg=None, sbar_bg=None, vbar_width=10, hbar_width=10, **kwargs):
        """initialize

        Args:
            parent (tk.Frame): parent widget
            bg (str): background color
            fg (str): foreground color
            bd (int): border width
            wrap (bool): wrap text, if omitted it will be true if no hscroll
            vscroll (bool): include vertical scrollbar
            hscroll (bool): include horizontal scrollbar
            autoscroll (bool): automatic vertical scrolling
            max_chars (int): maximum characters allowed in Text widget, text will be truncated from the beginning to
                             match the max chars
            sbar_fg (str): color of scrollbars' slider
            sbar_bg (str): color of scrollbars' trough, default to frame's background
            vbar_width (int): vertical scrollbar width
            hbar_width (int): horizontal scrollbar width

        """
        tk.Frame.__init__(self, parent, bg=bg)

        self.bd = bd
        self.bg = bg
        self.fg = fg
        self.vscroll = vscroll
        self.hscroll = hscroll
        self.autoscroll = autoscroll
        self.max_chars = max_chars
        self.sbar_bg = sbar_bg
        self.sbar_fg = sbar_fg

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.var = tk.StringVar()

        # wrap mechanism
        if wrap or not hscroll:
            wrap = tk.WORD
        else:
            wrap = 'none'

        self.text = tk.Text(self, bg=self.bg, fg=self.fg, bd=self.bd, wrap=wrap, undo='false', **kwargs)
        self.text.grid(sticky='ewns')

        if self.vscroll:
            self.vbar = SimpleScrollbar(self, orient='vertical', command=self.text.yview, slider_color=self.sbar_fg,
                                        bg=self.sbar_bg, width=vbar_width)
            self.vbar.grid(row=0, column=1, sticky='ns')
            self.text.config(yscrollcommand=self.vbar.set)

        if self.hscroll:
            self.hbar = SimpleScrollbar(self, orient='horizontal', command=self.text.xview, slider_color=self.sbar_fg,
                                        bg=self.sbar_bg, width=hbar_width)
            self.hbar.grid(row=1, column=0, sticky='ew')
            self.text.config(xscrollcommand=self.hbar.set)

        # bind mouse wheel to scroll
        scroll_with_mousewheel(self.text)

        # aliases
        self.delete = self.text.delete
        self.get = self.text.get
        self.delete = self.text.delete
        self.insert = self.text.insert

    def set(self, text):
        """replace contents"""
        self.clear()

        if self.max_chars:
            count = len(text)
            if count > self.max_chars:
                delta = count - self.max_chars
                text = text[delta:]

        self.text.insert("1.0", text)

        self.scrolltobottom()

    def clear(self):
        """clear all Text widget contents"""
        self.text.delete("1.0", tk.END)

    def append(self, text, text_color=None, text_bg=None):
        """append text with arbitrary colors"""

        color_tags = []

        if text_color:
            self.text.tag_configure(text_color, foreground=text_color)
            color_tags.append(text_color)

        if text_bg:
            self.text.tag_configure(text_bg, foreground=text_bg)
            color_tags.append(text_bg)

        self.text.insert(tk.END, text, ','.join(color_tags))

        self.remove_extra_chars()

        self.scrolltobottom()

    def remove_extra_chars(self):
        """remove characters from beginning of Text widget if it exceeds max chars"""
        if self.max_chars:
            # get current text characters count
            # txt = self.text.get()
            count = len(self.text.get("1.0", tk.END))
            if count > self.max_chars:
                delta = count - self.max_chars
                self.text.delete("1.0", f"1.0 + {delta} chars")

    def scrolltobottom(self):
        """scroll to bottom if autoscroll enabled and scrollbar position at the bottom"""
        try:
            if self.autoscroll and self.vbar.get()[1] == 1:
                self.text.yview_moveto("1.0")
        except:
            pass 
