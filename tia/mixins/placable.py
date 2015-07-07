"""
"""
from tia.coords   import Coords
from tia.commands import MoveCommand


class Placable:
    """
    """

    def __init__(self, coords):
        assert(isinstance(coords, Coords))
        self.coords = coords

    @property
    def placable(self): return True


