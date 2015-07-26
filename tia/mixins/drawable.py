"""
"""
from tia.coords   import Coords



class Drawable:
    """
    """

    def __init__(self, sprite):
        self.sprite = sprite

    @property
    def drawable(self): return True

    def __str__(self):
        return '[DRAWABLE]'


