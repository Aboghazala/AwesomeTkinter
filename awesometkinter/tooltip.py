"""
    AwesomeTkinter, a new tkinter widgets design using custom styles and images

    :copyright: (c) 2020-2021 by Mahmoud Elshahat.

    Description:
        tooltip popup window for tkinter widgets on mouse hover
        some parts inspired from https://svn.python.org/projects/python/trunk/Lib/idlelib/ToolTip.py

"""

import tkinter as tk

__package__ = 'awesometkinter'


class ToolTip(tk.Menu):

    def __init__(self, widget, text, waittime=500, xoffset=10, yoffset=10, bg="#ffffe0", fg='black', **kwargs):
        """
        tooltip class

        Args:
            widget: any tkinter widget
            text: tooltip text
            waittime: time in milliseconds to wait before showing tooltip
            xoffset(int): x - offset (pixels) of tooltip box from mouse pointer
            yoffset(int): y - offset (pixels) of tooltip box from mouse pointer
        """

        self.widget = widget
        tk.Menu.__init__(self, widget, tearoff=0, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, relief='flat')
        self.add_command(label=text, hidemargin=True)

        self.text = text
        self.waittime = waittime  # milliseconds
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.id = None

        self._id1 = self.widget.bind("<Enter>", self.enter, add='+')
        self._id2 = self.widget.bind("<Leave>", self.leave, add='+')
        self._id3 = self.widget.bind("<ButtonPress>", self.leave, add='+')

        # for compatibility, to be removed in future
        widget.update_tooltip = self.update_tooltip
        widget.tooltip = self

    def __del__(self):
        try:
            self.unpost()
            self.widget.unbind("<Enter>", self._id1)
            self.widget.unbind("<Leave>", self._id2)
            self.widget.unbind("<ButtonPress>", self._id3)
            self.unschedule()
            self.hidetip()
        except tk.TclError:
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
        if not self.winfo_viewable():
            # tip text should be displayed away from the mouse pointer to prevent triggering leave event
            x = self.widget.winfo_pointerx() + self.xoffset
            y = self.widget.winfo_pointery() + self.yoffset
            self.update_tooltip(self.text)
            self.post(x, y)

    def hidetip(self):
        if self.winfo_viewable():
            self.unpost()

    def update_tooltip(self, text):
        self.text = text
        try:
            self.entryconfigure(0, label=text, hidemargin=True)
        except:
            pass


tooltip = ToolTip


def main():
    # Test code
    root = tk.Tk()
    b = tk.Button(root, text="Hello", command=root.destroy)
    b.pack()
    l = tk.Label(root, text='my label')
    l.pack()
    b.tp = tooltip(b, "Hello world")
    l.tp = tooltip(l, "Hello world")

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


if __name__ == '__main__':
    main()
