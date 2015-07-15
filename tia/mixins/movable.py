"""
"""
from tia.coords   import Coords
from tia.commands import MoveCommand


class Movable:
    """
    """

    def __init__(self, speed=0.1, target=None):
        self.target = None
        self.speed  = speed
        assert(speed >= 0.0)

    @property
    def movable(self): return True

    def __str__(self):
        if self.target is None:
            return '[MOVABLE]'
        else:
            return '[MOVING TO ' + str(self.target) + ']'

