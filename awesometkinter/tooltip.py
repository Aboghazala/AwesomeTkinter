"""
    AwesomeTkinter, a new tkinter widgets design using custom styles and images

    :copyright: (c) 2020-2021 by Mahmoud Elshahat.

    Description:
        tooltip popup window for tkinter widgets on mouse hover
        based on code from https://svn.python.org/projects/python/trunk/Lib/idlelib/ToolTip.py

        original author notes:
            general purpose 'tooltip' routines - currently unused in idlefork
            (although the 'calltips' extension is partly based on this code)
            may be useful for some purposes in (or almost in ;) the current project scope
            Ideas gleaned from PySol

"""


import tkinter as tk
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
        self.text = text
        self.waittime = waittime  # milliseconds
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.kwargs = kwargs
        self.tipwindow = None
        self.id = None
        self.label = None
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

    def update_tooltip(self, text):
        self.text = text
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
        # The tip window must be completely outside the widget;
        # otherwise when the mouse enters the tip window we get
        # a leave event and it disappears, and then we get an enter
        # event and it reappears, and so on forever :-(
        # x = self.widget.winfo_rootx() + 20
        # y = self.widget.winfo_rooty() + self.widget.winfo_height() + 1

        # or show it under mouse position with offset
        x = self.widget.winfo_pointerx() + self.xoffset
        y = self.widget.winfo_pointery() + self.yoffset

        self.tipwindow = tw = tk.Toplevel(self.widget)
    
        # show no border on the top level window
        tw.wm_overrideredirect(1)

        tw.wm_geometry("+%d+%d" % (x, y))
 
        self.label = ttk.Label(self.tipwindow, text=self.text, justify=tk.LEFT, padding=(5, 2),
                          background="#ffffe0", relief=tk.SOLID, borderwidth=1)

        configure_widget(self.label, **self.kwargs)
        self.label.pack()


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
    tooltip(b, "Hello world")

    # we can modify any property thru the widget.tooltip reference
    # b.tooltip.waittime = 2000
    # b.tooltip.text= 'new text'

    root.mainloop()

if __name__ == '__main__':
    main()