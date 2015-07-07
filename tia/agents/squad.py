"""
"""
from tia.coords import Coords
from tia.agents import Agent
from tia.mixins import Movable, Placable



class Squad(Placable, Movable, Agent):
    """
    """

    def __init__(self, name, coords):
        Agent.__init__(self, name)
        Placable.__init__(self, coords)
        Movable.__init__(self)


    def __str__(self):
        return 'Squad ' + super().__str__()
