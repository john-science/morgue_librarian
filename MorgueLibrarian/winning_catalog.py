import os
from sys import argv
from library_data import DATA_DIR, WINNERS


def main():
    """
    1. parse input commandline for winning build/run info
    2. open/read all winning runs in /data/, bzip or not
    3. print lines that match search criteria
      a) exact matches
      b) wildcard match any
      c) match any in a list
      d) range operators from Python syntax: < > <= >= !=
        i) perhaps we can use eval() here, to build lambdas?
    """
    data_dir = DATA_DIR
    winners = WINNERS
    args = ['*', '*', '*', '*', '*']

    for a, arg in enumerate(argv[1:]):
        args[a - 1] = arg

    wc = WinningCatalog(data_dir, winners)
    wc.print_matches(args[0], args[1], args[2], args[3], args[4])


class WinningCatalog:

    def __init__(self, data_dir, winners):
        self.data_dir = data_dir
        self.winners = winners
        self.morgues = {}

    def print_matches(self, species, background, god, num_runes, ver):
        """
        """
        pass


if __name__ == '__main__':
    main()
