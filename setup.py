from __future__ import absolute_import
from __future__ import print_function

from setuptools import setup, find_packages

setup(
    name='inkscape_pages',
    version="0.1",
    description='Inkscape Pages - Make multipage PDFs with Inkscape SVG layers.',
    author='Samuel D. Lotz',
    author_email='samuel.lotz@salotz.info',
    url='https://github.com/salotz/inkscape_pages',
    license='GPLv3',
    install_requires=[
        "pyPdf2<3",
        'click',
    ],
    packages=find_packages(where='src'),
    package_dir={'' : 'src'},

    entry_points={'console_scripts' :
                  ['inkscape_pages=inkscape_pages.cli:cli']
    },

)


