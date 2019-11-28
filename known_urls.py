from bz2 import BZ2File
import os


class KnownURLs:
    """ Every time we write data to an output file we want to make sure we aren't duplicating effort.
    To that end, we end up checking and re-checking if a URL has been seen or parsed before.
    This class encapsulates that logic.
    To improve the RAM footprint, we only save the hash of the URL.
    """

    def __init__(self, file_prefixes, dirs='.'):
        self.file_prefixes = file_prefixes
        self.dirs = dirs
        self.known_morgues = set()

    def find(self):
        """
        """
        # this set of known morgues saves only the hash of the URL or file path, to save space
        known_morgues = set()

        for d in self.dirs:
            for prefix in self.file_prefixes
                # read any old outputs that are in plain txt format
                old_morgue_files = glob(os.path.join(d, prefix + '*.txt'))
                for old_file in old_morgue_files:
                    known_morgues.update([hash(f.strip()) for f in open(old_file, 'r').readlines()])

                # read any old outputs that are in bzip2 format
                old_morgue_files = glob(os.path.join(d, prefix + '*.txt.bz2'))
                for old_file in old_morgue_files:
                    known_morgues.update([hash(f.strip()) for f in BZ2File(old_file, 'r').readlines()])

        self.known_morgues = known_morgues
        return known_morgues

    def update(self, urls):
        """
        """
        for url in urls:
            self.known_morgues.add(hash(url))
