"""
Definition of an Agent object, that is a mixin
common to all objects in the game.

"""
from tia.coords     import Coords
from tia.ressources import random_agent_name


class Agent:
    """
    """

###############################################################################
# CONSTRUCTION
###############################################################################
    def __init__(self, name=None, player=None):
        if name is None:
            name = random_agent_name()
        self.name = name
        self.player = player

    def _update(self, _):
        """Called at each game step. Call update method of all bases, except Agent itself."""
        pass

    def update(self, engine):
        """Interface for update pattern, calling all _update() methods of self bases"""
        for base in self._bases:
            if base is not Agent:
                base._update(self, engine)


    @property
    def drawable(self):   return False
    @property
    def placable(self):   return False
    @property
    def movable(self):    return False
    @property
    def reportable(self): return False

###############################################################################
# INTERFACE WITH OTHER OBJECTS
###############################################################################
    def __str__(self):
        bases = (base for base in self._bases
                 if not issubclass(base, Agent))
        return (
            self.__class__.__name__ + ' ' + self.name + ' '
            + ' '.join(base.__str__(self) for base in bases)
        )

    @property
    def _bases(self):
        """Return bases"""
        return self.__class__.__bases__
