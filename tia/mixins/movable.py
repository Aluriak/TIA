"""
"""
from tia.coords   import Coords
from tia.commands import MoveCommand


class Movable:
    """
    """

    def __init__(self):
        self.target = None
        self.speed  = 1.0

    @property
    def movable(self): return True


