"""
    AwesomeTkinter, a new tkinter widgets design using custom styles and images

    :copyright: (c) 2020-2021 by Mahmoud Elshahat.

"""

import platform
import subprocess
import shlex
from tkinter import filedialog


operating_system = platform.system()  # current operating system  ('Windows', 'Linux', 'Darwin')


def run_command(cmd):
    try:
        p = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE, check=True)
        return p.returncode, p.stdout.decode('utf-8').strip()
    except Exception as e:
        # print(e)
        return -1, ''


class FileDialog:
    """use alternative file chooser to replace tkinter ugly file chooser on linux

    available options:
        Zenity: command line tool, based on gtk
        kdialog: command line tool for kde file chooser
        gtk: use Gtk.FileChooserDialog directly thru python, "Don't not use", since sometimes it will raise
             error: Gdk-Message: Fatal IO error 0 (Success) on X server :1, and application will crash
    """

    def __init__(self, foldersonly=False):
        self.use = 'TK'  # , 'zenity', or 'kdialog'
        self.foldersonly = foldersonly
        self.title = 'FireDM - '
        self.title += 'Select a folder' if self.foldersonly else 'Select a file'
        if operating_system == 'Linux':
            # looking for zenity
            _, zenity_path = run_command('which zenity')
            if zenity_path:
                self.use = 'zenity'
            else:
                # looking for kdialog
                _, kdialog_path = run_command('which kdialog')
                if kdialog_path:
                    self.use = 'kdialog'

    def run(self, initialdir='', backend=None):
        selected_path = initialdir
        if backend:
            self.use = backend

        if self.use == 'zenity':
            cmd = 'zenity --file-selection'
            if self.foldersonly:
                cmd += ' --directory'
            if isinstance(initialdir, str):
                cmd += f' --filename="{initialdir}"'
            retcode, path = run_command(cmd)
            # zenity will return either 0, 1 or 5, depending on whether the user pressed OK,
            # Cancel or timeout has been reached
            if retcode in (0, 1, 5):
                selected_path = path

        elif self.use == 'kdialog':
            cmd = 'kdialog'
            if self.foldersonly:
                cmd += ' --getexistingdirectory'
            else:
                cmd += ' --getopenfilename'

            if isinstance(initialdir, str):
                cmd += f' "{initialdir}"'

            retcode, path = run_command(cmd)
            # kdialog will return either 0, 1 depending on whether the user pressed OK, Cancel
            if retcode in (0, 1):
                selected_path = path
        else:
            selected_path = self.run_default(initialdir=initialdir)

        return selected_path

    def run_default(self, initialdir=''):
        # use ugly tkinter filechooser
        if self.foldersonly:
            selected_path = filedialog.askdirectory(initialdir=initialdir)
        else:
            selected_path = filedialog.askopenfilename(initialdir=initialdir)

        return selected_path


filechooser = FileDialog().run
folderchooser = FileDialog(foldersonly=True).run


if __name__ == '__main__':
    # ret, stdout = run_command('blah blah')
    # print(ret, stdout)
    test_fp = filechooser(backend='kdialog')
    print(test_fp)
    #
    test_dir = folderchooser()
    print(test_dir)
