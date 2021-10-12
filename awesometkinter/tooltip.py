"""
    AwesomeTkinter, a new tkinter widgets design using custom styles and images

    :copyright: (c) 2020-2021 by Mahmoud Elshahat.

    Description:
        tooltip popup window for tkinter widgets on mouse hover
        some parts inspired from https://svn.python.org/projects/python/trunk/Lib/idlelib/ToolTip.py

"""

import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk

__package__ = 'awesometkinter'

from .utils import configure_widget


class ToolTip:

    def __init__(self, widget, text, waittime=500, xoffset=10, yoffset=10, **kwargs):
        """
        tooltip class

        Args:
            widget: any tkinter widget
            text: tooltip text
            waittime: time in milliseconds to wait before showing tooltip
            xoffset(int): x - offset (pixels) of tooltip box from mouse pointer
            yoffset(int): y - offset (pixels) of tooltip box from mouse pointer
            kwargs: parameters to be passed to tooltip label, e.g: , background='red', foreground='blue', etc

        """
        self.widget = widget
        self._text = text
        self.waittime = waittime  # milliseconds
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.kwargs = kwargs
        self.tipwindow = None
        self.label = None
        self.id = None
        self._id1 = self.widget.bind("<Enter>", self.enter, add='+')
        self._id2 = self.widget.bind("<Leave>", self.leave, add='+')
        self._id3 = self.widget.bind("<ButtonPress>", self.leave, add='+')

        # for dynamic tooltip, use widget.update_tooltip('new text')
        widget.update_tooltip = self.update_tooltip

        widget.tooltip = self

    def __del__(self):
        try:
            self.widget.unbind("<Enter>", self._id1)
            self.widget.unbind("<Leave>", self._id2)
            self.widget.unbind("<ButtonPress>", self._id3)
            self.unschedule()
            self.hidetip()
        except tk.TclError:
            pass

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, txt):
        self._text = txt
        self.update_tooltip(txt)

    def update_tooltip(self, text):
        self._text = text
        try:
            self.label.config(text=text)
        except:
            pass

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None

    def showtip(self):
        if self.tipwindow:
            return

        # tip text should be displayed away from the mouse pointer to prevent triggering leave event
        x = self.widget.winfo_pointerx() + self.xoffset
        y = self.widget.winfo_pointery() + self.yoffset

        self.tipwindow = tw = tk.Toplevel(self.widget)

        # show no border on the top level window
        tw.wm_overrideredirect(1)

        self.label = ttk.Label(tw, text=self.text, justify=tk.LEFT, padding=(5, 2),
                               background="#ffffe0", relief=tk.SOLID, borderwidth=1)

        lbl = self.label
        self.kwargs['background'] = self.kwargs.get('background') or self.kwargs.get('bg') or "#ffffe0"
        self.kwargs['foreground'] = self.kwargs.get('foreground') or self.kwargs.get('fg') or "black"
        configure_widget(lbl, **self.kwargs)

        # get text width using font, because .winfo_width() needs to call "update_idletasks()" to get correct width
        font = tkfont.Font(font=lbl['font'])
        txt_width = font.measure(self.text)

        # correct position to stay inside screen
        x = min(x, lbl.winfo_screenwidth() - txt_width)

        tw.wm_geometry("+%d+%d" % (x, y))
        lbl.pack()

    def hidetip(self):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None


tooltip = ToolTip


def main():
    # Test code
    root = tk.Tk()
    b = tk.Button(root, text="Hello", command=root.destroy)
    b.pack()
    l = tk.Label(root, text='my label')
    l.pack()
    b.tp = tooltip(b, "Hello world")
    l.tp = tooltip(l, "Hello world", bg='cyan', fg='blue')

    # we can modify any property thru the widget.tooltip reference
    b.tp.waittime = 100
    b.tp.text = 'new text'

    # use dynamic tooltip
    x = list(range(20))

    def foo():
        if x:
            l.tp.update_tooltip(f'counter: {x.pop()}')  # or can use l.tp.text='some text'
            root.after(1000, foo)

    foo()

    root.mainloop()


x = 0


def main():
    root = tk.Tk()
    btn = tk.Button(root, text="Hello", command=root.destroy)
    btn.pack()
    lbl = tk.Label(root, text='my label')
    lbl.pack()
    btn.tp = tooltip(btn, "Hello world")
    lbl.tp = tooltip(lbl, "Hello world")

    # we can modify any property thru the widget.tooltip reference
    btn.tp.waittime = 100
    btn.tp.text = 'new text'

    # Also we can dynamically change tooltip as follows:
    lbl.counter = 0

    def foo():
        # change tooltip every second to mimic progress
        lbl.counter = lbl.counter + 1 if lbl.counter < 100 else 0
        lbl.tp.update_tooltip('Progress: ' + str(lbl.counter) + '%')  # or use l.tp.text='some text'
        root.after(1000, foo)

    foo()

    root.mainloop()


if __name__ == '__main__':
    main()
