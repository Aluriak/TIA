"""
"""
from tia.coords   import Coords


class Placable:
    """
    An agent is placable when have a place in the world,
    i.e. coordinates.
    """

    def __init__(self, coords):
        assert(isinstance(coords, Coords))
        self.coords = coords

    @property
    def placable(self):
        return True

    def __str__(self):
        return '[' + str(self.coords) + ']'

