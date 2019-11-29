""" Morgue Parser

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
from datetime import datetime
from bz2 import BZ2File
from random import choice
import requests
from sys import argv
from known_morgues import KnownMorgues
from url_iterator import URLIterator

# CONSTANTS (PROBABLY TO BE MOVED TO CLASS VARIABLES)
LOSERS = 'losers_'
MORGUE_LIST = 'morgue_urls_'
PARSER_ERRORS = 'parser_errors_'
WINNERS = 'winners_'
DATA_DIR = 'data'
DT_FMT = '%Y%m%d_%H%M%S'


# TODO: create a callable non-main function
def main():
    # the user will pass in some file filled with links / paths to morgues
    urls = []
    for master_file in argv[1:]:
        if master_file.endswith('.bz2'):
            binary_urls = BZ2File(master_file, 'r').readlines()
            urls += [u.decode('utf-8') for u in binary_urls]
        else:
            urls += open(master_file, 'r').readlines()

    # init new output files
    dt_now = current_datetime_string()
    wf = os.path.join(DATA_DIR, '{0}{1}.txt'.format(WINNERS, dt_now))
    lf = os.path.join(DATA_DIR, '{0}{1}.txt'.format(LOSERS, dt_now))
    ef = os.path.join(DATA_DIR, '{0}{1}.txt'.format(PARSER_ERRORS, dt_now))

    # what URLs have we already seen?
    known_morgues = KnownMorgues([WINNERS, LOSERS, PARSER_ERRORS], DATA_DIR)
    known_morgues.find()

    # loop through each morgue file/URL and parse it, save the results to files
    url_iter = URLIterator(urls)
    for url in url_iter:
        print(url)
        # make sure we haven't already parsed this morgue
        if known_morgues.includes(url):
            continue

        # parse the file and write any results to output files
        try:
            # parse the text file or HTML link
            if url.startswith('http'):
                txt = read_url(url)
            else:
                txt = read_file(url)

            spec, back, god, runes, ver = parse_one_morgue(txt)
            open(wf, 'a+').write('{0}  {1}{2}^{3},{4},{5}\n'.format(url.strip(), spec, back, god, runes, ver))
        except Loser:
            open(lf, 'a+').write('{0}\n'.format(url.strip()))
        except ParserError as e:
            open(ef, 'a+').write('{0}  ParserError{1}\n'.format(url.strip(), str(e).replace('\n', '    ')))
        except Exception as e:
            open(ef, 'a+').write('{0}  UnknownError{1}\n'.format(url.strip(), str(e).replace('\n', '    ')))

def read_url(url):
    """ Read the text from a URL

    Args:
        url (str): HTML address for a morgue file
    Returns:
        str: content of the URL
    """
    user_agents = ['Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Custom']

    r = requests.get(url.strip(), headers={'User-Agent': choice(user_agents)}, timeout=10)
    return r.content.decode("utf-8")

def read_file(file_path):
    """ Read the text from a file

    Args:
        file_path (str): path to the morgue file
    Returns:
        str: content of the file
    """
    return open(file_path.strip(), 'r').read()


def parse_one_morgue(txt):
    """ Parse the text of a single morgue file, to try and determine:
    1. Did the player win this game?
    2. If so, what was their character build, how many runes did they get?

    Args:
        txt (str): full text dump of morgue file
    Returns:
        tuple: species, background, god, num_runes, version
    """
    txt = strip_html(txt)

    lines = txt.split('\n')[:20]
    if len(lines) < 13:
        print(txt)
        print(lines)
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


def current_datetime_string():
    """ Get the current datetime in a simple format useful for file names

    Returns:
        str: current datetime, to the second
    """
    return datetime.now().strftime(DT_FMT)


class Loser(Exception):
    pass


class ParserError(Exception):
    pass


# Below are the data for all valid character build types, mapped to the shorthands players use.
SPECIES = {'barachian': 'Br', 'black draconian': 'Dr', 'centaur': 'Ce', 'deep dwarf': 'DD', 'deep elf': 'DE',
           'demigod': 'Dg', 'demonspawn': 'Ds', 'djinni': 'Dj', 'draconian': 'Dr', 'felid': 'Fe', 'formicid': 'Fo',
           'gargoyle': 'Gr', 'ghoul': 'Gh', 'green draconian': 'Dr', 'grey draconian': 'Dr', 'grotesk': 'Gr',
           'halfling': 'Ha', 'high elf': 'HE', 'hill orc': 'HO', 'human': 'Hu', 'kobold': 'Ko', 'lava orc': 'LO',
           'merfolk': 'Me', 'minotaur': 'Mi', 'mottled draconian': 'Dr', 'mountain dwarf': 'MD', 'mummy': 'Mu',
           'naga': 'Na', 'octopode': 'Op', 'ogre': 'Og', 'pale draconian': 'Dr', 'purple draconian': 'Dr',
           'red draconian': 'Dr', 'sludge elf': 'SE', 'spriggan': 'Sp', 'tengu': 'Te', 'troll': 'Tr', 'vampire': 'Va',
           'vine stalker': 'VS', 'white draconian': 'Dr', 'yellow draconian': 'Dr'}
SPECIES_ABR = {v.lower(): v for v in SPECIES.values()}

BACKGROUNDS = {'abyssal': 'AK', 'abyssal knight': 'AK', 'air': 'AE', 'air elementalist': 'AE', 'arcane': 'AM',
               'arcane marksman': 'AM', 'artificer': 'Ar', 'assassin': 'As', 'berserker': 'Be', 'chaos': 'CK',
               'chaos knight': 'CK', 'conjurer': 'Cj', 'death': 'DK', 'death knight': 'DK', 'earth': 'EE',
               'earth elementalist': 'EE', 'enchanter': 'En', 'fighter': 'Fi', 'fire': 'FE', 'fire elementalist': 'FE',
               'gladiator': 'Gl', 'healer': 'He', 'hunter': 'Hu', 'ice': 'IE', 'ice elementalist': 'IE', 'monk': 'Mo',
               'necromancer': 'Ne', 'paladin': 'Pa', 'priest': 'Pr', 'reaver': 'Re', 'skald': 'Sk', 'stalker': 'St',
               'summoner': 'Su', 'thief': 'Th', 'transmuter': 'Tm', 'venom': 'VM', 'venom mage': 'VM',
               'wanderer': 'Wn', 'warper': 'Wr', 'wizard': 'Wz'}
BACKGROUNDS_ABR = {b.lower(): b for b in BACKGROUNDS.values()}

GODS = {'ashenzari': 'Ash', 'beogh': 'Beo', 'cheibriados': 'Chei', 'council': 'Wu', 'dithmenos': 'Dith',
        'elyvilon': 'Ely', 'fedhas': 'Fed', 'fedhas madash': 'Fed', 'gozag': 'Goz', 'gozag ym sagoz': 'Goz',
        'hepliaklqana': 'Hep', 'jian': 'Wu', 'jiyva': 'Jiyva', 'kikubaaqudgha': 'Kik', 'lugonu': 'Lug',
        'madash': 'Fed', 'makhleb': 'Mak', 'muna': 'Sif', 'nemelex': 'Nem', 'nemelex xobeh': 'Nem', 'okawaru': 'Oka',
        'one': 'TSO', 'pakellas': 'Pak', 'qazlal': 'Qaz', 'qazlal stormbringer': 'Qaz', 'ru': 'Ru', 'sagoz': 'Goz',
        'shining': 'TSO', 'shinning': 'TSO', 'sif': 'Sif', 'sif muna': 'Sif', 'stormbringer': 'Qaz',
        'the shining one': 'TSO', 'the wu jian council': 'Wu', 'trog': 'Trog', 'uskayaw': 'Usk', 'vehumet': 'Veh',
        'wu': 'Wu', 'xobeh': 'Nem', 'xom': 'Xom', 'ym': 'Goz', 'yredelemnul': 'Yred', 'zin': 'Zin'}
GODS_ABR = {g.lower(): g for g in GODS.values()}



if __name__ == '__main__':
    main()
