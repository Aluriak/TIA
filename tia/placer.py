"""
Definition of the Placer, that place Placable agents in space.

"""
from tia.coords         import Coords


class Placer:
    """
    Container of Placable objects. (objects with coords)
    A Placer instance contains objects, and rely them through
     their coordinates in space.
    The space is defined at the construction, as a square with origin at (0;0).

    Provides API for nearer objects retrieving.

    """

    def __init__(self, max_coords, min_coords=Coords(0, 0)):
        assert(isinstance(max_coords, Coords))
        assert(isinstance(min_coords, Coords))
        assert(max_coords.x > min_coords.x)
        assert(max_coords.y > min_coords.y)
        self.max_coords = max_coords
        self.min_coords = min_coords
        self.placables = set()

    def add(self, placable, coords=None):
        """register given placable

        if coords is not provided, the coords will be asked to the placable.
        Note that coords or placable.coords will be modified,
         if the values are not valid in space.
        """
        assert coords is None or isinstance(coords, Coords)
        if not coords:
            assert placable.coords is not None
            coords = placable.coords
        placable.coords = self.fix_coords(coords)
        self.placables.add(placable)

    def __iter__(self):
        return iter(self.placables)

    def remove(self, placable, new_coords=None):
        self.placables.remove(placable)
        placable.coords = new_coords

    def neighbors(self, coords, max_dist:float, min_dist:float=0.):
        """Yield all objects found at a dist between given minimal and maximal bounds.
        """
        square_max = max_dist * max_dist
        square_min = min_dist * min_dist
        for placable in self.placables:
            dist = coords.square_distance_to(placable.coords)
            if square_min <= dist <= square_max:
                yield placable

    def fix_coords(self, coords):
        """Return a fixed version of coords. Returned coords is valid"""
        return Coords(
            min(self.max_coords.x, max(self.min_coords.x, coords.x)),
            min(self.max_coords.y, max(self.min_coords.y, coords.y))
        )

    def __len__(self):
        return len(self.placables)
