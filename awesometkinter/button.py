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


all = ['Button3d']