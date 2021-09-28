AwesomeTkinter offers some pretty tkinter widgets  
These widgets are just a tkinter widgets with custom styles and images.

![progressbar](https://user-images.githubusercontent.com/37757246/93717162-3c059b80-fb74-11ea-9998-00fc5ba82ca3.png)

[More Screenshots](https://github.com/Aboghazala/AwesomeTkinter/issues/1)

current available widgets:
- radial progressbar (flat or 3d).
- scrollable frames,
- 3d buttons,
- 3d frames.
- Scrollable text widget
- radiobutton with better indicator/check mark quality.
- simple scrollbar "without arrow heads"
- tooltip

new widgets are coming soon

# bidi support on Linux:

Added support to bidi language e.g. Arabic to be shown properly in tkinter widgets (on linux), see example below
![progressbar](https://user-images.githubusercontent.com/37757246/117579022-63a07880-b0f1-11eb-8295-66942fec4025.png)

```
import tkinter as tk
from awesometkinter.bidirender import add_bidi_support, render_text
root = tk.Tk()

text = 'السلام عليكم'

# text display incorrectly on linux without bidi support
dummyvar = tk.StringVar()
dummyvar.set(text)
tk.Label(root, textvariable=dummyvar, font='any 20').pack()

# uncomment below to set a rendered text to first label
# dummyvar.set(render_text(text))

entry = tk.Entry(root, font='any 20', justify='right')
entry.pack()

lbl = tk.Label(root, font='any 20')
lbl.pack()

# adding bidi support for widgets
add_bidi_support(lbl)
add_bidi_support(entry)

# now there is a new set() and get() methods to set and get text on a widget
entry.set(text)
lbl.set('هذا كتاب adventure شيق')

root.mainloop()
```


--------------------------------------------------------------------------------------------------------------------


# Applications examples that uses AwesomeTkinter:
- [FireDM](https://github.com/firedm/FireDM)

![FireDM](https://user-images.githubusercontent.com/58998813/112715559-83852f80-8ee9-11eb-8ea3-d8c0f98a0153.png)

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

atk.Button3d(f2, text='Button2').pack(pady=10)

root.mainloop()
```

# ToolTip

you can enable tooltip for tkinter widgets on mouse hover, signature and arguments like below

```python
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

```

Tooltip Example:

```python
import tkinter as tk
import awesometkinter as atk

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

# Also we can dynamically change tooltip as follows:
x = 0
def foo():
    # change tooltip every second to mimic progress
    global x
    x += 1
    l.tp.update_tooltip('Progress: ' + str(x) + '%')  # or use l.tp.text='some text'
    root.after(1000, foo)

foo()

root.mainloop()

```

also, you can use a lot of useful functions that manipulate images, e.g.
to create a tkinter PhotoImage from a file but want to change its size
and color:
```
img = atk.create_image(fp='path to my image file', color='red', size=(150, 100))
```

# Demos:
https://github.com/Aboghazala/AwesomeTkinter/tree/master/demos

---
# Author:
Mahmoud Elshahat  
2020-2021
