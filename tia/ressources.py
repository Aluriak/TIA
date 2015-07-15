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


NOUNS = tuple(set((
    'animal',
    'approval',
    'atom',
    'beaver',
    'bus shelter',
    'bread',
    'cat',
    'colored',
    'connection',
    'day',
    'walker',
    'michel',
    'mood',
    'music',
    'nothing',
    'pastafarist',
    'person',
    'octopus',
    'odyssey',
    'orange',
    'seal',
    'server',
    'solar',
    'space',
    '64',
    'slave',
)))

ADJECTIVES = tuple(set((
    'absolute',
    'approving',
    'blue',
    'commander',
    'commodor',
    'controlable',
    'clockwork',
    'drawing',
    'dreaming',
    'drooling',
    'enraging',
    'inefficient',
    'flying',
    'forgiving',
    'fool',
    'grooving',
    'growing',
    'globbing',
    'hiding',
    'little',
    'master',
    'mister',
    'mysterious',
    'orange',
    'questionnable',
    'red',
    'remote',
    'speaking',
    'tumbling',
)))

NAME_FIRSTS = tuple(set((
    'our',
    'the',
))) + ADJECTIVES


def once(x):
    """True once an x"""
    return randint(0, x) == 0

def random_player_name():
    """Return a generated name"""
    subtitle = once(2)
    origin   = once(2)
    name = (
        choice(NAME_FIRSTS).title()
        + ' ' + choice(ADJECTIVES)
        + ' ' + choice(NOUNS)
    )
    if subtitle:
        name += ', the ' + choice(ADJECTIVES) + ' '  + choice(NOUNS)
    if origin:
        name += ' of '  + choice(ADJECTIVES) + ' ' + choice(NOUNS)
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




