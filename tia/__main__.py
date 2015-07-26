

from tia.agents         import Squad
from tia.coords         import Coords
from tia.engine         import Engine
from tia.commands       import PrintCommand, MoveCommand, QuitCommand
from tia.gui            import WorldView, TerminalManagementInterface
from random             import randint
import tia.commons as commons


LOGGER = commons.logger()


# initialization
engine = Engine(Coords(100, 100))
engine.start()  # thread start
gui  = WorldView(engine)
term = TerminalManagementInterface(engine, 'lucas')
engine.register_observer(gui)

gui.start()
term.run()


gui.join()
engine.join()  # wait the end


