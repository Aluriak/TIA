"""
Definition of the mother class of all troops.
"""
from tia.coords import Coords
from tia.agents import Agent
from tia.mixins import Movable, Placable, Drawable



class Troop(Placable, Movable, Drawable, Agent):
    """
    """

    def __init__(self, coords, name=None):
        Agent.__init__(self, name)
        Placable.__init__(self, coords)
        Movable.__init__(self)
        Drawable.__init__(self, None)


    def __str__(self):
        return Agent.__str__(self)
