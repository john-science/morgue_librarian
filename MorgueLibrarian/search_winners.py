""" Search all the Winning Morgues You've Catalogued
"""
from glob import glob
import os
from sys import argv
from library_data import DATA_DIR, WINNERS


def main():
    """
    1. parse input commandline for winning build/run info
    2. open/read all winning runs in /data/, bzip or not
    3. print lines that match search criteria
    """
    data_dir = DATA_DIR
    winners = WINNERS
    args = ['-', '-', '-', '-', '-']
    print_stats = 0

    for a, arg in enumerate(argv[1:]):
        if arg.startswith('-s') or arg.startswith('--stats'):
            # How many top builds do we want to print?
            print_stats = 1
            if ':' in arg:
                print_stats = int(arg.split(':')[1].strip())
        else:
            args[a] = arg

    wc = SearchWinners(data_dir, winners, print_stats)
    wc.print_matches(args[0], args[1], args[2], args[3], args[4])


class SearchWinners:

    def __init__(self, data_dir, prefix, print_stats=0):
        self.data_dir = data_dir
        self.prefix = prefix
        self.print_stats = print_stats
        self.morgues = {}

    def print_matches(self, species, background, god, num_runes, ver):
        """ Print any morgues that match the winning character build info provided
        (Defaults are given by "-".)

        Args:
            species (str): species of winning character
            background (str): background of winning character
            god (str): final diety for the of winning character
            num_runes (int): number of runes player had by end
            version (float): major game version of the
        Returns: None
        """
        self.find()

        matches = self.morgues.copy()

        # subset the morgues to match our search criteria
        if species != '-':
            matches = {m:u for m, u in matches.items() if m[0] == species}
        if background != '-':
            matches = {m:u for m, u in matches.items() if m[1] == background}
        if god != '-':
            matches = {m:u for m, u in matches.items() if m[2] == god}
        if num_runes != '-':
            matches = {m:u for m, u in matches.items() if m[3] == int(num_runes)}
        if ver != '-':
            matches = {m:u for m, u in matches.items() if m[4] == float(ver)}

        if not len(matches):
            print('No matches found.')
            return

        # print all the winning morgues that matches the search criteria
        for build in sorted(matches.keys()):
            god_str = '^' + build[2].ljust(4) if len(build[2]) else '     '
            b = build[0] + build[1] + god_str + str(build[3]).rjust(3) + ' ' + str(build[4]).ljust(5) + '  '
            for line in sorted(matches[build]):
                print(b + line)

        # print some summary statistics, for the most popular builds that match the search criteria
        if not self.print_stats:
            return

        # calc optional stats
        build_counts = {}
        for b, us in matches.items():
            build = b[0] + b[1]
            if len(b[2]):
                build += '^' + b[2]
            cnt = len(us)
            if build not in build_counts:
                build_counts[build] = 0
            build_counts[build] += cnt

        # print optional stats
        the_cut = sorted(set(build_counts.values()))
        the_cut = the_cut[-min(self.print_stats, len(the_cut))]
        total_count = sum(build_counts.values())
        print('\nMost popular build(s):')
        bcs = sorted([(c,b) for b,c in build_counts.items() if c >= the_cut], reverse=True)
        for count, build in bcs:
            if count >= the_cut:
                print('{0}/{1}:\t{2}'.format(count, total_count, build))

    def find(self):
        """ read all the lines from any winning morgue files that you have lying around

        Returns: None
        """
        # this set of known morgues saves only the hash of the URL or file path, to save space
        self.morgues = {}

        # read any old outputs that are in plain txt format
        old_morgue_files = glob(os.path.join(self.data_dir, self.prefix + '*.txt'))
        for old_file in old_morgue_files:
            with open(old_file, 'r') as f:
                for line in f.readlines():
                    url, build = SearchWinners.read_winning_line(line)
                    if build not in self.morgues:
                        self.morgues[build]= []
                    self.morgues[build].append(url)

        # read any old outputs that are in bzip2 format
        old_morgue_files = glob(os.path.join(self.data_dir, self.prefix + '*.txt.bz2'))
        for old_file in old_morgue_files:
            with BZ2File(old_file, 'r') as f:
                for line in f.readlines():
                    url, build = SearchWinners.read_winning_line(line)
                    if build not in self.morgues:
                        self.morgues[build]= []
                    self.morgues[build].append(url)

    @staticmethod
    def read_winning_line(line):
        """ read a custom winning game descrption line

        Args:
            line (str): custom winning morgue line
        Returns:
            tuple: (url, (species, background, god, num_runes, ver))
        """
        url, info = line.strip().split()
        sbg, num_runes, ver = info.split(',')
        if '^' in sbg:
            sb, god = sbg.split('^')
        else:
            sb = sbg
            god = ''

        species = sb[:2]
        background = sb[2:]
        num_runes = int(num_runes)
        ver = float(ver)
        return url, (species, background, god, num_runes, ver)


if __name__ == '__main__':
    main()
