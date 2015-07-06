# -*- coding: utf-8 -*-
"""
Definition of a Unit object, that is a printable object with some attributes
commons to all objects in the game.

"""
from tia.coords import Coords




class Unit:
    """
    """

###############################################################################
# CONSTRUCTION
###############################################################################
    def __init__(self, name, coords):
        assert(isinstance(coords, Coords))
        self.coords = coords
        self.name   = name

    @property
    def movable(self): return False

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
        return self.name

