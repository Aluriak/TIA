"""
"""
from tia.coords import Coords
from tia.agents import Troop
from tia.mixins import Movable, Placable, Drawable



class Squad(Troop):
    """
    """

    def __init__(self, coords, name=None):
        Troop.__init__(self, coords, name)

