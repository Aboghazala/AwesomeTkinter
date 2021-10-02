"""
    AwesomeTkinter, a new tkinter widgets design using custom styles and images

    :copyright: (c) 2020-2021 by Mahmoud Elshahat.

"""

import tkinter as tk
from tkinter import font as tkfont


class AutoWrappingLabel(tk.Label):
    """auto-wrapping label
    wrap text based on widget changing size
    """

    def __init__(self, parent=None, justify='left', anchor='w', **kwargs):
        tk.Label.__init__(self, parent, justify=justify, anchor=anchor, **kwargs)
        self.bind('<Configure>', lambda event: self.config(wraplength=self.winfo_width()))


class AutofitLabel(tk.Label):
    """label that fit contents by using 3 dots in place of truncated text
    should be autoresizable, e.g. packed with expand=True and fill='x', or grid with sticky='ew'
    """

    def __init__(self, parent=None, justify='left', anchor='w', refresh_time=500, **kwargs):
        self.refresh_time = refresh_time
        tk.Label.__init__(self, parent, justify=justify, anchor=anchor, **kwargs)
        self.original_text = ''
        self.id = None
        self.bind('<Configure>', self.schedule)

    def schedule(self, *args):
        self.unschedule()
        self.id = self.after(self.refresh_time, self.update_text)

    def unschedule(self):
        if self.id:
            self.after_cancel(self.id)
            self.id = None

    def update_text(self, *args):
        txt = self.original_text or self['text']
        self.original_text = txt
        width = self.winfo_width()
        font = tkfont.Font(font=self['font'])
        txt_width = font.measure(txt)

        if txt_width > width:
            for i in range(0, len(txt), 2):
                num = len(txt) - i
                slice = num // 2
                new_txt = txt[0:slice] + ' ... ' + txt[-slice:]
                if font.measure(new_txt) < width:
                    self['text'] = new_txt
                    break
        else:
            self['text'] = self.original_text


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('400x200')

    txt = ', '.join([str(x) for x in range(1, 31)])
    tk.Label(root, text=txt, bg='green').pack(fill='x', padx=5)
    AutoWrappingLabel(root, text=txt, bg='yellow').pack(fill='x', padx=5)
    AutofitLabel(root, text=txt, bg='grey', refresh_time=200).pack(fill='x', padx=5)
    root.mainloop()
