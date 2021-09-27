"""
    AwesomeTkinter, a new tkinter widgets design using custom styles and images

    :copyright: (c) 2020-2021 by Mahmoud Elshahat.

"""

import tkinter as tk


class RightClickMenu(tk.Menu):
    """Context menu or right click menu popup"""

    def __init__(self, parent, menu_items, callback=None, bg='white', fg='black', abg='blue', afg='white',
                 bind_left_click=False, bind_right_click=True):
        """initialize
        Args:
            parent: tkinter widget to show this menu when right clicked
            menu_items (iterable): a list of entries / options to show in right click menu, to add a separator you can
                                   pass a string '---' as an item name
            callback (callable): any function or method that will be called when an option get selected,
                                 should expect option name as a positional argument
            bg: background color
            fg: text color
            abg: background color on mouse hover
            afg: text color on mouse hover
            bind_left_click: if true will bind left mouse click
            bind_right_click: if true will bind right mouse click

        Example:
            right_click_map = {'say hi': lambda x: print(x),  # x = 'say hi'
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

        self.parent = parent

        # prevent random selection if menu shows under mouse 
        self.pressflag = False

        def onpress(event):
            self.pressflag = True

        def onrelease(event):
            # diable mouse release action if no mouse press
            if not self.pressflag:
                return 'break'
            else:
                self.pressflag = False

        trigger_buttons = []
        if bind_left_click:
            trigger_buttons.append(1)
        if bind_right_click:
            trigger_buttons += [2, 3]

        for i in trigger_buttons:
            parent.bind(f"<Button-{i}>", self.popup, add='+')
            self.bind(f'<{i}>', onpress, add='+')
            self.bind(f'<ButtonRelease-{i}>', onrelease, add='+')

    def popup(self, event):
        """show right click menu"""
        x, y = event.x_root, event.y_root
        self.tk_popup(x, y)

    def context_menu_handler(self, option):
        """handle selected option

        Args:
            option (str): selected option
        """

        if callable(self.callback):
            self.callback(option)
