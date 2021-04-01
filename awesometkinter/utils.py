import base64
import math
import platform
import tkinter as tk
from tkinter import ttk
import PIL
from PIL import Image, ImageTk, ImageColor, ImageDraw, ImageFilter
import hashlib
import io


def identify_operating_system():
    """identify current operating system

    Returns:
        (str): 'Windows', 'Linux', or 'Darwin' for mac
      """

    return platform.system()


def calc_md5(binary_data):
    return hashlib.md5(binary_data).hexdigest()


def generate_unique_name(*args):
    """get md5 encoding for any arguments that have a string representation

    Returns:
        md5 string
    """
    name = ''.join([str(x) for x in args])

    try:
        name = calc_md5(name.encode())
    except:
        pass

    return name


def invert_color(color):
    """return inverted hex color
    """
    color = color_to_rgba(color)
    r, g, b, a = color

    inverted_color = rgb2hex(255 - r, 255 - g, 255 - b)
    return inverted_color


def rgb2hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def change_img_color(img, new_color, old_color=None):
    """Change image color

    Args:
        img: pillow image
        new_color (str): new image color, ex: 'red', '#ff00ff', (255, 0, 0), (255, 0, 0, 255)
        old_color (str): color to be replaced, if omitted, all colors will be replaced with new color keeping
                         alpha channel.

    Returns:
        pillow image
    """

    # convert image to RGBA color scheme
    img = img.convert('RGBA')

    # load pixels data
    pixdata = img.load()

    # handle color
    new_color = color_to_rgba(new_color)
    old_color = color_to_rgba(old_color)

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            alpha = pixdata[x, y][-1]
            if old_color:
                if pixdata[x, y] == old_color:
                    r, g, b, _ = new_color
                    pixdata[x, y] = (r, g, b, alpha)
            else:
                r, g, b, _ = new_color
                pixdata[x, y] = (r, g, b, alpha)

    return img


def resize_img(img, size, keep_aspect_ratio=True):
    """resize image using pillow

    Args:
        img (PIL.Image): pillow image object
        size(int or tuple(in, int)): width of image or tuple of (width, height)
        keep_aspect_ratio(bool): maintain aspect ratio relative to width

    Returns:
        (PIL.Image): pillow image
    """

    if isinstance(size, int):
        size = (size, size)

    # get ratio
    width, height = img.size
    requested_width = size[0]

    if keep_aspect_ratio:
        ratio = width / requested_width
        requested_height = height / ratio
    else:
        requested_height = size[1]

    size = (int(requested_width), int(requested_height))

    img = img.resize(size, resample=PIL.Image.LANCZOS)

    return img


def mix_images(background_img, foreground_img):
    """paste an image on top of another image
    Args:
        background_img: pillow image in background
        foreground_img: pillow image in foreground

    Returns:
        pillow image
    """
    background_img = background_img.convert('RGBA')
    foreground_img = foreground_img.convert('RGBA')

    img_w, img_h = foreground_img.size
    bg_w, bg_h = background_img.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    background_img.paste(foreground_img, offset, mask=foreground_img)

    return background_img


def color_to_rgba(color):
    """Convert color names or hex notation to RGBA,

    Args:
        color (str): color e.g. 'white' or '#333' or formats like #rgb or #rrggbb

    Returns:
        (4-tuple): tuple of format (r, g, b, a) e.g. it will return (255, 0, 0, 255) for solid red
    """

    if color is None:
        return None

    if isinstance(color, (tuple, list)):
        if len(color) == 3:
            r, g, b = color
            color = (r, g, b, 255)
        return color
    else:
        return ImageColor.getcolor(color, 'RGBA')


def is_dark(color):
    """rough check if color is dark or light

    Returns:
        (bool): True if color is dark, False if light
    """
    r, g, b, a = color_to_rgba(color)

    # calculate lumina, reference https://stackoverflow.com/a/1855903
    lumina = (0.299 * r + 0.587 * g + 0.114 * b) / 255

    return True if lumina < 0.6 else False


def calc_font_color(bg):
    """calculate font color based on given background

    Args:
        bg (str): background color

    Returns:
        (str): color name, e.g. "white" for dark background and "black" for light background
    """

    return 'white' if is_dark(bg) else 'black'


def calc_contrast_color(color, offset):
    """calculate a contrast color

    for darker colors will get a slightly lighter color depend on "offset" and for light colors will get a darker color

    Args:
        color (str): color
        offset (int): 1 to 254

    Returns:
        (str): color
    """

    r, g, b, a = color_to_rgba(color)
    if is_dark(color):
        new_color = [x + offset if x + offset <= 255 else 255 for x in (r, g, b)]
    else:
        new_color = [x - offset if x - offset >= 0 else 0 for x in (r, g, b)]

    return rgb2hex(*new_color)


def text_to_image(text, text_color, bg_color, size):
    """Not implemented"""
    pass
    # img = Image.new('RGBA', size, color_to_rgba(text_color))
    # draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype(current_path + "s.ttf", size - int(0.15 * width))
    # draw.text((pad, -pad), str(num), font=font, fill=color_to_rgba(bg_color))


def create_pil_image(fp=None, color=None, size=None, b64=None):
    """create pillow Image object

    Args:
        fp: A filename (string), pathlib.Path object or a file object. The file object must implement read(), seek(),
            and tell() methods, and be opened in binary mode.
        color (str): color in tkinter format, e.g. 'red', '#3300ff', also color can be a tuple or a list of RGB,
                     e.g. (255, 0, 255)
        size (int or 2-tuple(int, int)): an image required size in a (width, height) tuple
        b64 (str): base64 hex representation of an image, if "fp" is given this parameter will be ignored

    Returns:
        pillow image object
    """

    if not fp and b64:
        fp = io.BytesIO(base64.b64decode(b64))

    img = Image.open(fp)

    # change color
    if color:
        img = change_img_color(img, color)

    # resize
    if size:
        if isinstance(size, int):
            size = (size, size)
        img = resize_img(img, size)

    return img


def create_image(fp=None, img=None, color=None, size=None, b64=None):
    """create tkinter PhotoImage object
    it can modify size and color of original image

    Args:
        fp: A filename (string), pathlib.Path object or a file object. The file object must implement read(), seek(),
            and tell() methods, and be opened in binary mode.
        img (pillow image): if exist fp or b64 arguments will be ignored
        color (str): color in tkinter format, e.g. 'red', '#3300ff', also color can be a tuple or a list of RGB,
                    e.g. (255, 0, 255)
        size (int or 2-tuple(int, int)): an image required size in a (width, height) tuple
        b64 (str): base64 hex representation of an image, if "fp" is given this parameter will be ignored

    Returns:
        tkinter PhotoImage object
    """
    # create pillow image
    if not img:
        img = create_pil_image(fp, color, size, b64)

    # create tkinter images using pillow ImageTk
    img = ImageTk.PhotoImage(img)

    return img


def create_circle(size=100, thickness=None, color='black', fill=None, antialias=4, offset=0):
    """create high quality circle

    the idea to smooth circle line is to draw a bigger size circle and then resize it to the requested size
    inspired from  https://stackoverflow.com/a/34926008

    Args:
        size (tuple or list, or int): outer diameter of the circle or width of bounding box
        thickness (int): outer line thickness in pixels
        color (str): outer line color
        fill (str): fill color, default is a transparent fill
        antialias (int): used to enhance outer line quality and make it smoother
        offset (int): correct cut edges of circle outline

    Returns:
        PIL image: a circle on a transparent image
    """

    if isinstance(size, int):
        size = (size, size)
    else:
        size = size

    fill_color = color_to_rgba(fill) or '#0000'

    requested_size = size

    # calculate thickness to be 2% of circle diameter
    thickness = thickness or max(size[0] * 2 // 100, 2)

    offset = offset or thickness // 2

    # make things bigger
    size = [x * antialias for x in requested_size]
    thickness *= antialias

    # create a transparent image with a big size
    img = Image.new(size=size, mode='RGBA', color='#0000')

    draw = ImageDraw.Draw(img)

    # draw circle with a required color
    draw.ellipse([offset, offset, size[0] - offset, size[1] - offset], outline=color, fill=fill_color, width=thickness)

    img = img.filter(ImageFilter.BLUR)

    # resize image back to the requested size
    img = img.resize(requested_size, Image.LANCZOS)

    # change color again will enhance quality (weird)
    if fill:
        img = change_img_color(img, color, old_color=color)
        img = change_img_color(img, fill, old_color=fill)
    else:
        img = change_img_color(img, color)

    return img


def apply_gradient(img, gradient='vertical', colors=None, keep_transparency=True):
    """apply gradient color for pillow image

    Args:
        img: pillow image
        gradient (str): vertical, horizontal, diagonal, radial
        colors (iterable): 2-colors for the gradient
        keep_transparency (bool): keep original transparency
    """

    size = img.size
    colors = colors or ['black', 'white']
    color1 = color_to_rgba(colors[0])
    color2 = color_to_rgba(colors[1])

    # load pixels data
    pixdata = img.load()

    if gradient in ('horizontal', 'vertical', 'diagonal'):

        for x in range(0, size[0]):
            for y in range(0, size[1]):

                if gradient == 'horizontal':
                    ratio1 = x / size[1]
                elif gradient == 'vertical':
                    ratio1 = y / size[1]
                elif gradient == 'diagonal':
                    ratio1 = (y + x) / size[1]

                ratio2 = 1 - ratio1

                r = ratio1 * color2[0] + ratio2 * color1[0]
                g = ratio1 * color2[1] + ratio2 * color1[1]
                b = ratio1 * color2[2] + ratio2 * color1[2]

                if keep_transparency:
                    a = pixdata[x, y][-1]
                else:
                    a = ratio1 * color2[3] + ratio2 * color1[3]

                r, g, b, a = (int(x) for x in (r, g, b, a))

                # Place the pixel
                img.putpixel((x, y), (r, g, b, a))

    elif gradient == 'radial':  # inspired by https://stackoverflow.com/a/30669765
        d = min(size)
        radius = d // 2

        for x in range(0, size[0]):
            for y in range(0, size[1]):

                # Find the distance to the center
                distance_to_center = math.sqrt((x - size[0] / 2) ** 2 + (y - size[1] / 2) ** 2)

                ratio1 = distance_to_center / radius
                ratio2 = 1 - ratio1

                r = ratio1 * color2[0] + ratio2 * color1[0]
                g = ratio1 * color2[1] + ratio2 * color1[1]
                b = ratio1 * color2[2] + ratio2 * color1[2]

                if keep_transparency:
                    a = pixdata[x, y][-1]
                else:
                    a = ratio1 * color2[3] + ratio2 * color1[3]
                r, g, b, a = (int(x) for x in (r, g, b, a))

                # Place the pixel
                img.putpixel((x, y), (r, g, b, a))

    return img


def scroll_with_mousewheel(widget, target=None, modifier='Shift', apply_to_children=False):
    """scroll a widget with mouse wheel

    Args:
        widget: tkinter widget
        target: scrollable tkinter widget, in case you need "widget" to catch mousewheel event and make another widget
                to scroll, useful for child widget in a scrollable frame
        modifier (str): Modifier to use with mousewheel to scroll horizontally, default is shift key
        apply_to_children (bool): bind all children

    Examples:
        scroll_with_mousewheel(my_text_widget, target='my_scrollable_frame')

        to make a scrollable canvas:
        for w in my_canvas:
            scroll_with_mousewheel(w, target=my_canvas)
    """

    def _scroll_with_mousewheel(widget):

        target_widget = target if target else widget

        def scroll_vertically(event):
            # scroll vertically  ----------------------------------
            if event.num == 4 or event.delta > 0:
                target_widget.yview_scroll(-1, "unit")

            elif event.num == 5 or event.delta < 0:
                target_widget.yview_scroll(1, "unit")

            return 'break'

        # bind events for vertical scroll ----------------------------------------------
        if hasattr(target_widget, 'yview_scroll'):
            # linux
            widget.bind("<Button-4>", scroll_vertically, add='+')
            widget.bind("<Button-5>", scroll_vertically, add='+')

            # windows and mac
            widget.bind("<MouseWheel>", scroll_vertically, add='+')

        # scroll horizontally ---------------------------------------
        def scroll_horizontally(event):
            # scroll horizontally
            if event.num == 4 or event.delta > 0:
                target_widget.xview_scroll(-1, "unit")

            elif event.num == 5 or event.delta < 0:
                target_widget.xview_scroll(1, "unit")

            return 'break'

        # bind events for horizontal scroll ----------------------------------------------
        if hasattr(target_widget, 'xview_scroll'):
            # linux
            widget.bind(f"<{modifier}-Button-4>", scroll_horizontally, add='+')
            widget.bind(f"<{modifier}-Button-5>", scroll_horizontally, add='+')

            # windows and mac
            widget.bind(f"<{modifier}-MouseWheel>", scroll_horizontally, add='+')

    _scroll_with_mousewheel(widget)

    def handle_children(w):
        for child in w.winfo_children():
            _scroll_with_mousewheel(child)

            # recursive call
            if child.winfo_children():
                handle_children(child)

    if apply_to_children:
        handle_children(widget)


def unbind_mousewheel(widget):
    """unbind mousewheel for a specific widget, e.g. combobox which have mouswheel scroll by default"""

    # linux
    widget.unbind("<Button-4>")
    widget.unbind("<Button-5>")

    # windows and mac
    widget.unbind("<MouseWheel>")


def get_widget_attribute(widget, attr):
    """get an attribute of a widget

    Args:
        widget: tkinter widget "tk or ttk"
        attr (str): attribute or property e.g. 'background'

    Returns:
        attribute value, e.g. '#ffffff' for a background color
    """

    # if it is ttk based will get style applied, it will raise an error if the widget not a ttk
    try:
        style_name = widget.cget('style') or widget.winfo_class()
        s = ttk.Style()
        value = s.lookup(style_name, attr)
        return value
    except:
        pass

    try:
        # if it's a tk widget will use cget
        return widget.cget(attr)
    except:
        pass

    return None


def configure_widget(widget, **kwargs):
    """configure widget's attributes"""
    for k, v in kwargs.items():
        # set widget attribute
        try:
            # treat as a "tk" widget, it will raise if widget is a "ttk"
            widget.config(**{k: v})
            continue
        except:
            pass

        try:
            # in case above failed, it might be a ttk widget
            style_name = widget.cget('style') or widget.winfo_class()
            s = ttk.Style()
            s.configure(style_name, **{k: v})
        except:
            pass


def set_default_theme():
    # select tkinter theme required for things to be right on windows,
    # only 'alt', 'default', or 'classic' can work fine on windows 10
    s = ttk.Style()
    s.theme_use('default')


def theme_compatibility_check(print_warning=False):
    """check if current theme is compatible
    Return:
        bool: True or False
    """
    compatible_themes = ['alt', 'default', 'classic']
    s = ttk.Style()
    current_theme = s.theme_use()
    if current_theme not in compatible_themes:
        if print_warning:
            print(f'AwesomeTkinter Warning: Widgets might not work properly under current theme ({current_theme})\n'
                  f"compatible_themes are ['alt', 'default', 'classic']\n"
                  f"you can set default theme using atk.set_default_theme() or style.theme_use('default')")
        return False

    return True


__all__ = ['identify_operating_system', 'calc_md5', 'generate_unique_name', 'invert_color', 'rgb2hex',
           'change_img_color', 'resize_img', 'mix_images', 'color_to_rgba', 'is_dark', 'calc_font_color',
           'calc_contrast_color', 'text_to_image', 'create_pil_image', 'create_image', 'create_circle',
           'scroll_with_mousewheel', 'unbind_mousewheel', 'get_widget_attribute', 'ImageTk', 'set_default_theme',
           'theme_compatibility_check', 'configure_widget']
