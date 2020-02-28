''' MorgueLibrarian

Install by building locally with:

python setup.py install
'''
from setuptools import setup

readme = open('README.md', 'r').read()

setup(
    name = "MorgueLibrarian",
    version = "0.1.2",
    author = "John Stilley",
    description = "Tools for parsing DCSS morgue files.",
    license = "GPLv3",
    url = "https://github.com/theJollySin/morgue_librarian",
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Natural Language :: English"
    ],
)

