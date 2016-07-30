"""
Graphical representation of the game.
Commands:
    ESC: quit
    ESPACE or ENTER: add a squad at mouse position
    LEFT CLIC: select a squad
    RIGHT CLIC: define pixel as selected squad's target

"""


#########################
# IMPORTS               #
#########################
from tia.info        import PACKAGE_NAME
from tia.mixins      import Drawable, Movable
from tia.coords      import Coords
from tia.commands    import (ChangeMoveTargetCommand, QuitCommand,
                             TogglePauseCommand)
from tia.commands    import AddAgentCommand
from tia.agents      import Squad
from tia.report      import Report
from pyglet.window   import key
from pyglet.window   import mouse
import tia.commons as commons
import threading
import itertools
import functools
import pyglet
import random
import types
import os




#########################
# PRE-DECLARATIONS      #
#########################
INTERFACE_TIME_SPEED  = 0.1
VIDEO_MODE_X          = 600
VIDEO_MODE_Y          = 800
UNIVERSE_DEFAULT_SIZE = (VIDEO_MODE_X, VIDEO_MODE_Y)
MOUSE_PRECISION       = 20.
LOGGER                = commons.logger()




###############################################################################
# WORLD VIEW CLASS
###############################################################################
class WorldView(pyglet.window.Window, threading.Thread):

    def __init__(self, engine):
        """create the pyglet window, initialize all"""
        pyglet.window.Window.__init__(
            self,
            # width=VIDEO_MODE_X, height=VIDEO_MODE_Y,
            width=engine.space_width, height=engine.space_height,
            caption=PACKAGE_NAME
        )
        threading.Thread.__init__(self)
        self.engine = engine
        self.selected_agent = None
        self.mouse_position = None

        # load graphical ressources
        self._load_images()

        # create the batchs (groups of sprites printed together)
        self.batch           = pyglet.graphics.Batch()
        # self.batch_drawables = pyglet.graphics.OrderedGroup(0)
        # self.batch_debug     = pyglet.graphics.OrderedGroup(1)

        # In order to avoid data race, leading to a
        #  pyglet.gl.lib.GLException: b'invalid operation'
        # Sprites added by client code are pushed as
        #  partial object of constructor with all parameters set,
        #  allowing the on_draw routine to construct and add
        #  Sprite objects to the sprites container.
        self.sprite_constructors = set()  # contains all sprites constructors
        self.sprites = set()  # contains all sprites printed at screen

        # schedule functions calls
        def schedule_wrap(f):
            def wrapper(_):
                f()
            return wrapper
        pyglet.clock.schedule_interval(schedule_wrap(self.on_draw),
                                       INTERFACE_TIME_SPEED)

    def run(self):
        """launch the pyglet event handler and associated printings"""
        # run pyglet
        pyglet.app.run()
        pyglet.app.exit()

    def update(self, *args, **kwargs):
        """part of Observer pattern, updated by engine"""
        # define default values, update them with given ones
        kwarg = {
            'terminated' : False,  # True if engine have quit
            'new_report' : None,   # new unit report
            'new_unit'   : None,   # new unit
            'quit'       : False,  # True if engine is stopped
        }
        kwarg.update(**kwargs)
        kwarg.update(*args)
        if kwarg['quit']:
            self.on_close(propagate_to_engine=False)
        if kwarg['new_report']:
            assert isinstance(kwarg['new_report'], Report)
            self._show_report(kwarg['new_report'])


###############################################################################
# DRAWING
###############################################################################
    def on_key_press(self, symbol, modifiers):
        if symbol == key.RETURN or symbol == key.SPACE: # add Squad
            if self.mouse_position is not None:
                self._add_squad(Coords(*self.mouse_position))
        elif symbol == key.ESCAPE:
            self.on_close()
        elif symbol == key.P:
            self.engine.add_command(TogglePauseCommand())
        elif symbol == key.M:
            self._move_agents()

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_position = (x, y)

    def on_mouse_press(self, x, y, buttons, modifiers):
        self.mouse_position = (x, y)
        if buttons == pyglet.window.mouse.LEFT:
            self.selected_agent = self._agent_at(x, y)
            if self.selected_agent:
                print(self.selected_agent)
        elif buttons == pyglet.window.mouse.RIGHT and self.selected_agent is not None:
            self.engine.add_command(ChangeMoveTargetCommand(
                self.selected_agent, Coords(x, y)
            ))

    def on_mouse_release(self, x, y, buttons, modifiers):
        self.mouse_position = (x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.mouse_position = (x, y)

    def on_draw(self):
        # sprites, self.sprites = list(self.sprites), []
        self.sprites |= {cons() for cons in self.sprite_constructors}
        self.clear()
        # try:
        self._draw_agents()
        self.batch.draw()

    def _draw_agents(self):
        """Print current state of engine"""
        if len(self.engine.agents) == 0: return
        agents = self.engine.agents_with((Drawable,))
        agents, coords = zip(*tuple((a, a.coords) for a in agents))
        coords = tuple(itertools.chain(*coords))

        pyglet.graphics.draw(len(tuple(agents)), pyglet.gl.GL_POINTS,
                                 ('v2i', coords),
                            )

    def on_close(self, *, propagate_to_engine=True):
        self.close()
        if propagate_to_engine:
            self.engine.add_command(QuitCommand())


###############################################################################
# PRIVATE FUNCTIONS : WRAPPER FOR HIGH LEVEL ACTIONS
###############################################################################
    def _add_squad(self, coords=None):
        """Add a random point in DT"""
        if coords is None:
            coords = Coords(random.randint(0,800),
                            random.randint(0,800))
        self.engine.add_command(AddAgentCommand(Squad(coords)))

    def _show_report(self, report):
        """Add given report in the batch as sprite"""
        x, y = report.coords
        self.sprite_constructors.add(functools.partial(
            pyglet.sprite.Sprite,
            self.images['report_ally'],
            x=x, y=y,
            batch=self.batch,
            # group=self.batch_drawables
        ))

    def _agent_at(self, x, y):
        """Return agent that is at given coordinates (about MOUSE_PRECISION)"""
        agent = self.engine.agents_at(Coords(x, y), precision=10.)
        try:
            # take the first placable agent returned by engine
            return next(iter(agent))
        except (StopIteration, TypeError):
            return None

    def _move_agents(self, agents=None, coords=None):
        """Move given agents to given coords

        if no agents and no coords given, all movables agents will
         be move to a random location
        """
        if agents is None:
            for movable in self.engine.agents_with((Movable,)):
                x = random.randint(0,800)
                y = random.randint(0,600)
                self.engine.add_command(ChangeMoveTargetCommand(movable,
                                                                Coords(x, y)))
        else:
            assert(coords is not None)
            [self.engine.add_command(ChangeMoveTargetCommand(agent, target))
             for agent, target in zip(agents, coords)]

    def _load_images(self):
        """populate the list of available images"""
        self.images = {
            os.path.splitext(os.path.basename(res))[0]: pyglet.image.load(res)
            for res in commons.ressources(path=commons.DIR_IMAGES, ext='png')
        }
        LOGGER.info('GUI: Loaded images: ' + ', '.join(k for k in self.images))
