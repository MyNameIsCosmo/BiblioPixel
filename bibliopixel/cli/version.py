# -*- coding: utf-8 -*-
"""
Prints version information
"""

from bibliopixel import __name__, __version__, __status__, __copyright__
from bibliopixel.cli import Command


class Version(Command):
    name = "version"
    description = "Prints the version, copyright, and release status"

    def main(self):
        print(__name__ + " "
              + __status__
              + " v" + __version__
              + "\n" + __copyright__)
