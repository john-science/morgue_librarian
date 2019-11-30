# TODO: Change the name of this file to "data.py"?


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


# Constants useful in HTML requests
USER_AGENTS = ['Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
               'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',
               'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0',
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
               'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
               'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
               'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
               'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
               'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
               'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
               'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
               'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
               'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
               'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
               'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
               'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
               'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
               'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
               'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
               ]

