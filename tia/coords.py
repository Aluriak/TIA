


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


