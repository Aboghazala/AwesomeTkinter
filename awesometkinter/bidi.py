"""
    AwesomeTkinter, a new tkinter widgets design using custom styles and images

    :copyright: (c) 2020-2021 by Mahmoud Elshahat.

    module description:
        handle arabic text to be shown properly in tkinter widgets (on linux)

"""

import tkinter as tk
import pyfribidi
import re


def hex2int(hcode):
    try:
        return int(hcode, 16)
    except:
        return None


arabic_ranges_pattern = r'[\u0600-\u06FF]|[\u0750-\u077F]|[\uFB50-\uFDFF]|[\uFE70-\uFEFF]'

# Arabic letters forms: base, isolated, end, middle, beginning
chars = [
    ['0627', 'fe8d', 'fe8e', '', ''],  # ['ا', 'ﺍ', 'ﺎ']
    ['0623', 'fe83', 'fe84', '', ''],  # ['ﺃ', 'ﺃ', 'ﺄ']
    ['0625', 'fe87', 'fe88', '', ''],  # ['ﺇ', 'ﺇ', 'ﺈ']
    ['0622', 'fe81', 'fe82', '', ''],  # ['آ', 'ﺁ', 'ﺂ']
    ['0624', 'fe85', 'fe86', '', ''],  # ['ﺅ', 'ﺅ', 'ﺆ']
    ['0626', 'fe89', 'fe8a', 'fe8c', 'fe8b'],  # ['ﺉ', 'ﺉ', 'ﺊ', 'ﺌ', 'ﺋ']
    ['0628', 'fe8f', 'fe90', 'fe92', 'fe91'],  # ['ب', 'ﺏ', 'ﺐ', 'ﺒ', 'ﺑ']
    ['062a', 'fe95', 'fe96', 'fe98', 'fe97'],  # ['ت', 'ﺕ', 'ﺖ', 'ﺘ', 'ﺗ']
    ['062b', 'fe99', 'fe9a', 'fe9c', 'fe9b'],  # ['ث', 'ﺙ', 'ﺚ', 'ﺜ', 'ﺛ']
    ['062c', 'fe9d', 'fe9e', 'fea0', 'fe9f'],  # ['ج', 'ﺝ', 'ﺞ', 'ﺠ', 'ﺟ']
    ['062d', 'fea1', 'fea2', 'fea4', 'fea3'],  # ['ح', 'ﺡ', 'ﺢ', 'ﺤ', 'ﺣ']
    ['062e', 'fea5', 'fea6', 'fea8', 'fea7'],  # ['خ', 'ﺥ', 'ﺦ', 'ﺨ', 'ﺧ']
    ['062f', 'fea9', 'feaa', '', ''],  # ['د', 'ﺩ', 'ﺪ']
    ['0630', 'feab', 'feac', '', ''],  # ['ذ', 'ﺫ', 'ﺬ']
    ['0631', 'fead', 'feae', '', ''],  # ['ر', 'ﺭ', 'ﺮ'
    ['0632', 'feaf', 'feb0', '', ''],  # ['ز', 'ﺯ', 'ﺰ']
    ['0633', 'feb1', 'feb2', 'feb4', 'feb3'],  # ['س', 'ﺱ', 'ﺲ', 'ﺴ', 'ﺳ']
    ['0634', 'feb5', 'feb6', 'feb8', 'feb7'],  # ['ش', 'ﺵ', 'ﺶ', 'ﺸ', 'ﺷ']
    ['0635', 'feb9', 'feba', 'febc', 'febb'],  # ['ص', 'ﺹ', 'ﺺ', 'ﺼ', 'ﺻ']
    ['0636', 'febd', 'febe', 'fec0', 'febf'],  # ['ض', 'ﺽ', 'ﺾ', 'ﻀ', 'ﺿ']
    ['0637', 'fec1', 'fec2', 'fec4', 'fec3'],  # ['ط', 'ﻁ', 'ﻂ', 'ﻄ', 'ﻃ']
    ['0638', 'fec5', 'fec6', 'fec8', 'fec7'],  # ['ظ', 'ﻅ', 'ﻆ', 'ﻈ', 'ﻇ']
    ['0639', 'fec9', 'feca', 'fecc', 'fecb'],  # ['ع', 'ﻉ', 'ﻊ', 'ﻌ', 'ﻋ']
    ['063a', 'fecd', 'fece', 'fed0', 'fecf'],  # ['غ', 'ﻍ', 'ﻎ', 'ﻐ', 'ﻏ']
    ['0641', 'fed1', 'fed2', 'fed4', 'fed3'],  # ['ف', 'ﻑ', 'ﻒ', 'ﻔ', 'ﻓ']
    ['0642', 'fed5', 'fed6', 'fed8', 'fed7'],  # ['ق', 'ﻕ', 'ﻖ', 'ﻘ', 'ﻗ']
    ['0643', 'fed9', 'feda', 'fedc', 'fedb'],  # ['ك', 'ﻙ', 'ﻚ', 'ﻜ', 'ﻛ']
    ['0644', 'fedd', 'fede', 'fee0', 'fedf'],  # ['ل', 'ﻝ', 'ﻞ', 'ﻠ', 'ﻟ']
    ['0645', 'fee1', 'fee2', 'fee4', 'fee3'],  # ['م', 'ﻡ', 'ﻢ', 'ﻤ', 'ﻣ']
    ['0646', 'fee5', 'fee6', 'fee8', 'fee7'],  # ['ن', 'ﻥ', 'ﻦ', 'ﻨ', 'ﻧ']
    ['0647', 'fee9', 'feea', 'feec', 'feeb'],  # ['ه', 'ﻩ', 'ﻪ', 'ﻬ', 'ﻫ']
    ['0648', 'feed', 'feee', '', ''],  # ['و', 'ﻭ', 'ﻮ']
    ['064a', 'fef1', 'fef2', 'fef4', 'fef3'],  # ['ي', 'ﻱ', 'ﻲ', 'ﻴ', 'ﻳ']

    ['0629', 'fe93', 'fe94', '', ''],  # ['ة', 'ﺓ', 'ﺔ']
    ['0649', 'feef', 'fef0', '', ''],  # ['ى', 'ﻯ', 'ﻰ']
    ['fefb', 'fefb', 'fefc', '', ''],  # ['ﻻ', 'ﻻ', 'ﻼ']
    ['fef7', 'fef7', 'fef8', '', ''],  # ['ﻷ', 'ﻷ', 'ﻸ']
    ['fef9', 'fef9', 'fefa', '', ''],  # ['ﻹ', 'ﻹ', 'ﻺ']
    ['fef5', 'fef5', 'fef6', '', ''],  # ['ﻵ', 'ﻵ', 'ﻶ']
]

# convert hex codes to int
chars = [[hex2int(x) for x in d] for d in chars]

# map lam-alif to a proper alif
lamalif_to_alif = {'fef5': '0622', 'fef7': '0623', 'fef9': '0625', 'fefb': '0627'}

# convert to int
lamalif_to_alif = {int(k, 16): int(v, 16) for k, v in lamalif_to_alif.items()}


def get_base_char(c):
    k = ord(c)
    v = [v for v in chars if k in v]
    if v:
        k = v[0][0]
    c = chr(k)
    return c


def get_base_text(text):
    l = [get_base_char(c) for c in text]

    unwanted_char = chr(65279)
    if unwanted_char in l:
        l.remove(unwanted_char)
    t = []
    for c in l:
        # remove zero size letter fribidi add to lam-alif
        if c == chr(65279):
            continue
        # dissolve lam-alif to separate lam and alif
        if ord(c) in lamalif_to_alif:
            alif = chr(lamalif_to_alif[ord(c)])
            lam_char = chr(int('0644', 16))
            t.append(alif)
            t.append(lam_char)
            continue
        t.append(c)

    text = ''.join(t)
    return text


def render_bidi_text(text):
    return pyfribidi.log2vis(text, pyfribidi.ON)


def is_neutral(c):
    """control symbols and punctuation"""
    try:
        key = ord(c)
        if key in range(0x0, 0x40) or key in range(0x5b, 0x60) or key in range(0x7b, 0x7f):
            return True
    except:
        pass

    return False


def isarabic(c):
    if isinstance(c, str):
        match = re.match(arabic_ranges_pattern, c)
        # print(match)
        return match
    return False


def handle_entry(event, widget):
    if widget.focus_get() != widget:
        return

    def move_cursor_to_left():
        # control direction
        current_index = widget.index(tk.INSERT)
        new_index = current_index - 1 if current_index >= 1 else 0
        widget.icursor(new_index)

    text = widget._get()

    index = widget.index('insert')

    # get charcters left, and right the cursor
    char_left = text[index - 1] if index > 0 else None
    char_right = text[index] if len(text) > index else None

    if isarabic(char_left) or isarabic(char_right):
        widget.RTL = True
        # print('RTL=TRUE')
    elif not is_neutral(event.char):
        widget.RTL = False

    # handle backspace
    if event.keysym in ('BackSpace', 'Delete'):
        try:
            widget.delete("sel.first", "sel.last")
        except:
            if widget.RTL and event.keysym == 'BackSpace' or not widget.RTL and event.keysym == 'Delete':
                widget.delete(index)
            elif index > 0:
                widget.delete(index - 1)

    elif widget.last_text == widget._get():
        return

    # decide cursor movement
    elif widget.RTL:
        move_cursor_to_left()

    text = widget._get()
    index = widget.index('insert')
    widget.delete(0, "end")

    text = get_base_text(text)
    text = render_bidi_text(text)
    text = get_base_text(text)
    text = render_bidi_text(text)

    widget.insert(0, text)
    widget.icursor(index)

    widget.last_text = widget._get()


def add_bidi_support_for_entry(widget):
    """add arabic support for an entry widget"""

    def handledeletion(event):
        handle_entry(event, widget)
        return 'break'

    widget.RTL = False
    widget.last_text = ''
    widget.bind("<BackSpace>", handledeletion)
    widget.bind("<Delete>", handledeletion)
    widget._get = widget.get
    widget.get = lambda: render_bidi_text(widget._get())

    def set_text(text):
        widget.delete(0, "end")
        widget.insert(0, render_bidi_text(text))

    widget.set = set_text

    widget.bind_all('<KeyPress>', lambda event: handle_entry(event, widget), add='+')


def add_bidi_support_for_label(widget):
    """add arabic support for an entry widget"""

    def get_text():
        return render_bidi_text(widget['text'])

    def set_text(text):
        widget['text'] = render_bidi_text(text)

    widget.get = get_text
    widget.set = set_text


def add_bidi_support(widget):
    """add bidi support for tkinter widget """
    if widget.winfo_class() == 'Label':
        add_bidi_support_for_label(widget)
    elif widget.winfo_class() == 'Entry':
        add_bidi_support_for_entry(widget)


if __name__ == '__main__':
    root = tk.Tk()
    text = 'السلام عليكم'

    # text display incorrectly on linux
    tk.Label(root, text=text, font='any 20').pack()

    entry = tk.Entry(root, font='any 20', justify='right')
    entry.pack()

    lbl = tk.Label(root, font='any 20')
    lbl.pack()

    # adding bidi support for widgets
    add_bidi_support(lbl)
    add_bidi_support(entry)

    # we can use set() and get() methods to set and get text on a widget
    entry.set(text)
    lbl.set('هذا كتاب adventure شيق')

    root.mainloop()
