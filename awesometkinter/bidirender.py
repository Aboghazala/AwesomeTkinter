"""
    AwesomeTkinter, a new tkinter widgets design using custom styles and images

    :copyright: (c) 2020-2021 by Mahmoud Elshahat.

    module description:
        handle arabic text to be shown properly in tkinter widgets (on linux)

"""

import os
import tkinter as tk
import re
from bidi.algorithm import get_display

from .menu import RightClickMenu

UNSHAPED = 0
ISOLATED = 1
INITIAL = 2
MEDIAL = 3
FINAL = 4


shapes_table = (
    ('\u0621', '\uFE80', '', '', ''),  # (ء, ﺀ, , , ), 
    ('\u0622', '\uFE81', '', '', '\uFE82'),  # (آ, ﺁ, , , ﺂ), 
    ('\u0623', '\uFE83', '', '', '\uFE84'),  # (أ, ﺃ, , , ﺄ), 
    ('\u0624', '\uFE85', '', '', '\uFE86'),  # (ؤ, ﺅ, , , ﺆ), 
    ('\u0625', '\uFE87', '', '', '\uFE88'),  # (إ, ﺇ, , , ﺈ), 
    ('\u0626', '\uFE89', '\uFE8B', '\uFE8C', '\uFE8A'),  # (ئ, ﺉ, ﺋ, ﺌ, ﺊ), 
    ('\u0627', '\uFE8D', '', '', '\uFE8E'),  # (ا, ﺍ, , , ﺎ), 
    ('\u0628', '\uFE8F', '\uFE91', '\uFE92', '\uFE90'),  # (ب, ﺏ, ﺑ, ﺒ, ﺐ), 
    ('\u0629', '\uFE93', '', '', '\uFE94'),  # (ة, ﺓ, , , ﺔ), 
    ('\u062A', '\uFE95', '\uFE97', '\uFE98', '\uFE96'),  # (ت, ﺕ, ﺗ, ﺘ, ﺖ), 
    ('\u062B', '\uFE99', '\uFE9B', '\uFE9C', '\uFE9A'),  # (ث, ﺙ, ﺛ, ﺜ, ﺚ), 
    ('\u062C', '\uFE9D', '\uFE9F', '\uFEA0', '\uFE9E'),  # (ج, ﺝ, ﺟ, ﺠ, ﺞ), 
    ('\u062D', '\uFEA1', '\uFEA3', '\uFEA4', '\uFEA2'),  # (ح, ﺡ, ﺣ, ﺤ, ﺢ), 
    ('\u062E', '\uFEA5', '\uFEA7', '\uFEA8', '\uFEA6'),  # (خ, ﺥ, ﺧ, ﺨ, ﺦ), 
    ('\u062F', '\uFEA9', '', '', '\uFEAA'),  # (د, ﺩ, , , ﺪ), 
    ('\u0630', '\uFEAB', '', '', '\uFEAC'),  # (ذ, ﺫ, , , ﺬ), 
    ('\u0631', '\uFEAD', '', '', '\uFEAE'),  # (ر, ﺭ, , , ﺮ), 
    ('\u0632', '\uFEAF', '', '', '\uFEB0'),  # (ز, ﺯ, , , ﺰ), 
    ('\u0633', '\uFEB1', '\uFEB3', '\uFEB4', '\uFEB2'),  # (س, ﺱ, ﺳ, ﺴ, ﺲ), 
    ('\u0634', '\uFEB5', '\uFEB7', '\uFEB8', '\uFEB6'),  # (ش, ﺵ, ﺷ, ﺸ, ﺶ), 
    ('\u0635', '\uFEB9', '\uFEBB', '\uFEBC', '\uFEBA'),  # (ص, ﺹ, ﺻ, ﺼ, ﺺ), 
    ('\u0636', '\uFEBD', '\uFEBF', '\uFEC0', '\uFEBE'),  # (ض, ﺽ, ﺿ, ﻀ, ﺾ), 
    ('\u0637', '\uFEC1', '\uFEC3', '\uFEC4', '\uFEC2'),  # (ط, ﻁ, ﻃ, ﻄ, ﻂ), 
    ('\u0638', '\uFEC5', '\uFEC7', '\uFEC8', '\uFEC6'),  # (ظ, ﻅ, ﻇ, ﻈ, ﻆ), 
    ('\u0639', '\uFEC9', '\uFECB', '\uFECC', '\uFECA'),  # (ع, ﻉ, ﻋ, ﻌ, ﻊ), 
    ('\u063A', '\uFECD', '\uFECF', '\uFED0', '\uFECE'),  # (غ, ﻍ, ﻏ, ﻐ, ﻎ), 
    ('\u0640', '\u0640', '\u0640', '\u0640', '\u0640'),  # (ـ, ـ, ـ, ـ, ـ), 
    ('\u0641', '\uFED1', '\uFED3', '\uFED4', '\uFED2'),  # (ف, ﻑ, ﻓ, ﻔ, ﻒ), 
    ('\u0642', '\uFED5', '\uFED7', '\uFED8', '\uFED6'),  # (ق, ﻕ, ﻗ, ﻘ, ﻖ), 
    ('\u0643', '\uFED9', '\uFEDB', '\uFEDC', '\uFEDA'),  # (ك, ﻙ, ﻛ, ﻜ, ﻚ), 
    ('\u0644', '\uFEDD', '\uFEDF', '\uFEE0', '\uFEDE'),  # (ل, ﻝ, ﻟ, ﻠ, ﻞ), 
    ('\u0645', '\uFEE1', '\uFEE3', '\uFEE4', '\uFEE2'),  # (م, ﻡ, ﻣ, ﻤ, ﻢ), 
    ('\u0646', '\uFEE5', '\uFEE7', '\uFEE8', '\uFEE6'),  # (ن, ﻥ, ﻧ, ﻨ, ﻦ), 
    ('\u0647', '\uFEE9', '\uFEEB', '\uFEEC', '\uFEEA'),  # (ه, ﻩ, ﻫ, ﻬ, ﻪ), 
    ('\u0648', '\uFEED', '', '', '\uFEEE'),  # (و, ﻭ, , , ﻮ), 
    # ('\u0649', '\uFEEF', '\uFBE8', '\uFBE9', '\uFEF0'),  # (ى, ﻯ, ﯨ, ﯩ, ﻰ), 
    ('\u0649', '\uFEEF', '', '', '\uFEF0'),   # (ى, ﻯ, , , ﻰ), 
    ('\u064A', '\uFEF1', '\uFEF3', '\uFEF4', '\uFEF2'),  # (ي, ﻱ, ﻳ, ﻴ, ﻲ), 
    ('\u0671', '\uFB50', '', '', '\uFB51'),  # (ٱ, ﭐ, , , ﭑ), 
    ('\u0677', '\uFBDD', '', '', ''),  # (ٷ, ﯝ, , , ), 
    ('\u0679', '\uFB66', '\uFB68', '\uFB69', '\uFB67'),  # (ٹ, ﭦ, ﭨ, ﭩ, ﭧ), 
    ('\u067A', '\uFB5E', '\uFB60', '\uFB61', '\uFB5F'),  # (ٺ, ﭞ, ﭠ, ﭡ, ﭟ), 
    ('\u067B', '\uFB52', '\uFB54', '\uFB55', '\uFB53'),  # (ٻ, ﭒ, ﭔ, ﭕ, ﭓ), 
    ('\u067E', '\uFB56', '\uFB58', '\uFB59', '\uFB57'),  # (پ, ﭖ, ﭘ, ﭙ, ﭗ), 
    ('\u067F', '\uFB62', '\uFB64', '\uFB65', '\uFB63'),  # (ٿ, ﭢ, ﭤ, ﭥ, ﭣ), 
    ('\u0680', '\uFB5A', '\uFB5C', '\uFB5D', '\uFB5B'),  # (ڀ, ﭚ, ﭜ, ﭝ, ﭛ), 
    ('\u0683', '\uFB76', '\uFB78', '\uFB79', '\uFB77'),  # (ڃ, ﭶ, ﭸ, ﭹ, ﭷ), 
    ('\u0684', '\uFB72', '\uFB74', '\uFB75', '\uFB73'),  # (ڄ, ﭲ, ﭴ, ﭵ, ﭳ), 
    ('\u0686', '\uFB7A', '\uFB7C', '\uFB7D', '\uFB7B'),  # (چ, ﭺ, ﭼ, ﭽ, ﭻ), 
    ('\u0687', '\uFB7E', '\uFB80', '\uFB81', '\uFB7F'),  # (ڇ, ﭾ, ﮀ, ﮁ, ﭿ), 
    ('\u0688', '\uFB88', '', '', '\uFB89'),  # (ڈ, ﮈ, , , ﮉ), 
    ('\u068C', '\uFB84', '', '', '\uFB85'),  # (ڌ, ﮄ, , , ﮅ), 
    ('\u068D', '\uFB82', '', '', '\uFB83'),  # (ڍ, ﮂ, , , ﮃ), 
    ('\u068E', '\uFB86', '', '', '\uFB87'),  # (ڎ, ﮆ, , , ﮇ), 
    ('\u0691', '\uFB8C', '', '', '\uFB8D'),  # (ڑ, ﮌ, , , ﮍ), 
    ('\u0698', '\uFB8A', '', '', '\uFB8B'),  # (ژ, ﮊ, , , ﮋ), 
    ('\u06A4', '\uFB6A', '\uFB6C', '\uFB6D', '\uFB6B'),  # (ڤ, ﭪ, ﭬ, ﭭ, ﭫ), 
    ('\u06A6', '\uFB6E', '\uFB70', '\uFB71', '\uFB6F'),  # (ڦ, ﭮ, ﭰ, ﭱ, ﭯ), 
    ('\u06A9', '\uFB8E', '\uFB90', '\uFB91', '\uFB8F'),  # (ک, ﮎ, ﮐ, ﮑ, ﮏ), 
    ('\u06AD', '\uFBD3', '\uFBD5', '\uFBD6', '\uFBD4'),  # (ڭ, ﯓ, ﯕ, ﯖ, ﯔ), 
    ('\u06AF', '\uFB92', '\uFB94', '\uFB95', '\uFB93'),  # (گ, ﮒ, ﮔ, ﮕ, ﮓ), 
    ('\u06B1', '\uFB9A', '\uFB9C', '\uFB9D', '\uFB9B'),  # (ڱ, ﮚ, ﮜ, ﮝ, ﮛ), 
    ('\u06B3', '\uFB96', '\uFB98', '\uFB99', '\uFB97'),  # (ڳ, ﮖ, ﮘ, ﮙ, ﮗ), 
    ('\u06BA', '\uFB9E', '', '', '\uFB9F'),  # (ں, ﮞ, , , ﮟ), 
    ('\u06BB', '\uFBA0', '\uFBA2', '\uFBA3', '\uFBA1'),  # (ڻ, ﮠ, ﮢ, ﮣ, ﮡ), 
    ('\u06BE', '\uFBAA', '\uFBAC', '\uFBAD', '\uFBAB'),  # (ھ, ﮪ, ﮬ, ﮭ, ﮫ), 
    ('\u06C0', '\uFBA4', '', '', '\uFBA5'),  # (ۀ, ﮤ, , , ﮥ), 
    ('\u06C1', '\uFBA6', '\uFBA8', '\uFBA9', '\uFBA7'),  # (ہ, ﮦ, ﮨ, ﮩ, ﮧ), 
    ('\u06C5', '\uFBE0', '', '', '\uFBE1'),  # (ۅ, ﯠ, , , ﯡ), 
    ('\u06C6', '\uFBD9', '', '', '\uFBDA'),  # (ۆ, ﯙ, , , ﯚ), 
    ('\u06C7', '\uFBD7', '', '', '\uFBD8'),  # (ۇ, ﯗ, , , ﯘ), 
    ('\u06C8', '\uFBDB', '', '', '\uFBDC'),  # (ۈ, ﯛ, , , ﯜ), 
    ('\u06C9', '\uFBE2', '', '', '\uFBE3'),  # (ۉ, ﯢ, , , ﯣ), 
    ('\u06CB', '\uFBDE', '', '', '\uFBDF'),  # (ۋ, ﯞ, , , ﯟ), 
    ('\u06CC', '\uFBFC', '\uFBFE', '\uFBFF', '\uFBFD'),  # (ی, ﯼ, ﯾ, ﯿ, ﯽ), 
    ('\u06D0', '\uFBE4', '\uFBE6', '\uFBE7', '\uFBE5'),  # (ې, ﯤ, ﯦ, ﯧ, ﯥ), 
    ('\u06D2', '\uFBAE', '', '', '\uFBAF'),  # (ے, ﮮ, , , ﮯ), 
    ('\u06D3', '\uFBB0', '', '', '\uFBB1'),  # (ۓ, ﮰ, , , ﮱ), 
    ('\uFEFB', '\uFEFB', '', '', '\uFEFC'),  # (ﻻ, ﻻ, , , ﻼ), 
    ('\uFEF7', '\uFEF7', '', '', '\uFEF8'),  # (ﻷ, ﻷ, , , ﻸ), 
    ('\uFEF5', '\uFEF5', '', '', '\uFEF6'),  # (ﻵ, ﻵ, , , ﻶ), 
)

mandatory_liga_table = {
    ('\uFEDF', '\uFE82'): '\uFEF5',  # ['ﻟ', 'ﺂ', 'ﻵ']
    ('\uFEDF', '\uFE84'): '\uFEF7',  # ['ﻟ', 'ﺄ', 'ﻷ']
    ('\uFEDF', '\uFE88'): '\uFEF9',  # ['ﻟ', 'ﺈ', 'ﻹ']
    ('\uFEDF', '\uFE8E'): '\uFEFB',  # ['ﻟ', 'ﺎ', 'ﻻ']
    ('\uFEE0', '\uFE82'): '\uFEF6',  # ['ﻠ', 'ﺂ', 'ﻶ']
    ('\uFEE0', '\uFE84'): '\uFEF8',  # ['ﻠ', 'ﺄ', 'ﻸ']
    ('\uFEE0', '\uFE88'): '\uFEFA',  # ['ﻠ', 'ﺈ', 'ﻺ']
    ('\uFEE0', '\uFE8E'): '\uFEFC',  # ['ﻠ', 'ﺎ', 'ﻼ']
    }

HARAKAT_RE = re.compile(
    '['
    '\u0610-\u061a'
    '\u064b-\u065f'
    '\u0670'
    '\u06d6-\u06dc'
    '\u06df-\u06e8'
    '\u06ea-\u06ed'
    '\u08d4-\u08e1'
    '\u08d4-\u08ed'
    '\u08e3-\u08ff'
    ']',

    re.UNICODE | re.X
    )

ARABIC_RE = re.compile(
    '['
    '\u0600-\u060A'
    '\u060C-\u06FF'
    '\u0750-\u077F'
    '\u08A0-\u08FF'
    '\u206C-\u206D'
    '\uFB50-\uFD3D'
    '\uFD50-\uFDFB'
    '\uFE70-\uFEFC'
    ']',
    re.UNICODE | re.X
    )

NUMBERS_RE = re.compile(
    '['
    '\u0660-\u0669'  # indic numbers
    '\u0030-\u0039'  # arabic numbers
    ']',

    re.UNICODE | re.X)

NEUTRAL_RE = re.compile(
    '['
    '\u0000-\u0040'  
    '\u005B-\u0060'  
    '\u007B-\u007F'  
    ']',

    re.UNICODE | re.X)


def remove_harakat(text):
    result = [c for c in text if not HARAKAT_RE.match(c)]
    # print(HARAKAT_RE.match(c))
    return ''.join(result)


def do_ligation(text):
    result = []

    for i, c in enumerate(text):
        shape = mandatory_liga_table.get((c, text[i - 1]), None)
        if shape:
            result.pop()
            result.append(shape)
        else:
            result.append(c)

    return ''.join(result)


def do_shaping(text):
    def get_shapes(c):
        # get all different letter shapes 
        if c is None:
            return {}
        key = c 
        match = [v for v in shapes_table if key in v]
        if match:
            match = match[0]
            return {ISOLATED: match[1], INITIAL: match[2], MEDIAL: match[3], FINAL: match[4]}
        else:
            return {}

    def get_shape(c, right_char, left_char):
        """get a proper letter shape
        Args:
            c: current letter
            right_char: letter before
            left_char: letter after
        """
        c_shapes = get_shapes(c)

        if c_shapes and c_shapes.get(FINAL):
            # letter is arabic
            right_char_shapes = get_shapes(right_char)
            left_char_shapes = get_shapes(left_char)

            position = MEDIAL if right_char_shapes.get(MEDIAL) else INITIAL
            alternative = {MEDIAL: FINAL, INITIAL: ISOLATED}
            if not isarabic(left_char):
                position = alternative[position]
            elif not left_char_shapes.get(FINAL):
                position = ISOLATED

            c = c_shapes.get(position) or c_shapes.get(alternative[position])

          
        return c

    t = []
    for i in range(len(text) - 1, -1, -1):
        c = text[i]
        right_char = text[i + 1] if i < len(text) - 1 else None
        left_char = text[i - 1] if i > 0 else None
        t.insert(0, get_shape(c, right_char, left_char))
    return ''.join(t)


def reshaper(text):
    text = do_shaping(text)
    text = do_ligation(text)
    text = remove_harakat(text)
    return text


def render_bidi_text(text):
    text = get_display(text)
    text = reshaper(text)
    
    return text


def derender_bidi_text(text):
    # convert visual text to logical

    # get unshaped characters
    unshaped_text = []
    for c in text:
        match = [item[0] for item in shapes_table if c in item]
        if match:
            c = match[0]
        unshaped_text.append(c)

    # reverse text order to its original state
    text = get_display(''.join(unshaped_text))

    return text


def split_path(path):
    """
    split path into individual parts

    Args:
        path(str): string representation of a path, e.g: '/home/Desktop'

    Return:
        list of splitted path

    credit: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch04s16.html
    """

    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts


def render_bidi_path(path):
    """
    render bidi words in path string

    Args:
        path(str): string representation of a path, e.g: '/home/Desktop'

    Return:
        (str) rendered path

    """
    parts = split_path(path)
    parts = [render_bidi_text(x) for x in parts]
    return os.path.join(*parts)


def derender_bidi_path(path):
    """
    reverse of render_bidi_path
    """
    parts = split_path(path)
    parts = [derender_bidi_text(x) for x in parts]
    return os.path.join(*parts)


def render_text(text, ispath=False):
    """
    render bidi text

    Args:
        text(str): input text that contains a bidi words e.g: English words mixed with Arabic words
        ispath(bool): whether the text argument is path or not, e.g: '/usr/bin/etc'

    Returns:
        (str): rendered text
    """
    if ispath:
        return render_bidi_path(text)
    else:
        return render_bidi_text(text)


def derender_text(text, ispath=False):
    if ispath:
        return derender_bidi_path(text)
    else:
        return derender_bidi_text(text)


def isarabic(c):
    if isinstance(c, str):
        match = ARABIC_RE.match(c)
        return match
    return False


def is_neutral(c):
    if isinstance(c, str):
        match = NEUTRAL_RE.match(c)
        return match
    return False


def handle_entry(event, widget):
    try:
        if widget.focus_get() != widget:  # sometimes it raise an exception
            return
    except:
        return

    def move_cursor_to_left():
        # control direction
        current_index = widget.index(tk.INSERT)
        new_index = current_index - 1 if current_index >= 1 else 0
        widget.icursor(new_index)


    c = event.char
    text = widget._get()
    index = widget.index('insert')

    if not (c or event.keysym in ('BackSpace', 'Delete') or isarabic(c) or is_neutral(c)):
        return

    if NUMBERS_RE.match(event.char):
        return

    if isarabic(c):
        widget.RTL = True
        move_cursor_to_left()
    # handle backspace
    elif event.keysym in ('BackSpace', 'Delete'):
        try:
            widget.delete("sel.first", "sel.last")
        except:
            if widget.RTL and event.keysym == 'BackSpace' or not widget.RTL and event.keysym == 'Delete':
                widget.delete(index)
            elif index > 0:
                widget.delete(index - 1)

    elif is_neutral(c) and widget.RTL:
        move_cursor_to_left()
    else:
        widget.RTL = False


    if widget.last_text == widget._get():
        return

   
    text = widget._get()
    index = widget.index('insert')
    widget.delete(0, "end")

    text = reshaper(text)

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
    widget.get = lambda: derender_bidi_text(widget._get())

    def set_text(text):
        widget.delete(0, "end")
        widget.insert(0, render_bidi_text(text))

    widget.set = set_text

    widget.bind_all('<KeyPress>', lambda event: handle_entry(event, widget), add='+')


def add_bidi_support_for_label(widget):
    """add arabic support for an entry widget"""

    def get_text():
        return derender_bidi_text(widget['text'])

    def set_text(text):
        widget['text'] = render_bidi_text(text)

    widget.get = get_text
    widget.set = set_text


def add_bidi_support(widget, render_copy_paste=True, copy_paste_menu=False, ispath=False):
    """add bidi support for tkinter widget """
    if widget.winfo_class() == 'Label':
        add_bidi_support_for_label(widget)
    elif widget.winfo_class() == 'Entry':
        add_bidi_support_for_entry(widget)
        if render_copy_paste:
            override_copy_paste(widget, ispath=ispath, copy_paste_menu=copy_paste_menu)


def override_copy_paste(widget, copyrender=derender_text, pasterender=render_text, ispath=False, copy_paste_menu=False):
    
    def copy(value):
        """copy clipboard value

        Args:
            value (str): value to be copied to clipboard
        """
        try:
            widget.clipboard_clear()
            widget.clipboard_append(str(value))
        except:
            pass

    def paste():
        """get clipboard value"""
        try:
            value = widget.clipboard_get()
        except:
            value = ''

        return value

    def copy_callback(*args):
        try:
            selected_text = widget.selection_get()
            derendered_text = copyrender(selected_text, ispath=ispath)
            copy(derendered_text)
        except:
            pass

        return 'break'

    def paste_callback(*args):
        try:
            widget.delete("sel.first", "sel.last")
        except:
            pass

        try:
            text = paste()
            rendered_text = pasterender(text, ispath=ispath)
            widget.insert(tk.INSERT, rendered_text)
        except:
            pass

        return 'break'

    # bind
    widget.bind("<<Copy>>", copy_callback)
    widget.bind("<<Paste>>", paste_callback)

    # reference copy paste
    widget.copy_callback = copy_callback
    widget.paste_callback = paste_callback

    # right click menu
    def rcm_handler(option):
        if option.lower() == 'copy':
            copy_callback()
        else:
            paste_callback()

    if copy_paste_menu:
        widget.rcm = RightClickMenu(widget, ['copy', 'paste'], callback=rcm_handler)


if __name__ == '__main__':
    root = tk.Tk()
    text = 'السلام عليكم'

    # text display incorrectly on linux
    dummyvar = tk.StringVar()
    dummyvar.set(text)
    tk.Label(root, textvariable=dummyvar, font='any 20').pack()

    # uncomment below to set a rendered text to first label
    dummyvar.set(render_bidi_text(text))

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
