""" Winning Morgue Parser

This the major tool I use to parse through large numbers of DCSS morgue files to determine:

1. Which morgues represent winning runs.
2. What was the build of the winning character.
3. How many runes were collected before the win.
4. What version of DCSS was the game played on.

From this information I hope to learn about the high-level strategies of people who won
games playing similar character builds to myself.

But a side result of this data mining is I can learn lots of other things. For instance,
what percentage of games do players win?
"""
from bz2 import BZ2File
from datetime import datetime
import os
from random import choice
import requests
from sys import argv
from crawl_data import *
from library_data import *
from custom_errors import Loser, ParserError
from known_morgues import KnownMorgues
from url_iterator import URLIterator

# TODO: Add the optional to download and save (bzip) all morgues you find (or just winning morgues).


def main():
    # grab file paths from command line
    master_files = argv[1:]

    # run the winning game parser
    p = WinningParser(master_files)
    p.parse()


class WinningParser:
    """ A helpful parser that can read DCSS morgue files, determine if it represents a winning game and
    save the basic character information if so.
    """

    def __init__(self, master_files):
        self.master_files = master_files
        self.data_dir = DATA_DIR
        self.dt_fmt = DT_FMT
        self.losers = LOSERS
        self.parser_errors = PARSER_ERRORS
        self.winners = WINNERS

    def parse(self):
        """ TODO

        Returns: None
        """
        # the user will pass in some file filled with links / paths to morgues
        urls = []
        for master_file in self.master_files:
            if master_file.endswith('.bz2'):
                binary_urls = BZ2File(master_file, 'r').readlines()
                urls += [u.decode('utf-8') for u in binary_urls]
            else:
                urls += open(master_file, 'r').readlines()

        # init new output files
        dt_now = self.current_datetime_string()
        wf = os.path.join(self.data_dir, '{0}{1}.txt'.format(self.winners, dt_now))
        lf = os.path.join(self.data_dir, '{0}{1}.txt'.format(self.losers, dt_now))
        ef = os.path.join(self.data_dir, '{0}{1}.txt'.format(self.parser_errors, dt_now))

        # what URLs have we already seen?
        known_morgues = KnownMorgues([self.winners, self.losers, self.parser_errors], [self.data_dir])
        known_morgues.find()

        # loop through each morgue file/URL and parse it, save the results to files
        url_iter = URLIterator(urls)
        for url in url_iter:
            # make sure we haven't already parsed this morgue
            if known_morgues.includes(url):
                continue

            # parse the file and write any results to output files
            print('.', end='', flush=True)
            try:
                # parse the text file or HTML link
                if url.startswith('http'):
                    txt = WinningParser.read_url(url)
                else:
                    # TODO: Need option to parse .bzip2 files.
                    txt = WinningParser.read_file(url)

                spec, back, god, runes, ver = self.parse_one_morgue(txt)
                if len(god.strip()):
                    open(wf, 'a+').write('{0}  {1}{2}^{3},{4},{5}\n'.format(url.strip(), spec, back, god, runes, ver))
                else:
                    open(wf, 'a+').write('{0}  {1}{2},{3},{4}\n'.format(url.strip(), spec, back, runes, ver))
            except Loser:
                open(lf, 'a+').write('{0}\n'.format(url.strip()))
            except Exception as e:
                err = str(e).replace('\n', '    ')
                if 'connection' in err.lower():
                    open(ef, 'a+').write('{0} ConnectionError\n'.format(url.strip()))
                else:
                    err_type = 'ParserError' if 'ParserError' in err else 'UnknownError'
                    open(ef, 'a+').write('{0}  {1}: {2}\n'.format(url.strip(), err_type, err))

    @staticmethod
    def read_url(url):
        """ Read the text from a URL

        Args:
            url (str): HTML address for a morgue file
        Returns:
            str: content of the URL
        """
        r = requests.get(url.strip(), headers={'User-Agent': choice(USER_AGENTS)}, timeout=5)
        return r.content.decode("utf-8")

    @staticmethod
    def read_file(file_path):
        """ Read the text from a file

        Args:
            file_path (str): path to the morgue file
        Returns:
            str: content of the file
        """
        return open(file_path.strip(), 'r').read()

    def parse_one_morgue(self, txt):
        """ Parse the text of a single morgue file, to try and determine:
        1. Did the player win this game?
        2. If so, what was their character build, how many runes did they get?

        Args:
            txt (str): full text dump of morgue file
        Returns:
            tuple: species, background, god, num_runes, version
        """
        txt = WinningParser.strip_html(txt)

        lines = txt.split('\n')[:20]
        if len(lines) < 13:
            raise ParserError('Invalid file, not long enough')
        elif not lines[0].startswith(' Dungeon Crawl Stone Soup version '):
            raise ParserError('Invalid file, starting line not found')
        elif "Escaped with the Orb" not in txt:
            raise Loser('This is not a winning run.')

        version = lines[0].split(' version ')[1].split('-')[0].split()[0].split('.')
        version = '.'.join([version[0], version[1]])

        god = ''
        num_runes = -1
        the_line = ''
        for line in lines[1:]:
            if not len(line.strip()):
                continue
            elif line.strip().startswith('... and '):
                num_runes = int(line.split('... and ')[1].split(' runes')[0])
            elif line.strip().startswith('Was ') and line.strip().endswith('.'):
                god = line.lower().split('.')[0].split(' ')[-1]
            elif ('the' in line) and ('(' in line) and (')' in line) and ('Turns:' in line) and ('Time:' in line):
                the_line = line
                break

        if not len(the_line) or num_runes < 0:
            raise ParserError('Error parsing file')

        try:
            build = the_line.split('(')[1].split(')')[0].lower()
            if ' ' not in build and len(build) == 4:
                # cover the case where builds are written as (OpEE)
                species = build[:2]
                background = build[2:]
            else:
                # cover the case where builds are written as (Octopode Earth Elementalist)
                b = build.split()
                if b[0] in SPECIES:
                    species = SPECIES[b[0]]
                    background = ' '.join(b[1:])
                elif (b[0] + ' ' + b[1]) in SPECIES:
                    species = SPECIES[b[0] + ' ' + b[1]]
                    background = ' '.join(b[2:])

            if background in BACKGROUNDS:
                background = BACKGROUNDS[background]
            elif background in BACKGROUNDS_ABR:
                background = BACKGROUNDS_ABR[background]

            if species in SPECIES:
                species = SPECIES[species]
            elif species in SPECIES_ABR:
                species = SPECIES_ABR[species]

            if god in GODS:
                god = GODS[god]
            elif god in GODS_ABR:
                god = GODS_ABR[god]
        except:
            raise ParserError('Build info: {0}'.format(build))

        if len(species) != 2 or len(background) != 2:
            raise ParserError('Build info: {0}'.format(build))

        return species, background, god, num_runes, version

    @staticmethod
    def strip_html(txt):
        """ strip HTML from a non-raw dump, if any exists

        Args:
            txt (str): raw text of morgue file
        Returns:
            str: text of morgue file, with any HTML hopefully stripped out
        """
        if "<!DOCTYPE html>" in txt or "<html>" in txt:
            i = txt.find(' Dungeon Crawl Stone Soup version ')
            if i < 21:
                return ''
            else:
                return txt[i:].split('</pre>')[0]
        else:
            return txt

    def current_datetime_string(self):
        """ Get the current datetime in a simple format useful for file names

        Returns:
            str: current datetime, to the second
        """
        return datetime.now().strftime(self.dt_fmt)


if __name__ == '__main__':
    main()
