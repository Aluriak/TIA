"""
"""
import threading
from tia.coords         import Coords
from tia.priority_queue import PriorityQueue
from tia.agents         import Agent
from tia.mixins         import Placable
import tia.time_scheduler as time
import tia.commons        as commons


LOGGER = commons.logger()



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
        self.agents     = set()  # contains all Agent
        self.observers  = set()  # contains all observers
        LOGGER.info('Engine: initialized')

    def run(self):
        LOGGER.info('Engine: thread started')
        while not self.terminated:
            self.invoker.execute_next()

    def add_command(self, command):
        self.invoker.put(command)

    def add_agent(self, agent):
        assert(isinstance(agent, Agent))
        self.agents.add(agent)

    def rmv_agent(self, agent):
        assert(issubclass(agent, Agent))
        try:
            self.agents.remove(agent)
        except KeyError:
            pass

    def agents_with(self, properties):
        return (a for a in self.agents
                if all(isinstance(a, p) for p in properties))

    def register_observer(self, observer):
        self.observers.add(observer)

    def deregister_observer(self, observer):
        try:
            self.observers.remove(observer)
        except KeyError:
            pass

    def notify_observers(self):
        map(lambda o: o.update(), self.observers)

###############################################################################
# GAME ENGINE API
###############################################################################
    def say(self, message):
        LOGGER.info('Engine: say: ' + message)

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
        # print(str(unit) + ' is at ' + str(unit.coords) + ' and go to '
              # + str(unit.target) + ' at ' + str(time.time()))
        # return target reached truth
        target_reached = unit.coords == unit.target
        if target_reached: unit.target = None
        return target_reached

    def quit(self):
        LOGGER.info('Engine: quit')
        self.terminated = True

    def agents_at(self, coords, precision=1.):
        return (
            agent for agent in self.agents_with((Placable,))
            if agent.coords.distance_to(coords) <= precision
        )





