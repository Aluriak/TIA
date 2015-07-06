"""
"""
import threading
from tia.coords import Coords
from tia.priority_queue import PriorityQueue


class Engine(threading.Thread):
    """
    """

###############################################################################
# CONSTRUCTION AND USAGE
###############################################################################
    def __init__(self):
        super().__init__()
        self.terminated = False
        self.invoker    = PriorityQueue(self)

    def run(self):
        while not self.terminated:
            self.invoker.execute_next()

    def add_command(self, command):
        self.invoker.put(command)

###############################################################################
# GAME ENGINE API
###############################################################################
    def say(self, message):
        print('Gimme the ' + message + ' !')

    def move_to_target(self, unit):
        def sign(x): return 1 if x > 0 else (-1 if x < 0 else 0)
        unit.coords = unit.coords + Coords(
            sign(unit.target.x - unit.coords.x),
            sign(unit.target.y - unit.coords.y),
        )
        print(str(unit) + ' is at ' + str(unit.coords))
        return unit.coords == unit.target

    def quit(self):
        print('Quit !')
        self.terminated = True





