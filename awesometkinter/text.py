"""
    AwesomeTkinter, a new tkinter widgets design using custom styles and images

    :copyright: (c) 2020 by Mahmoud Elshahat.

"""

import tkinter as tk
from tkinter import ttk
from .utils import *
from .scrollbar import SimpleScrollbar


class ScrolledText(tk.Text):
    """Scrolled multiline entry good for log output

    has both horizontal and vertical scrollbar

    auto-scroll vertically by default, if you move vertical scrollbar it will stop auto scroll until vertical
    scroll bar moved back to bottom

    undo action disabled to save memory

    basically, this is a Text widget inside an outer Frame with scrolllbars,
    pack, grid, and place methods for Text will be replaced by outer frame methods

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

        self.bd = bd
        self.bg = bg
        self.fg = fg
        self.vscroll = vscroll
        self.hscroll = hscroll
        self.autoscroll = autoscroll
        self.max_chars = max_chars
        self.sbar_bg = sbar_bg
        self.sbar_fg = sbar_fg

        self.var = tk.StringVar()

        # wrap mechanism
        if wrap or not hscroll:
            wrap = tk.WORD
        else:
            wrap = 'none'

        # create outside frame
        self.fr = tk.Frame(parent, bg=bg)

        self.fr.rowconfigure(0, weight=1)
        self.fr.columnconfigure(0, weight=1)

        # initialize super class
        tk.Text.__init__(self, self.fr, bg=self.bg, fg=self.fg, bd=self.bd, wrap=wrap, undo='false', **kwargs)
        self.grid(sticky='ewns')

        if self.vscroll:
            self.vbar = SimpleScrollbar(self.fr, orient='vertical', command=self.yview, slider_color=self.sbar_fg,
                                        bg=self.sbar_bg, width=vbar_width)
            self.vbar.grid(row=0, column=1, sticky='ns')
            self.config(yscrollcommand=self.vbar.set)

        if self.hscroll:
            self.hbar = SimpleScrollbar(self.fr, orient='horizontal', command=self.xview, slider_color=self.sbar_fg,
                                        bg=self.sbar_bg, width=hbar_width)
            self.hbar.grid(row=1, column=0, sticky='ew')
            self.config(xscrollcommand=self.hbar.set)

        # bind mouse wheel to scroll
        scroll_with_mousewheel(self)

        # use outer frame geometry managers
        self.pack = self.fr.pack
        self.pack_forget = self.fr.pack_forget

        self.grid = self.fr.grid
        self.grid_forget = self.fr.grid_forget
        self.grid_remove = self.fr.grid_remove

        self.place = self.fr.place
        self.place_forget = self.fr.place_forget

        # for compatibility
        self.text = self

    def set(self, text):
        """replace contents"""
        self.clear()

        if self.max_chars:
            count = len(text)
            if count > self.max_chars:
                delta = count - self.max_chars
                text = text[delta:]

        self.insert("1.0", text)

        self.scrolltobottom()

    def clear(self):
        """clear all Text widget contents"""
        self.delete("1.0", tk.END)

    def append(self, text, text_color=None, text_bg=None):
        """append text with arbitrary colors"""

        color_tags = []

        if text_color:
            self.tag_configure(text_color, foreground=text_color)
            color_tags.append(text_color)

        if text_bg:
            self.tag_configure(text_bg, foreground=text_bg)
            color_tags.append(text_bg)

        self.insert(tk.END, text, ','.join(color_tags))

        self.remove_extra_chars()

        self.scrolltobottom()

    def remove_extra_chars(self):
        """remove characters from beginning of Text widget if it exceeds max chars"""
        if self.max_chars:
            # get current text characters count
            count = len(self.get("1.0", tk.END))
            if count > self.max_chars:
                delta = count - self.max_chars
                self.delete("1.0", f"1.0 + {delta} chars")

    def scrolltobottom(self):
        """scroll to bottom if autoscroll enabled and scrollbar position at the bottom"""
        try:
            if self.autoscroll and self.vbar.get()[1] == 1:
                self.yview_moveto("1.0")
        except:
            pass 
