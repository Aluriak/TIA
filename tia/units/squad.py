"""
"""
from tia.coords import Coords
from tia.units  import Unit
from tia.mixins import Movable



class Squad(Movable, Unit):
    """
    """

    def __init__(self, name, coords):
        Unit.__init__(self, name, coords)
        Movable.__init__(self)


    def __str__(self):
        return 'Squad ' + super().__str__()
