import math


class Coords:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, othr):
        return Coords(self.x + othr.x, self.y + othr.y)

    def __eq__(self, othr):
        return self.x == othr.x and self.y == othr.y

    def __str__(self):
        return '(' + str(self.x) + ';' + str(self.y) + ')'

    def __iter__(self):
        return iter((self.x, self.y))

    def square_distance_to(self, othr):
        assert(isinstance(othr, Coords))
        return (othr.x - self.x)**2 + (othr.y - self.y)**2

    def distance_to(self, othr):
        return math.sqrt(self.square_distance_to(othr))


