"""
"""
from random    import randint, randrange, choice
from itertools import cycle
import random
import tia.commons as commons


# names from ressources files
#  get an infinite generator
with open(commons.DIR_RESSOURCES + 'names.txt') as fd:
    NAMES = [l.strip('\n') for l in fd]
    random.shuffle(NAMES)
    NAMES = cycle(NAMES)

NOUNS_AND_ADJECTIVES = tuple(set((
    'orange',
    'pastafarist',
    'remote',
    'slave',
    'walker',
)))


NOUNS = tuple(set((
    'animal',
    'approval',
    'atom',
    'banana',
    'beaver',
    'bus shelter',
    'bread',
    'cat',
    'connection',
    'day',
    'michel',
    'mood',
    'music',
    'nothing',
    'octopus',
    'odyssey',
    'person',
    'phase',
    'seal',
    'server',
    'solar',
    'space',
    'teapot',
    'wapiti',
    '64',
))) + NOUNS_AND_ADJECTIVES

ADJECTIVES = tuple(set((
    'absolute',
    'approving',
    'blue',
    'bringer',
    'clanic',
    'colored',
    'commander',
    'commodor',
    'connected',
    'controlable',
    'clockwork',
    'drawing',
    'dreaming',
    'drooling',
    'enraging',
    'evil',
    'green',
    'geometric',
    'freudian',
    'inefficient',
    'flying',
    'forgiving',
    'fool',
    'grooving',
    'growing',
    'globbing',
    'hiding',
    'isometric',
    'little',
    'master',
    'mister',
    'mysterious',
    'paster',
    'questionnable',
    'red',
    'speaking',
    'tumbling',
    'yanker',
))) + NOUNS_AND_ADJECTIVES

NAME_FIRSTS = tuple(set((
    'our',
    'the',
)))# + ADJECTIVES

SUPERLATIFS = tuple(set((
    'very',
    'smallest',
    'slowest',
)))


def once(x):
    """True once an x"""
    return randint(0, x) == 0

def random_player_name():
    """Return a generated name"""
    first       = once(3)
    subtitle    = once(2)
    origin      = once(2)
    superlatif1 = once(3)
    superlatif2 = once(3)

    name = (
        choice(NAME_FIRSTS).title()
        + ' ' + choice(ADJECTIVES)
        + ' ' + choice(NOUNS)
    )
    if subtitle:
        name += ', the '
        if superlatif1:
            name += choice(SUPERLATIFS) + ' '
        name += choice(ADJECTIVES) + ' ' + choice(NOUNS)
    if origin:
        name += ' of '
        if superlatif2:
            name += choice(SUPERLATIFS) + ' '
        name += choice(ADJECTIVES) + ' ' + choice(NOUNS)
    shortname = ''.join(
        l[0] for l in random.sample(tuple(
            w for w in name.replace(',', '').split(' ')
            if w not in ('the', 'of')
        ), 3)
    ).upper()
    return name, shortname


def random_agent_name():
    """Return a randomly generated name that can be given to an agent"""
    return next(NAMES)




