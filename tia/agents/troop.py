"""
Definition of the mother class of all troops.
Troops are placable, movable drowable and reportable agents.

"""
from itertools  import chain
from tia.coords import Coords
from tia.agents import Agent
from tia.mixins import Placable, Movable, Drawable, Reportable



class Troop(Placable, Movable, Drawable, Reportable, Agent):
    """
    """

    def __init__(self, coords, name=None):
        Agent.__init__(self, name)
        Placable.__init__(self, coords)
        Movable.__init__(self)
        Drawable.__init__(self, None)
        Reportable.__init__(self)

    def __str__(self):
        return Agent.__str__(self)

    @property
    def _bases(self):
        """Return generator of bases"""
        return set(chain(self.__class__.__bases__, Troop.__bases__))


