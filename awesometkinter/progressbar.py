"""
    AwesomeTkinter, a new tkinter widgets design using custom styles and images

    :copyright: (c) 2020-2021 by Mahmoud Elshahat.

"""

import tkinter as tk
from tkinter import ttk

if not __package__:
    __package__ = 'awesometkinter'

from .utils import *
from .images import *


class RadialProgressbar(tk.Frame):
    """create radial flat progressbar

    basically this is a ttk horizontal progressbar modified using custom style layout and images

    Example:
        bar = RadialProgressbar(frame1, size=150, fg='green')
        bar.grid(padx=10, pady=10)
        bar.start()
    """

    # class variables to be shared between objects
    styles = []  # hold all style names created for all objects
    imgs = {}  # imgs{"size":{"color": img}}  example: imgs{"100":{"red": img}}

    def __init__(self, parent, size=100, bg=None, fg='cyan', text_fg=None, text_bg=None, font=None, font_size_ratio=0.1,
                 base_img=None, indicator_img=None, parent_bg=None, **extra):
        """initialize progressbar

        Args:
            parent  (tkinter object): tkinter container, i.e. toplevel window or frame
            size (int or 2-tuple(int, int)) size of progressbar in pixels
            bg (str): color of base ring
            fg(str): color of indicator ring
            text_fg (str): percentage text color
            font (str): tkinter font for percentage text, e.g. 'any 20'
            font_size_ratio (float): font size to progressbar width ratio, e.g. for a progressbar size 100 pixels,
                                     a 0.1 ratio means font size 10
            base_img (tk.PhotoImage): base image for progressbar
            indicator_img (tk.PhotoImage): indicator image for progressbar
            parent_bg (str): color of parent container
            extra: any extra kwargs

        """

        self.parent = parent
        self.parent_bg = parent_bg or get_widget_attribute(self.parent, 'background')
        self.bg = bg or calc_contrast_color(self.parent_bg, 30)
        self.fg = fg
        self.text_fg = text_fg or calc_font_color(self.parent_bg)
        self.text_bg = text_bg or self.parent_bg
        self.size = size if isinstance(size, (list, tuple)) else (size, size)
        self.font_size_ratio = font_size_ratio
        self.font = font or f'any {int((sum(self.size) // 2) * self.font_size_ratio)}'

        self.base_img = base_img
        self.indicator_img = indicator_img

        self.var = tk.IntVar()

        # initialize super class
        tk.Frame.__init__(self, master=parent)

        # create custom progressbar style
        self.bar_style = self.create_style()

        # create tk Progressbar
        self.bar = ttk.Progressbar(self, orient='horizontal', mode='determinate', length=self.size[0],
                                   variable=self.var, style=self.bar_style)
        self.bar.pack()

        # percentage Label
        self.percent_label = ttk.Label(self.bar, text='0%')
        self.percent_label.place(relx=0.5, rely=0.5, anchor="center")

        # trace progressbar value to show in label
        self.var.trace_add('write', self.show_percentage)

        # set default attributes
        self.config(**extra)

        self.start = self.bar.start
        self.stop = self.bar.stop

    def set(self, value):
        """set and validate progressbar value"""
        value = self.validate_value(value)
        self.var.set(value)

    def get(self):
        """get validated progressbar value"""
        value = self.var.get()
        return self.validate_value(value)

    def validate_value(self, value):
        """validate progressbar value
        """

        try:
            value = int(value)
            if value < 0:
                value = 0
            elif value > 100:
                value = 100
        except:
            value = 0

        return value

    def create_style(self):
        """create ttk style for progressbar

        style name is unique and will be stored in class variable "styles"
        """

        # create unique style name
        bar_style = f'radial_progressbar_{len(RadialProgressbar.styles)}'

        # add to styles list
        RadialProgressbar.styles.append(bar_style)

        # create style object
        s = ttk.Style()

        RadialProgressbar.imgs.setdefault(self.size, {})
        self.indicator_img = self.indicator_img or RadialProgressbar.imgs[self.size].get(self.fg)
        self.base_img = self.base_img or RadialProgressbar.imgs[self.size].get(self.bg)

        if not self.indicator_img:
            img = create_circle(self.size, color=self.fg)
            self.indicator_img = ImageTk.PhotoImage(img)
            RadialProgressbar.imgs[self.size].update(**{self.fg: self.indicator_img})

        if not self.base_img:
            img = create_circle(self.size, color=self.bg)
            self.base_img = ImageTk.PhotoImage(img)
            RadialProgressbar.imgs[self.size].update(**{self.bg: self.base_img})

        # create elements
        indicator_element = f'top_img_{bar_style}'
        base_element = f'bottom_img_{bar_style}'

        try:
            s.element_create(base_element, 'image', self.base_img, border=0, padding=0)
        except:
            pass

        try:
            s.element_create(indicator_element, 'image', self.indicator_img, border=0, padding=0)
        except:
            pass

        # create style layout
        s.layout(bar_style,
                 [(base_element, {'children':
                        [('pbar', {'side': 'left', 'sticky': 'nsew', 'children':
                                [(indicator_element, {'sticky': 'nswe'})]})]})])

        # configure new style
        s.configure(bar_style, pbarrelief='flat', borderwidth=0, troughrelief='flat')

        return bar_style

    def show_percentage(self, *args):
        """display progressbar percentage in a label"""
        bar_value = self.get()
        self.percent_label.config(text=f'{bar_value}%')

    def config(self, **kwargs):
        """config widgets' parameters"""

        # create style object
        s = ttk.Style()

        kwargs = {k: v for k, v in kwargs.items() if v}
        self.__dict__.update(kwargs)

        # frame bg
        self['bg'] = self.parent_bg

        # bar style configure
        s.configure(self.bar_style, background=self.parent_bg, troughcolor=self.parent_bg)

        # percentage label
        self.percent_label.config(background=self.text_bg, foreground=self.text_fg, font=self.font)


class RadialProgressbar3d(RadialProgressbar):
    """create radial 3d progressbar

        basically this is a ttk horizontal progressbar modified by using custom style layout and images

        Example:
            bar = Radial3dProgressbar(root, size=150, fg='blue')
            bar.pack(padx=10, pady=10)
            bar.start()
        """
    imgs = {}  # imgs{"size":{"color": img}}  example: imgs{"100":{"red": img}}

    def __init__(self, parent, size=100, fg='cyan', text_bg = '#333', text_fg = 'white', **extra):
        """initialize progressbar

        Args:
            parent  (tkinter object): tkinter container, i.e. toplevel window or frame
            size (int or 2-tuple(int, int)) size of progressbar
            fg(str): color of indicator ring
            extra: any extra kwargs, e.g. font, font_size_ratio, etc... see parent class docs
        """

        RadialProgressbar3d.imgs.setdefault(size, {})
        base_img = RadialProgressbar3d.imgs[size].get('base')
        indicator_img = RadialProgressbar3d.imgs[size].get(fg)

        if not indicator_img:
            # create pillow images
            base_img = create_pil_image(b64=progressbar_3d_base)
            indicator_img = create_circle(size=84, thickness=4, color=fg)

            # change indicator color
            indicator_img = change_img_color(indicator_img, fg)

            # merge indicator ring with base image copy
            indicator_img = mix_images(base_img.copy(), indicator_img)

            # resize
            if self.size:
                base_img = resize_img(base_img, size)
                indicator_img = resize_img(indicator_img, size)

            # create tkinter images using pillow ImageTk
            indicator_img = ImageTk.PhotoImage(indicator_img)
            base_img = ImageTk.PhotoImage(base_img)

            # store images for future use
            RadialProgressbar3d.imgs[size].update(**{'base': base_img})
            RadialProgressbar3d.imgs[size].update(**{fg: indicator_img})

        kwargs = locals().copy()
        kwargs.update(**extra)
        kwargs.pop('self')
        kwargs.pop('extra')

        RadialProgressbar.__init__(self, **kwargs)


class Segmentbar(tk.Canvas):
    def __init__(self, master, bg=None, fg=None, width=100, height=10):
        self.master = master
        master_bg = get_widget_attribute(master, 'background')
        bg = bg or calc_contrast_color(master_bg, 30)
        self.fg = fg or calc_font_color(bg)
        self.bars = {}
        self.height = height
        self.width = width
        super().__init__(self.master, bg=bg, width=self.width, height=self.height, bd=0, highlightthickness=0)
        self.bind('<Configure>', self.redraw)

    def ubdate_bars(self, segments_progress):
        # segments_progress, e.g [total size, [(starting range, length), ...]]
        size = segments_progress[0]

        # scale values
        scale = size / self.width
        scaled_values = set()  # use set to filter repeated values
        for item in segments_progress[1]:
            start, length = item
            start = start // scale  # ignore fraction, e.g. 3.7 ====> 3.0
            length = length // scale + (1 if length % scale else 0)  # ceiling, eg: 3.2 ====> 4.0
            end = start + length

            start = int(start)
            end = int(end)

            scaled_values.add((start, end))

        for item in scaled_values:
            self.update_bar(item)

    def update_bar(self, info):
        """expecting a tuple or a list with the following structure
        (range-start, length, total-file-size)"""
        start, end = info

        tag_id = self.bars.get(start, None)
        if tag_id:
            x0, y0, x1, y1 = self.coords(tag_id)
            x1 = end
            self.coords(tag_id, x0, y0, x1, y1)
        else:
            tag_id = self.create_rectangle(start, 0, end, self.height, fill=self.fg, width=0)
            self.bars[start] = tag_id

        self.update_idletasks()

    def redraw(self, *args):
        # in case of window get resized by user
        scale = self.winfo_width() / self.width
        self.width = self.winfo_width()
        for tag_id in self.bars.values():
            x0, y0, x1, y1 = self.coords(tag_id)
            x0 *= scale
            x1 *= scale
            self.coords(tag_id, x0, y0, x1, y1)

        self.update_idletasks()


if __name__ == '__main__':
    root = tk.Tk()
    sb = Segmentbar(root, bg='grey', fg='black', width=200)
    sb.pack(fill='x', padx=10, pady=10)

    # segments_progress, e.g [total size, [(starting range, length), ...]]
    seg1 = [20, 0]
    seg2 = [100, 0]
    seg3 = [300, 15]

    def progress():
        sb.ubdate_bars([400, [seg1, seg2, seg3]])
        seg1[1] += 1
        seg2[1] += 1
        seg3[1] += 1

        if seg1[1] != 101:
            root.after(100, progress)

    progress()

    root.mainloop()
