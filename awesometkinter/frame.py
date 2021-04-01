"""
    AwesomeTkinter, a new tkinter widgets design using custom styles and images

    :copyright: (c) 2020-2021 by Mahmoud Elshahat.

"""

import tkinter as tk
from tkinter import ttk
from .utils import *
from .config import *
from .images import *
from .scrollbar import SimpleScrollbar


class ScrollableFrame(tk.Frame):
    """A frame with scrollbars
    inspired by : https://stackoverflow.com/a/3092341
    basically it is a frame inside a canvas inside another frame

    usage:
        frame = ScrollableFrame(root)
        frame.pack(fill='both', expand=True)

        # add your widgets normally
        tk.Label(frame, text=hello).pack()
    """

    def __init__(self, parent, vscroll=True, hscroll=True, autoscroll=False, bg=None, sbar_fg=None, sbar_bg=None,
                 vbar_width=10, hbar_width=10):
        """initialize

        Args:
            parent (tk.Widget): tkinter master widget
            vscroll (bool): use vertical scrollbar
            hscroll (bool): use horizontal scrollbar
            autoscroll (bool): auto scroll to bottom if new items added to frame
            bg (str): background
            sbar_fg (str): color of scrollbars' slider
            sbar_bg (str): color of scrollbars' trough, default to frame's background
            vbar_width (int): vertical scrollbar width
            hbar_width (int): horizontal scrollbar width
        """
        self.autoscroll = autoscroll
        self.current_height = None

        sbar_bg = sbar_bg or 'white'
        sbar_fg = sbar_fg or 'blue'

        # create outside frame
        self.outer_frame = tk.Frame(parent, bg=bg)

        # create canvas
        self.canvas = tk.Canvas(self.outer_frame, borderwidth=0, highlightthickness=0, background=bg)

        # initialize super class
        tk.Frame.__init__(self, self.canvas, bg=bg)

        # scrollbars
        if vscroll:
            self.vsb = SimpleScrollbar(self.outer_frame, orient="vertical", command=self.canvas.yview, bg=sbar_bg,
                                       slider_color=sbar_fg, width=vbar_width)
            self.canvas.configure(yscrollcommand=self.vsb.set)

            self.vsb.pack(side="right", fill="y")
        if hscroll:
            self.hsb = SimpleScrollbar(self.outer_frame, orient="horizontal", command=self.canvas.xview, bg=sbar_bg,
                                       slider_color=sbar_fg, width=hbar_width)
            self.canvas.configure(xscrollcommand=self.hsb.set)

            self.hsb.pack(side="bottom", fill="x")

        self.canvas.pack(side="left", fill="both", expand=True)

        self._id = self.canvas.create_window((0, 0), window=self, anchor="nw", tags="self")

        self.bind("<Configure>", self._on_self_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # scroll with mousewheel
        scroll_with_mousewheel(self, target=self.canvas)

        # use outer frame geometry managers
        self.pack = self.outer_frame.pack
        self.pack_forget = self.outer_frame.pack_forget

        self.grid = self.outer_frame.grid
        self.grid_forget = self.outer_frame.grid_forget
        self.grid_remove = self.outer_frame.grid_remove

        self.place = self.outer_frame.place
        self.place_forget = self.outer_frame.place_forget

        # get scroll methods from canvas
        self.yview_scroll = self.canvas.yview_scroll
        self.xview_scroll = self.canvas.xview_scroll
        self.yview_moveto = self.canvas.yview_moveto
        self.xview_moveto = self.canvas.xview_moveto

    def _on_self_configure(self, event):
        """Reset the scroll region to match contents"""
        if self.winfo_height() != self.current_height:
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

            # scroll to bottom, if new widgets added to frame
            if self.autoscroll:
                self.scrolltobottom()

            self.current_height = self.winfo_height()

    def _on_canvas_configure(self, event):
        """expand self to fill canvas"""
        self.canvas.itemconfigure(self._id, width=self.canvas.winfo_width())

    def vscroll(self, fraction):
        """scroll canvas vertically

        Args:
            fraction (float): from 0 "top" to 1.0 "bottom"
        """

        self.canvas.yview_moveto(fraction)

    def scrolltobottom(self):
        self.vscroll(1.0)

    def scrolltotop(self):
        self.vscroll(0)

    def hscroll(self, fraction):
        """scroll canvas horizontally

        Args:
            fraction (float): from 0 "left" to 1.0 "right"
        """

        self.canvas.xview_moveto(fraction)


class Frame3d(ttk.Frame):
    """create a frame with 3d background color and shadow"""
    styles = []

    def __init__(self, parent, bg=None, **options):
        """initialize

        Args:
            parent: tkinter container widget, i.e. root or another frame
            bg (str): color of frame
        """
        self.bg = bg or DEFAULT_COLOR
        parent_color = get_widget_attribute(parent, 'background') or DEFAULT_COLOR

        # initialize super class
        ttk.Frame.__init__(self, parent, **options)

        # create unique style name based on frame color
        frame_style = f'Frame3d_{generate_unique_name(color_to_rgba(self.bg))}'

        # create style
        if frame_style not in Frame3d.styles:

            self.img = self.create_image()

            # create elements
            s = ttk.Style()
            element_style = f'{frame_style}_element'
            s.element_create(element_style, 'image', self.img, border=15, sticky="nsew")
            s.layout(frame_style, [(element_style, {"sticky": "nsew"})])
            s.map(frame_style, background=[('', parent_color)])

            # add to styles
            Frame3d.styles.append(frame_style)

        self['style'] = frame_style

    def create_image(self):

        shadow_img = create_pil_image(b64=btn_base)
        img = create_pil_image(b64=btn_face, color=self.bg)

        # merge face with base image
        img = mix_images(shadow_img, img)

        return ImageTk.PhotoImage(img) 
