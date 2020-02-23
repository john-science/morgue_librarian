""" fsim.py

Purpose:

This is just a down-and-dirty version of fsim that doesn't take brands into account.
It doesn't really belong in MorgueLibrarian.

The math here doesn't really apply to the early game.

Usage:

    python fsim.py base_damage STR weapon_skill fighting_skill, enchant, slaying

"""
from sys import argv


def main():
    if len(argv) < 7:
        usage()

    print_damage(damage(int(argv[1]), int(argv[2]), int(argv[3]), int(argv[4]), int(argv[5]), int(argv[6])))


def damage(base_damage, strength, weapon_skill, fighting_skill, enchant, slaying):
    str_mod = [1., (39. + ((((strength - 8)/2.)-1)*2)) / 39., (39. + (((strength - 8)-1)*2)) / 39.]
    weapon_mod = [1., (2499. + ((100 * weapon_skill +1)/2.))/2500., (2499 + (100 * weapon_skill +1))/2500.]
    fighting_mod = [1., (3999. + ((100 * fighting_skill +1)/2.)) / 4000., (3999. + (100 * fighting_skill +1)) / 4000.]
    eff_enchant = enchant + slaying
    eff_enchant = [0, (enchant + slaying)/2. - 1, enchant + slaying - 1]

    mind = (eff_enchant[0])
    expd = (((base_damage * str_mod[1] + 1)/2. - 1) * weapon_mod[1] * fighting_mod[1] + eff_enchant[1])
    maxd = (((base_damage * str_mod[2] + 1) - 1) * weapon_mod[2] * fighting_mod[2] + eff_enchant[2])

    return mind, expd, maxd


def print_damage(tup):
    print('min\texpected\tmax')
    print('%1.0f' % tup[0] + '\t' + '%3.1f' % tup[1] + '\t\t' + '%3.1f' % tup[2])


def usage():
    """ Print a help menu to the screen, if the user enters a bad command line flag. """
    print(__doc__)
    exit()


if __name__ == '__main__':
    main()
