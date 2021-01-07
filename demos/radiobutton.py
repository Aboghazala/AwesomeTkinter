import tkinter as tk
from tkinter import ttk
import awesometkinter as atk

root = tk.Tk()
root.title('AwesomeTkinter')

# select tkinter theme required for things to be right on windows,
# only 'alt', 'default', or 'classic' can work fine on windows 10
s = ttk.Style()
s.theme_use('default')

f = tk.Frame(root, bg='white')
f.pack(expand=True, fill='both')

# radio buttons' variable
var = tk.StringVar()
var.set('test')

# lets print selection value
var.trace_add('write', lambda *args: print(var.get()))

# atk radiobutton, you can control indicator ring, fill, and mark color
atk.Radiobutton(f, text='AwesomeTkinter Radiobutton', variable=var).pack(padx=17, pady=10, anchor='w')
atk.Radiobutton(f, text='AwesomeTkinter Radiobutton, selected', value='test', variable=var).pack(padx=17, pady=10, anchor='w')

ttk.Separator(f).pack(expand=True, fill='x')

# standard tk button
tk.Radiobutton(f, text='standard tk Radiobutton', variable=var, value='standard tk Radiobutton', fg='black',
               bg='white').pack(padx=10, pady=10, anchor='w')
tk.Radiobutton(f, text='standard tk Radiobutton, selected', variable=var, value='test', bg='white',
               fg='black').pack(padx=10, pady=10, anchor='w')

ttk.Separator(f).pack(expand=True, fill='x')

# standard ttk Radiobutton
ttk.Radiobutton(f, text='standard ttk Radiobutton', variable=var).pack(padx=15, pady=10, anchor='w')
ttk.Radiobutton(f, text='standard ttk Radiobutton, selected', variable=var, value='test').pack(padx=15, pady=10, anchor='w')

ttk.Separator(f).pack(expand=True, fill='x')

# atk with custom colors
atk.Radiobutton(f, text='AwesomeTkinter Radiobutton, with custom colors', ind_bg='yellow', ind_outline_color='red',
                ind_mark_color='blue', variable=var, value='test').pack(padx=17, pady=10, anchor='w')
root.mainloop()

