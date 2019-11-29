from datetime import datetime
from random import choice, random, shuffle
from time import sleep


class URLIterator:
    """ A Helpful iterator designed to loop through a set of URLs,
    with an eye towards not hitting the same URL too often
    """

    def __init__(self, url_set, wait=60.0):
        # load set of URLs into interleaving dictionary
        self.wait = abs(wait)
        self.urls = {}

        for url in url_set:
            base_url = url[:url[8:].find('/') + 8].replace('https', 'http')
            if base_url not in self.urls:
                self.urls[base_url] = []

            self.urls[base_url].append(url.strip())

        for base_url in list(self.urls.keys()):
            shuffle(self.urls[base_url])

        # set the last time each base URL has been hit
        self.last_times = {}
        last = datetime.now().timestamp() - 2 * self.wait
        for base_url in self.urls:
            self.last_times[base_url] = last

        # What was the last base URL we hit?
        self.last_base_url = 'FAKE_URL'

    def __iter__(self):
        return self

    def __next__(self):
        # cleanup any base URLs that are now empty
        all_keys = list(self.urls.keys())
        for k in all_keys:
            if not len(self.urls[k]):
                del self.urls[k]

        # Do we need to stop iteration?
        if not len(self.urls):
            raise StopIteration

        # Okay, we need to iterate over something, pick a random element
        new_keys = set(self.urls.keys()) - {self.last_base_url}
        if not len(new_keys):
            # if there is only one base URL left
            new_key = self.last_base_url
        else:
            # If there are multiple base URLs left, choose one that hasn't been hit lately.
            oldest_time = min(self.last_times[u] for u in new_keys)
            lonliest_urls = [u for u in new_keys if self.last_times[u] == oldest_time]
            new_key = choice(lonliest_urls)

        # Wait, if need be.
        if new_key == self.last_base_url or (datetime.now().timestamp() - self.last_times[new_key]) < self.wait:
            sleep(self.wait + 0.25 * self.wait * random())

        # FINALLY, return the next URL
        self.last_times[new_key] = datetime.now().timestamp()
        self.last_base_url = new_key
        return self.urls[new_key].pop().strip()


if __name__ == '__main__':
    main()
