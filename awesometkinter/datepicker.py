"""
    AwesomeTkinter, a new tkinter widgets design using custom styles and images

    :copyright: (c) 2020-2021 by Mahmoud Elshahat.

"""

import datetime
import tkinter as tk
from tkinter import ttk

if not __package__:
    __package__ = 'awesometkinter'

from .utils import *


class DatePicker(tk.Toplevel):
    """Date picker window"""

    def __init__(self, master, min_year=None, max_year=None, year=None, month=None, day=None, hour=None, minute=None,
                 title='Date Picker', bg=None, fg=None, sbg=None,
                 btnbg=None, btnfg=None, width=420, height=180):
        """initialize

        Args:
            parent: parent window
            min_year (int): minimum year to show
            max_year (int): max. year to show
            year, month, day, hour, minute (int): set selected time
            title (str): window title
        """
        self.master = master
        master_bg = get_widget_attribute(master, 'background')
        self.bg = bg or calc_contrast_color(master_bg, 30)
        self.fg = fg or calc_font_color(self.bg)
        self.sbg = sbg or fg
        self.btnbg = btnbg or self.sbg
        self.btnfg = btnfg or calc_font_color(self.btnbg)

        today = datetime.datetime.today()
        year = year or today.year
        min_year = min_year or year - 100
        max_year = max_year or year + 100
        month = month or today.month
        day = day or today.day
        hour = hour or today.hour
        minute = minute or today.minute

        self.selected_date = None

        self.fields = {'Year': {'values': list(range(min_year, max_year + 1)), 'selection': year},
                       'Month': {'values': list(range(1, 13)), 'selection': month},
                       'Day': {'values': list(range(1, 32)), 'selection': day},
                       'Hour': {'values': list(range(0, 24)), 'selection': hour},
                       'Minute': {'values': list(range(0, 60)), 'selection': minute},
                       }

        # initialize super
        tk.Toplevel.__init__(self, self.master)

        # bind window close
        center_window(self, width=width, height=height, reference=self.master)

        self.title(title)
        self.config(bg=self.sbg)

        self.create_widgets()

        self.wait_window(self)

    def is_leap(self, year):
        """year -> 1 if leap year, else 0, source: datetime.py"""
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def days_in_month(self, year, month):
        """year, month -> number of days in that month in that year, modified from source: datetime.py"""
        default = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        if month == 2 and self.is_leap(year):
            return 29
        return default[month]

    def create_widgets(self):
        bg = self.bg
        fg = self.fg
        sbg = self.sbg
        btnbg = self.btnbg
        btnfg = self.btnfg
        main_frame = tk.Frame(self, bg=bg)
        top_frame = tk.Frame(main_frame, bg=bg)
        tk.Label(top_frame, text='Select Date and time:', bg=bg, fg=fg).pack(side='left', padx=5, pady=5)

        middle_frame = tk.Frame(main_frame, bg=bg)

        def set_field(field_name, value):
            x = self.fields[field_name]
            x['selection'] = int(value)

            # set correct days according to month and year
            year = self.fields['Year']['selection']
            month = self.fields['Month']['selection']
            day = self.fields['Day']['selection']
            days_in_month = self.days_in_month(year, month)
            day_combo.config(values=list(range(1, days_in_month + 1)))
            if day > days_in_month:
                corrected_value = days_in_month
                day_combo.set(corrected_value)
                self.fields['Day']['selection'] = corrected_value

        # style
        s = ttk.Style()
        custom_style = 'custom.TCombobox'
        # combobox consists of a text area, down arrow, and dropdown menu (listbox)
        # arrow: arrowcolor, background
        # text area: foreground, fieldbackground
        arrow_bg = sbg
        textarea_bg = btnbg
        s.configure(custom_style, arrowcolor=calc_font_color(arrow_bg),
                    foreground=calc_font_color(textarea_bg), padding=4, relief=tk.RAISED)
        s.map(custom_style, fieldbackground=[('', textarea_bg)], background=[('', arrow_bg)])

        def on_selection(event):
            widget = event.widget
            widget.selection_clear()

            widget.callback()

        c = 0
        for key, item in self.fields.items():
            tk.Label(middle_frame, text=key, bg=bg, fg=fg).grid(row=0, column=c, padx=5, sticky='w')
            cb = ttk.Combobox(middle_frame, state="readonly", values=item['values'], style=custom_style, width=5)
            cb.set(item['selection'])
            cb.grid(row=1, column=c, padx=(5, 10), sticky='w')
            cb.callback = lambda field_name=key, combo=cb: set_field(field_name, combo.get())
            cb.bind('<<ComboboxSelected>>', on_selection)

            # get day combo box reference
            if key == 'Day':
                day_combo = cb

            c += 1

        bottom_frame = tk.Frame(main_frame, bg=bg)
        tk.Button(bottom_frame, text='Cancel', command=self.close, bg=btnbg, fg=btnfg).pack(side='right', padx=5)
        tk.Button(bottom_frame, text='Ok', command=self.set_selection, bg=btnbg, fg=btnfg).pack(side='right')

        main_frame.pack(expand=True, fill='both', padx=(10, 0), pady=(10, 0))
        bottom_frame.pack(side='bottom', fill='x', pady=5)
        ttk.Separator(main_frame).pack(side='bottom', fill='x', expand=True)
        middle_frame.pack(side='bottom', expand=True, fill='both')
        ttk.Separator(main_frame).pack(side='bottom', fill='x', expand=True)
        top_frame.pack(side='bottom', fill='x')

    def close(self):
        self.destroy()

    def set_selection(self):
        """return selected date"""
        values = [int(item['selection']) for item in self.fields.values()]
        self.selected_date = datetime.datetime(*values)
        self.close()


if __name__ == '__main__':
    root = tk.Tk()

    def foo():
        dp = DatePicker(root, year=1900, day=23, hour=18, bg='white', fg='black')
        print(dp.selected_date)

    tk.Button(root, text='select date', command=foo).pack()
    root.mainloop()
