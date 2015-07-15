# -*- coding: utf-8 -*-
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
from tia.mixins      import Placable
from tia.coords      import Coords
from tia.commands    import MoveCommand, QuitCommand
from tia.agents      import Squad
from pyglet.window   import key
from pyglet.window   import mouse
import threading
import itertools
import functools
import pyglet
import types




#########################
# PRE-DECLARATIONS      #
#########################
INTERFACE_TIME_SPEED  = 0.1
VIDEO_MODE_X          = 100
VIDEO_MODE_Y          = 100
UNIVERSE_DEFAULT_SIZE = (VIDEO_MODE_X, VIDEO_MODE_Y)
MOUSE_PRECISION       = 20.




###############################################################################
# WORLD VIEW CLASS
###############################################################################
class WorldView(pyglet.window.Window, threading.Thread):

    def __init__(self, engine):
        """create the pyglet window, initialize all"""
        super().__init__(
            width=VIDEO_MODE_X, height=VIDEO_MODE_Y,
            caption=PACKAGE_NAME
        )
        threading.Thread.__init__(self)
        self.engine = engine
        self.selected_agent = None
        self.mouse_position = None

        # schedule functions calls
        def schedule_wrap(f):
            def wrapper(_):
                f()
            return wrapper
        pyglet.clock.schedule_interval(schedule_wrap(self.on_draw),
                                       INTERFACE_TIME_SPEED)

    def run(self):
        """launch the pyglet event handler

        start function needs to be called first"""
        # run pyglet printings
        pyglet.app.run()
        pyglet.app.exit()


    def update(**kwargs):
        """part of Observer pattern, updated by engine"""
        raise NotImplementedError
        # define default values, update them with given ones
        kwarg = {
            'terminated' : False,  # True if engine have quit
            'new reports': None,   # an iterable of new reports
            'new unit'   : None,   # new unit
        }.update(kwargs)



###############################################################################
# DRAWING
###############################################################################
    def on_key_press(self, symbol, modifiers):
        if symbol == key.RETURN or symbol == key.SPACE: # add Squad
            if self.mouse_position is not None:
                self._add_squad(Coords(*self.mouse_position))
        elif symbol == key.ESCAPE:
            self.on_close()

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_position = (x, y)

    def on_mouse_press(self, x, y, buttons, modifiers):
        self.mouse_position = (x, y)
        if buttons == pyglet.window.mouse.LEFT:
            self.selected_agent = self._agent_at(x, y)
        elif buttons == pyglet.window.mouse.RIGHT and self.selected_agent is not None:
            self.engine.add_command(MoveCommand(self.selected_agent, Coords(x, y)))

    def on_mouse_release(self, x, y, buttons, modifiers):
        self.mouse_position = (x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.mouse_position = (x, y)

    def on_draw(self):
        self.clear()
        self._draw_agents()

    def _draw_agents(self):
        """Print current state of engine"""
        if len(self.engine.agents) == 0: return
        agents = self.engine.agents_with((Placable,))
        agents, coords = zip(*tuple((a, a.coords) for a in agents))
        coords = tuple(itertools.chain(*coords))

        pyglet.graphics.draw(len(tuple(agents)), pyglet.gl.GL_POINTS,
                                 ('v2i', coords),
                            )

    def on_close(self):
        self.engine.add_command(QuitCommand())
        self.close()



###############################################################################
# PRIVATE FUNCTIONS : WRAPPER FOR HIGH LEVEL ACTIONS
###############################################################################
    def _add_squad(self, coords=None):
        """Add a random point in DT"""
        if coords is None:
            coords = Coords(randint(0,VIDEO_MODE_X),
                            randint(0,VIDEO_MODE_Y))
        self.engine.add_agent(Squad('Alpha', coords))

    def _agent_at(self, x, y):
        """Return agent that is at given coordinates (about MOUSE_PRECISION)"""
        try:
            # take the first placable agent returned by engine
            return next(self.engine.agents_at(Coords(x, y), precision=10.))
        except StopIteration:
            return None





