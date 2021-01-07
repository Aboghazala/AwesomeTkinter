"""
    AwesomeTkinter, a new tkinter widgets design using custom styles and images

    :copyright: (c) 2020 by Mahmoud Elshahat.

"""

import tkinter as tk


class RightClickMenu(tk.Menu):
    """Context menu or right click menu popup"""
    def __init__(self, parent, menu_items, callback=None, bg='white', fg='black', abg='blue', afg='white'):
        """initialize
        Args:
            parent: tkinter widget to show this menu when right clicked
            menu_items (iterable): a list of entries / options to show in right click menu, to add a separator you can
                                   pass a string '---' as an item name
            callback (callable): any function or method that will be called when an option get selected,
                                 should expect option name as an argument
            bg: background color
            fg: text color
            abg: background color on mouse hover
            afg: text color on mouse hover

        Example:
            right_click_map = {'say hi': lambda: print('hiiii'),
                               'help': show_help,
                               'blah blah': blah_callback,
                               }

            RightClickMenu(my_listbox, right_click_map.keys(),
                           callback=lambda option: right_click_map[option](),
                           bg='white', fg='black', abg=blue, afg='white')
        """
        self.callback = callback

        # initialize super
        tk.Menu.__init__(self, parent, tearoff=0, bg=bg, fg=fg, activebackground=abg, activeforeground=afg)

        for option in menu_items:
            if option == '---':
                self.add_separator()
            else:
                self.add_command(label=f' {option}', command=lambda x=option: self.context_menu_handler(x))

        parent.bind("<Button-3>", self.popup)
        parent.bind("<Button-2>", self.popup)

    def popup(self, event):
        self.tk_popup(event.x_root, event.y_root)

    def context_menu_handler(self, option):
        """handle selected option

        Args:
            option (str): selected option
        """

        if callable(self.callback):
            self.callback(option)

        else:
            print(f'{option}, selected, you should assign callback to handle selection') 
