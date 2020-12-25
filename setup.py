#!/usr/bin/env python

"""
    AwesomeTkinter, a new tkinter widgets design using custom styles and images

    :copyright: (c) 2020 by Mahmoud Elshahat.

"""

import os
import setuptools

# get current directory
path = os.path.realpath(os.path.abspath(__file__))
current_directory = os.path.dirname(path)

# get version
version = {}
with open(f"{current_directory}/awesometkinter/version.py") as f:
    exec(f.read(), version)  # then we can use it as: version['__version__']

# get long description from readme
with open(f"{current_directory}/README.md", "r") as fh:
    long_description = fh.read()

try:
    with open(f"{current_directory}/requirements.txt", "r") as fh:
        requirements = fh.readlines()
except:
    requirements = ['pillow >= 8.0.0']

setuptools.setup(
    name="AwesomeTkinter",
    version=version['__version__'],
    scripts=[],
    author="Mahmoud Elshahat",
    author_email="",
    description="Pretty tkinter widgets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Aboghazala/AwesomeTkinter",
    packages=setuptools.find_packages(),
    keywords="tkinter gui python",
    project_urls={
        'Source': 'https://github.com/Aboghazala/AwesomeTkinter',
        'Tracker': 'https://github.com/Aboghazala/AwesomeTkinter/issues',
        'Releases': 'https://github.com/Aboghazala/AwesomeTkinter/releases',
        'Screenshots': 'https://github.com/Aboghazala/AwesomeTkinter/issues/1'
    },
    install_requires=requirements,
    entry_points={
        # our executable: "exe file on windows for example"
        'console_scripts': [
            'awesometkinter = awesometkinter.__init__:main',
        ]},
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
