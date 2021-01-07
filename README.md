AwesomeTkinter offers some pretty tkinter widgets  
These widgets are just a tkinter widgets with custom styles and images.

current available widgets:
- radial progressbar (flat or 3d).
- scrollable frames,
- 3d buttons,
- 3d frames.
- Scrollable text widget
- radiobutton with better indicator/check mark quality.
- simple scrollbar "without arrow heads"

new widgets are coming soon


# Screenshots:
![progressbar](https://user-images.githubusercontent.com/37757246/93717162-3c059b80-fb74-11ea-9998-00fc5ba82ca3.png)

[More Screenshots](https://github.com/Aboghazala/AwesomeTkinter/issues/1)

--------------------------------------------------------------------------------------------------------------------


# Applications examples that uses AwesomeTkinter:
- [PyIDM](https://github.com/pyIDM/PyIDM)

![PyIDM](https://user-images.githubusercontent.com/58998813/92564079-e4fcee00-f278-11ea-83e1-9a272bc06b0f.png)

# Installation:
`python pip install awesometkinter` on windows  
`python3 pip install awesometkinter` on linux

for quick test:
```
import awesometkinter as atk
atk.main()
```

or from terminal:
```
python3 -m awesometkinter
or just
awesometkinter
```
this will display a test window

# Requirements:
- minimum python version 3.6
- tkinter
- pillow >= 6.0.0

# Limitations:
- some widgets don't work well with all tkinter themes, it is recommended to 
  set tkinter theme to 'default', 'alt', or 'classic' for things to
  work fine, so after creating your root you should change
  theme like example below


# Example:
```
import tkinter as tk
from tkinter import ttk
import awesometkinter as atk

# our root
root = tk.Tk()
root.config(background=atk.DEFAULT_COLOR)

# it is recommended to select tkinter theme required for things to be right on windows,
# 'alt', 'default', or 'classic' work fine on windows
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

root.mainloop()
```

also, you can use a lot of useful functions that manipulate images, e.g.
to create a tkinter PhotoImage from a file but want to change its size
and color:
```
img = atk.create_image(fp='path to my image file', color='red', size=(150, 100))
```

# Documentations:
TBA

---
# Author:
Mahmoud Elshahat  
2020
