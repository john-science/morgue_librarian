from bz2 import BZ2File
from glob import glob
import os


class KnownMorgues:
    """ Every time we write data to an output file we want to make sure we aren't duplicating effort.
    To that end, we end up checking and re-checking if a URL has been seen or parsed before.
    This class encapsulates that logic.
    To improve the RAM footprint, we only save the hash of the URL.
    """

    def __init__(self, file_prefixes=['morgue_urls'], dirs=['data']):
        self.file_prefixes = file_prefixes
        self.dirs = dirs
        self.paths = set()

    def find(self):
        """ Master method to populate the known morgues collection

        Returns: None
        """
        # this set of known morgues saves only the hash of the URL or file path, to save space
        self.paths = set()

        for d in self.dirs:
            for prefix in self.file_prefixes:
                self._find(d, prefix)

    def _find(self, d, prefix):
        """ All the files MorgueLibrarian creates start with a URL and then they might have whitespace
        followed by further information. This allows us to easily parse all the various types of
        output files the same, by simply grabbing the first column of whitespace-separated data.

        Here we parse one directory and one file prefix to find all the URLs that match that those
        file names and grab all the URLs from those files and add them to our hashed set.

        Args:
            d (str): directory path to find files
            prefix (str): file prefix to look for
        Returns: None
        """
        # read any old outputs that are in plain txt format
        old_morgue_files = glob(os.path.join(d, prefix + '*.txt'))
        for old_file in old_morgue_files:
            self.paths.update([hash(f.strip().split()[0]) for f in open(old_file, 'r').readlines()])

        # read any old outputs that are in bzip2 format
        old_morgue_files = glob(os.path.join(d, prefix + '*.txt.bz2'))
        for old_file in old_morgue_files:
            self.paths.update([hash(f.strip().split()[0]) for f in BZ2File(old_file, 'r').readlines()])

    def add(self, urls):
        """ Helper method to add some collection of URLs to our hashed set.

        Args:
            urls (iterable): iterable collection URLs as strings
        Returns: None
        """
        # the intended case, where a collection of URLs are passed
        for url in urls:
            self.paths.add(hash(url.strip()))

    def includes(self, url):
        """ Helper method to test if a URL is included in our hashed set.

        Args:
            url (str): URL address
        Returns:
            bool: Is this URL in the our set of known addresses?
        """
        return hash(url) in self.paths

    def reset(self):
        """ Helper method to nuke all the URLs in our hashed set.

        Returns: None
        """
        self.paths = set()

    def __len__(self):
        return len(self.paths)
