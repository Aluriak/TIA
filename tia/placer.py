"""
Definition of the Placer, that place Placable agents in space.

"""
from tia.coords         import Coords



class Placer(dict):
    """
    Container of Placable objects. (objects with coords)
    A Placer instance contains objects, and rely them through
     their coordinates in space.
    The space is defined at the construction, as a square with origin at (0;0).

    """

    def __init__(self, max_coords, min_coords=Coords(0, 0)):
        assert(isinstance(max_coords, Coords))
        assert(isinstance(min_coords, Coords))
        assert(max_coords.x > min_coords.x)
        assert(max_coords.y > min_coords.y)
        self.max_coords = max_coords
        self.min_coords = min_coords

    def add(self, placable, coords=None):
        """add given placable in the space

        if coords is not provided, the coords will be asked to the placable.
        Note that coords or placable.coords can be modified,
         if the values are not valid in space.
        """
        assert(coords is None or isinstance(coords, Coords))
        if coords:
            coords = self.fix_coords(coords)
            self[coords.as_pair] = placable
            placable.coords = coords
        else:
            assert(placable.coords is not None)
            placable.coords = self.fix_coords(placable.coords)
            self[placable.coords.as_pair] = placable

    def __iter__(self):
        return iter(self.values())

    def remove(self, placable, new_coords=None):
        del self[placable.coords.as_pair]
        placable.coords = new_coords

    def fix_coords(self, coords):
        """Return a fixed version of coords. Returned coords is valid"""
        return Coords(
            min(self.max_coords.x, max(self.min_coords.x, coords.x)),
            min(self.max_coords.y, max(self.min_coords.y, coords.y))
        )

    def __len__(self):
        return len(self.keys())



