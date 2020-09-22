"""
    AwesomeTkinter, a new tkinter widgets design using custom styles and images

    :copyright: (c) 2020 by Mahmoud Elshahat.

"""

from .utils import *
from .config import *
from .images import *


class Button3d(ttk.Button):
    """create a button with 3d background color and shadow"""
    styles = []

    def __init__(self, parent, bg=None, fg=None, **options):
        """initialize

        Args:
            parent: tkinter container widget, i.e. root or another frame
            bg (str): button color
            fg (str): text color
        """
        self.bg = bg or DEFAULT_COLOR
        parent_color = get_widget_attribute(parent, 'background') or DEFAULT_COLOR

        # initialize super class
        ttk.Button.__init__(self, parent, **options)

        # create unique style name based on frame color
        button_style = f'Button3d_{len(Button3d.styles)}_.TButton'

        # create style
        if button_style not in Button3d.styles:
            self.create_images()

            # create elements
            s = ttk.Style()
            element_name = f'{button_style}_element'
            s.element_create(element_name, 'image', self.img, ('pressed', self.pressed_img), border=12, sticky="nsew")
            s.layout(button_style,
                     [('Button.border', {'sticky': 'nswe', 'border': '1', 'children':
                         [(element_name, {'sticky': 'nswe', 'children':
                             [('Button.padding', {'sticky': 'nswe', 'children':
                                 [('Button.label', {'sticky': 'nswe'})]})]})]})])
            s.map(button_style, background=[('', parent_color)], foreground=[('', calc_font_color(self.bg))])
            s.configure(button_style, padding=0, borderwidth=0, focuscolor=self.bg)

            # add to styles
            Button3d.styles.append(button_style)

        self['style'] = button_style

    def create_images(self):

        shadow_img = create_pil_image(b64=btn_base)
        img = create_pil_image(b64=btn_face, color=self.bg)

        # merge face with base image
        img = mix_images(shadow_img, img)

        pressed_img = img.rotate(180)

        self.img = ImageTk.PhotoImage(img)
        self.pressed_img = ImageTk.PhotoImage(pressed_img) 


class Radiobutton(ttk.Radiobutton):
    """ttk.Radiobutton with better indicator quality"""

    styles = []

    def __init__(self, parent, text=None, ind_bg=None, ind_mark_color=None, ind_outline_color=None, bg=None, fg=None,
                 font=None, value=None, **kwargs):
        """initialize
        Args:
            parent: tkinter container
            text (str): text
            ind_bg (str): indicator ring background "fill color"
            ind_outline_color (str): indicator outline / ring color
            ind_mark_color (str): check mark color
            bg (str): background color "should match parent bg
            fg (str): text color
            font (str): text font, e.g. "any 10 bold"
            value (any): value assigned to button variable when selected
        """
        bg = bg or get_widget_attribute(parent, 'background')
        fg = fg or calc_font_color(bg)
        ind_bg = ind_bg or bg
        ind_outline_color = ind_outline_color or fg
        ind_mark_color = ind_mark_color or fg

        value = value or text

        custom_style = f'RadioButton_{len(Radiobutton.styles)}'
        Radiobutton.styles.append(custom_style)

        s = ttk.Style()

        # create indicator outline
        outline_img = create_circle(size=12, thickness=1, color=ind_outline_color, fill=ind_bg, offset=2)

        # create indicator mark
        mark_img = create_circle(size=6, thickness=0, color=ind_mark_color, fill=ind_mark_color)

        selection_img = mix_images(outline_img, mark_img)

        # create tkinter PhotoImage
        self.outline_img = create_image(img=outline_img)
        self.selection_img = create_image(img=selection_img)

        # custom style
        s.layout(custom_style, [('Radiobutton.padding',
                                 {'sticky': 'nswe', 'children': [('Radiobutton.label', {'sticky': 'nswe'})]})])
        s.configure(custom_style, foreground=fg)
        s.map(custom_style, background=[('', bg)])

        if font:
            s.configure(custom_style, font=font)

        # initialize super class
        ttk.Radiobutton.__init__(self, master=parent, text=text, value=value, style=custom_style,
                                 image=[self.outline_img, 'selected', self.selection_img],
                                 compound='left', **kwargs)


all = ['Button3d', 'RadioButton']

