from __future__ import absolute_import
from __future__ import print_function

from setuptools import setup, find_packages

setup(
    name='inkscapeslide',
    version="1.0",
    description='Inkscape Slide - the Inkscape Presentation maker',
    author='Samuel D. Lotz',
    author_email='samuel.lotz@salotz.info',
    url='https://github.com/salotz/inkscapeslide',
    license='GPLv3',
    install_requires=[
        "pyPdf2",
        "lxml",
        'click',
    ],
    packages=find_packages(),
    entry_points="""
    [console_scripts]
    inkscapeslide = inkscapeslide.cli:main

    """,
)


