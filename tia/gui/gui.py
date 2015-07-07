# -*- coding: utf-8 -*-
"""
Graphical representation of the game.
Commands:
    ESC: quit
    ESPACE or ENTER: add a Squad at mouse position
    DELETE: remove Point at mouse position

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
import itertools
import functools
import pyglet
import types




#########################
# PRE-DECLARATIONS      #
#########################
INTERFACE_TIME_SPEED  = 0.01
SIMULATION_FPS        = 10
VIDEO_MODE_X          = 100
VIDEO_MODE_Y          = 100
UNIVERSE_DEFAULT_SIZE = (VIDEO_MODE_X, VIDEO_MODE_Y)
MOUSE_PRECISION       = 20.
WINDOW                = None  # access to the window
ENGINE                = None  # access to the engine
MOUSE_POSITION        = None
SELECTION             = None  # selected agent




###############################################################################
# PUBLIC FUNCTIONS
###############################################################################
def run():
    """launch the pyglet event handler

    start function needs to be called first"""
    # run pyglet printings
    pyglet.app.run()
    pyglet.app.exit()



def update(*args, **kwargs):
    """part of Observer pattern"""
    pass



def init(engine):
    """create the pyglet window, initialize all"""
    global WINDOW
    # windowing
    WINDOW = pyglet.window.Window(
        width=VIDEO_MODE_X, height=VIDEO_MODE_Y,
        caption=PACKAGE_NAME
    )
    WINDOW.engine = engine
    WINDOW.update = update
    WINDOW.run    = run

    @WINDOW.event
    def on_key_press(symbol, modifiers):
        if symbol == key.RETURN or symbol == key.SPACE: # add Squad
            if MOUSE_POSITION is not None:
                _add_squad(WINDOW.engine, Coords(*MOUSE_POSITION))
        elif symbol in (key.S,):
            _snapshot()
        elif symbol == key.DELETE:  # del point
            if MOUSE_POSITION is not None:
                _delPoint(_getPointAt(*MOUSE_POSITION))
        elif symbol == key.ESCAPE:
            WINDOW.engine.add_command(QuitCommand())

    @WINDOW.event
    def on_mouse_motion(x, y, dx, dy):
        global MOUSE_POSITION
        MOUSE_POSITION = (x, y)

    @WINDOW.event
    def on_mouse_press(x, y, buttons, modifiers):
        global MOUSE_POSITION, SELECTION
        MOUSE_POSITION = (x, y)
        if buttons == pyglet.window.mouse.LEFT:
            SELECTION = _agent_at(x, y)
            print(SELECTION, 'at', Coords(x, y))
        elif buttons == pyglet.window.mouse.RIGHT and SELECTION is not None:
            WINDOW.engine.add_command(MoveCommand(SELECTION, Coords(x, y)))

    @WINDOW.event
    def on_mouse_release(x, y, buttons, modifiers):
        global MOUSE_POSITION
        MOUSE_POSITION = (x, y)

    @WINDOW.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        MOUSE_POSITION = (x, y)

    @WINDOW.event
    def on_draw():
        WINDOW.clear()
        _draw_agents()


    def schedule_wrap(f):
        def wrapper(_):
            f()
        return wrapper
    pyglet.clock.schedule_interval(schedule_wrap(on_draw), 0.1)

    return WINDOW




###############################################################################
# DRAWING
###############################################################################
def _draw_agents():
    """Print current state of engine"""
    if len(WINDOW.engine.agents) == 0: return
    agents = WINDOW.engine.agents_with((Placable,))
    agents, coords = zip(*tuple((a, a.coords) for a in agents))
    coords = tuple(itertools.chain(*coords))

    pyglet.graphics.draw(len(tuple(agents)), pyglet.gl.GL_POINTS,
                             ('v2i', coords),
                        )



###############################################################################
# PRIVATE FUNCTIONS : WRAPPER FOR HIGH LEVEL ACTIONS
###############################################################################
def _add_squad(engine, coords=None):
    """Add a random point in DT"""
    if coords is None:
        coords = Coords(randint(0,VIDEO_MODE_X),
                        randint(0,VIDEO_MODE_Y))
    engine.add_agent(Squad('Alpha', coords))


def _delPoint(point):
    """Delete given Point"""
    global dt, dragged_point
    if point is not None:
        if dragged_point == point:
            dragged_point = None
        dt.delTrianguledObject(point)


def _agent_at(x, y):
    """Return agent that is at given coordinates (about MOUSE_PRECISION)"""
    try:
        # take the first placable agent returned by engine
        return next(WINDOW.engine.agents_at(Coords(x, y), precision=10.))
    except StopIteration:
        return None


def _movePoint(x, y, p):
    """Add given values to (x;y) of given point"""
    global dt
    if p is not None:
        dt.movTrianguledObject(p, (x, y))


def _moveAllPoints():
    """Move all vertices by a small move"""
    global dt, dragged_point
    for v in dt.trianguledObjects():
        eps = 1
        mx = choice([-eps,eps])
        my = choice([-eps,eps])
        if v is not dragged_point:
            dt.movTrianguledObject(v, (mx, my))


def _snapshot():
    global dt
    print('\nsnapshot:')
    for c in (o.coordinates() for o in dt.trianguledObjects()):
        print('\t_addPointToDT' + str((c.x, c.y)))




