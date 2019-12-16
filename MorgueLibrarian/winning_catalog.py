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
    args = ['*', '*', '*', '*', '*']

    for a, arg in enumerate(argv[1:]):
        args[a] = arg

    wc = WinningCatalog(data_dir, winners)
    wc.print_matches(args[0], args[1], args[2], args[3], args[4])


class WinningCatalog:

    def __init__(self, data_dir, prefix):
        self.data_dir = data_dir
        self.prefix = prefix
        self.morgues = {}

    def print_matches(self, species, background, god, num_runes, ver):
        """ TODO
        """
        self.find()

        matches = self.morgues.copy()

        # TODO: asterisk doesn't parse well as a POSIX commandline term. Try "-", "@", "any", "all", or something.
        if species != '*':
            matches = {m:u for m, u in matches.items() if m[0] == species}
        if background != '*':
            matches = {m:u for m, u in matches.items() if m[1] == background}
        if god != '*':
            matches = {m:u for m, u in matches.items() if m[2] == god}
        if num_runes != '*':
            matches = {m:u for m, u in matches.items() if m[3] == int(num_runes)}
        if ver != '*':
            matches = {m:u for m, u in matches.items() if m[4] == float(ver)}

        if not len(matches):
            print('No matches found.')
        else:
            for build in sorted(matches.keys()):
                b = build[0] + build[1] + '^' + build[2] + str(build[3]).rjust(3) + ' ' + str(build[4]).ljust(5) + '  '
                for line in sorted(matches[build]):
                    print(b + line)

    def find(self):
        """ TODO

        Returns: None
        """
        # this set of known morgues saves only the hash of the URL or file path, to save space
        self.morgues = {}

        # read any old outputs that are in plain txt format
        old_morgue_files = glob(os.path.join(self.data_dir, self.prefix + '*.txt'))
        for old_file in old_morgue_files:
            with open(old_file, 'r') as f:
                for line in f.readlines():
                    url, build = WinningCatalog.read_winning_line(line)
                    if build not in self.morgues:
                        self.morgues[build]= []
                    self.morgues[build].append(url)

        # read any old outputs that are in bzip2 format
        old_morgue_files = glob(os.path.join(self.data_dir, self.prefix + '*.txt.bz2'))
        for old_file in old_morgue_files:
            with BZ2File(old_file, 'r') as f:
                for line in f.readlines():
                    url, build = WinningCatalog.read_winning_line(line)
                    if build not in self.morgues:
                        self.morgues[build]= []
                    self.morgues[build].append(url)

    @staticmethod
    def read_winning_line(line):
        """ TODO
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
