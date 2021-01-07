import tkinter as tk
from tkinter import ttk
import awesometkinter as atk

# our root
root = tk.Tk()
root.config(background=atk.DEFAULT_COLOR)

# select tkinter theme required for things to be right on windows,
# only 'alt', 'default', or 'classic' can work fine on windows 10
s = ttk.Style()
s.theme_use('default')

# 3d frame
f1 = atk.Frame3d(root)
f1.pack(side='left', expand=True, fill='both', padx=3, pady=3)

# 3d progressbar
bar = atk.RadialProgressbar3d(f1, fg='cyan', size=120)
bar.pack(padx=20, pady=20)
bar.start()

# 3d button
atk.Button3d(f1, text='3D Button').pack(pady=10)

f2 = atk.Frame3d(root)
f2.pack(side='left', expand=True, fill='both', padx=3, pady=3)

# flat radial progressbar
bar = atk.RadialProgressbar(f2, fg='green')
bar.pack(padx=30, pady=30)
bar.start()

atk.Button3d(f2, text='Pressed Button').pack(pady=10)

f3 = atk.Frame3d(root)
f3.pack(side='left', expand=True, fill='both', padx=3, pady=3)

atk.Radiobutton(f3, text="Radiobutton 1").pack(padx=20, pady=(20, 5))
atk.Radiobutton(f3, text="Radiobutton 2", ind_outline_color='white', ind_bg='yellow',
                ind_mark_color='red').pack(padx=20, pady=5)

atk.Checkbutton(f3, text=" Checkbutton 1", check_mark_color='red', size=12).pack(padx=20, pady=(20, 5))
atk.Checkbutton(f3, text=" Checkbutton 2").pack(padx=20, pady=5)


root.mainloop()
