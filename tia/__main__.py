

from tia.agents         import Squad
from tia.coords         import Coords
from tia.engine         import Engine
from tia.commands       import PrintCommand, MoveCommand, QuitCommand
from tia.gui            import WorldView
from random import randint
from tia.gui.terminal   import test
import tia.commons as commons


LOGGER = commons.logger()

test()
exit()


# initialization
engine = Engine()
engine.start()  # thread start
gui = WorldView(engine)
engine.register_observer(gui)
gui.start()

test()

gui.join()
engine.join()  # wait the end


