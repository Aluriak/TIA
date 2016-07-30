"""
"""
from tia.coords import Coords
from tia.agents import Troop


class Squad(Troop):
    """
    """

    def __init__(self, coords, name=None, player=None):
        Troop.__init__(self, coords, name, player)

    def _update(self, engine):
        Troop._update(self, engine)
