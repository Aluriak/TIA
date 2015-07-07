"""
"""
from tia.coords import Coords
from tia.agents import Agent
from tia.mixins import Movable



class Squad(Movable, Agent):
    """
    """

    def __init__(self, name, coords):
        Agent.__init__(self, name, coords)
        Movable.__init__(self)


    def __str__(self):
        return 'Squad ' + super().__str__()
