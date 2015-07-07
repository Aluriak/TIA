"""
"""
import threading
from tia.coords import Coords
from tia.priority_queue import PriorityQueue
import tia.time_scheduler as time


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

    def move(self, unit):
        """Operate a step for the unit move.

        Return True iff unit reach its target.
        In this case, unit.target will be set to None.
        """
        if not unit.movable: return
        def sign(x): return 1 if x > 0 else (-1 if x < 0 else 0)
        unit.coords = unit.coords + Coords(
            sign(unit.target.x - unit.coords.x),
            sign(unit.target.y - unit.coords.y),
        )
        # debug
        print(str(unit) + ' is at ' + str(unit.coords) + ' and go to '
              + str(unit.target) + ' at ' + str(time.time()))
        # return target reached truth
        target_reached = unit.coords == unit.target
        if target_reached: unit.target = None
        return target_reached

    def quit(self):
        print('Quit !')
        self.terminated = True





