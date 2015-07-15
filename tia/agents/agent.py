# -*- coding: utf-8 -*-
"""
Definition of an Agent object, that is a printable object with some attributes
commons to all objects in the game.

"""
from tia.coords     import Coords
from tia.ressources import random_agent_name




class Agent:
    """
    """

###############################################################################
# CONSTRUCTION
###############################################################################
    def __init__(self, name=None):
        if name is None:
            name = random_agent_name()
        self.name = name

    @property
    def movable(self):  return False
    @property
    def placable(self): return False
    @property
    def drawable(self): return False

###############################################################################
# INTERFACE WITH OTHER OBJECTS
###############################################################################
    @property
    def x(self): return self.coords.x
    @property
    def y(self): return self.coords.y

    def __add__(self, othr):
        if isinstance(othr, Coords):
            return self.coords + othr

    def __str__(self):
        bases = (base for base in self.__class__.__bases__
                 if base is not Agent)
        return (
            self.__class__.__name__ + ' ' + self.name + ' '
            + ' '.join(base.__str__(self) for base in bases)
        )


