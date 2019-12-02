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
