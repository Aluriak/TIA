"""
"""
from random import randint, randrange, choice
import random



nouns = tuple(set((
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

adjectives = tuple(set((
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

name_firsts = tuple(set((
    'our',
    'the',
))) + adjectives

def once(x):
    """True once an x"""
    return randint(0, x) == 0

def random_name():
    """Return a generated name"""
    subtitle = once(2)
    origin   = once(2)
    name = (
        choice(name_firsts).title()
        + ' ' + choice(adjectives)
        + ' ' + choice(nouns)
    )
    if subtitle:
        name += ', the ' + choice(adjectives) + ' '  + choice(nouns)
    if origin:
        name += ' of '  + choice(adjectives) + ' ' + choice(nouns)
    shortname = ''.join(
        l[0] for l in random.sample(tuple(
            w for w in name.replace(',', '').split(' ')
            if w not in ('the', 'of')
        ), 3)
    ).upper()
    return name, shortname



