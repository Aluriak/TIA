"""
"""
import threading
import itertools
from tia.coords         import Coords
from tia.priority_queue import PriorityQueue
from tia.placer         import Placer
from tia.agents         import Agent
from tia.player         import Player
from tia.mixins         import Placable
from tia.commands       import Command
from tia.report         import Report
import tia.time_scheduler as time
import tia.commons        as commons


LOGGER = commons.logger()



class Engine(threading.Thread):
    """
    """

###############################################################################
# CONSTRUCTION AND USAGE
###############################################################################
    def __init__(self, max_coords):
        super().__init__()
        self.terminated = False
        self.observers  = set()  # contains all observers
        self.containers = {  # containables and containers
            Agent  : Placer(max_coords),
            Player : set(),
            Command: PriorityQueue(self),
            Report : set(),
        }
        self.containables = tuple(self.containers.keys())
        # shortcuts to the containers
        self.invoker = self.containers[Command]
        self.players = self.containers[Player]
        self.agents  = self.containers[Agent]
        self.reports = self.containers[Report]
        LOGGER.info('Engine: initialized')


    def run(self):
        """Game loop implementation"""
        LOGGER.info('Engine: thread started')
        while not self.terminated:
            # collect actions from each agent
            for agent in self.agents:
                agent.update(self)
            # invoke actions from each agent
            self.invoker.execute_next()
            # dirty sleep avoiding a too quick game
            time.sleep(0.1)


    def add(self, obj):
        """add object to the container associated

        For instance, a command will be added to the container
        that contains commands.
        """
        # get the first recognized motherclass
        try:
            self.containers[next(
                cls for cls in self.containables
                if isinstance(obj, cls)
            )].add(obj)
        except StopIteration:
            # no valid motherclass
            LOGGER.warning('engine.add(2) receive a non valid object '
                           + str(obj) + ' of ' + str(obj.__class__))

    def add_command(self, command):
        self.invoker.put(command)

    def add_agent(self, agent):
        assert(isinstance(agent, Agent))
        self.agents.add(agent)
        self.notify_observers(new_agent=agent)

    def add_report(self, report):
        if report is None:
            # TODO: special cases where unit send nothing
            LOGGER.info("ENGINE: report 'None' received")
        else:
            if not isinstance(report, Report):
                LOGGER.error(str(report) + ' ' + str(report.__class__))
                assert(isinstance(report, Report))
            self.reports.add(report)
            self.notify_observers(new_report=report)


    def add_player(self, player):
        assert(isinstance(player, Player))
        self.players.add(player)

    def rmv_agent(self, agent):
        assert(issubclass(agent, Agent))
        try:
            self.agents.remove(agent)
        except KeyError:
            pass

    def agents_with(self, properties):
        """Return a generator of agents that have given properties"""
        return (a for a in self.containers[Agent]
                if all(isinstance(a, p) for p in properties))

    def register_observer(self, observer):
        self.observers.add(observer)

    def deregister_observer(self, observer):
        try:
            self.observers.remove(observer)
        except KeyError:
            pass

    def notify_observers(self, *args, **kwargs):
        tuple(o.update(*args, **kwargs) for o in self.observers)

###############################################################################
# GAME ENGINE API
###############################################################################
    def say(self, message):
        LOGGER.info('Engine: say: ' + message)

    def quit(self):
        self.terminated = True
        self.notify_observers({'quit': True})
        LOGGER.info('Engine: quit')

    def agents_at(self, coords, precision=1.):
        return (
            agent for agent in self.agents_with((Placable,))
            if agent.coords.distance_to(coords) <= precision
        )

    def toggle_pause(self):
        time.toggle_pause()


###############################################################################
# GAME ENGINE PROPERTIES
###############################################################################
    @property
    def space_width(self): return self.agents.max_coords.x

    @property
    def space_height(self): return self.agents.max_coords.y




