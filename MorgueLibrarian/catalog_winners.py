""" Catalog all the Winning Morgues you have collected

The Idea:

First this script prints out some basics about all the winning morgues it can find:

 * How many winners? What's the oldest? How many of each number of runes?

Then this script will print out some stats on the winning morgues sorted based on user input:

* species
* background
* god
* number of runes
* game version

Ideally, we would make this very flexible so users can design their own queries, within the interests of looking through winning morgue to learn how to play.

"""
from glob import glob
import os
from library_data import DATA_DIR, WINNERS
from search_winners import SearchWinners


def main():
    """
    1. parse input commandline for winning build/run info
    2. open/read all winning runs in /data/, bzip or not
    3. print lines that match search criteria
    """
    print("WARNING: This tool still under construction!")
    data_dir = DATA_DIR
    winners = WINNERS

    cw = CatalogWinners(data_dir, winners)
    cw.print_basics()


class CatalogWinners(SearchWinners):

    def __init__(self, data_dir, prefix):
        self.data_dir = data_dir
        self.prefix = prefix
        self.morgues = {}
        super(CatalogWinners, self).__init__(data_dir, prefix)
        self.find()

    def print_basics(self):
        """ TODO
        """
        print("\nTotal Number of Morgues: {0}\n".format(sum(len(v) for v in self.morgues.values())))

        species = set([b[0] for b in self.morgues.keys()])
        species_counts = {s:sum([len(v) for b,v in self.morgues.items() if b[0] == s]) for s in species}

        for v, k in sorted(list((v,k) for k,v in species_counts.items()), reverse=True):
            print("{0}:\t{1}".format(k, v))


if __name__ == '__main__':
    main()

