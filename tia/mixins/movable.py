"""
"""
from tia.coords   import Coords


class Movable:
    """
    An agent is movable if its coordinates
    can be modified at each update in order to reach
    a defined target coordinates.

    Note that the mixin Placable is necessary in order
    to Movable mixin to work properly.
    """

    def __init__(self, speed=1.0, target=None):
        self.target = None
        self.speed  = speed
        assert speed >= 0.0
        assert self.placable

    def update(self, _):
        """Move at each step towards its target"""
        self.move()

    def move(self):
        """Operate a step for the unit move."""
        if self.target_reached:
            return  # nothing to do
        def sign(x):
            return 1 if x > 0 else (-1 if x < 0 else 0)
        self.coords = self.coords + Coords(
            self.speed * sign(self.target.x - self.coords.x),
            self.speed * sign(self.target.y - self.coords.y),
        )

    @property
    def movable(self):
        return True

    @property
    def target_reached(self):
        """True if unit is on its target, or if no target"""
        return self.target is None or self.target == self.coords

    def __str__(self):
        if self.target is None:
            return '[MOVABLE]'
        else:
            return '[MOVING TO ' + str(self.target) + ']'
