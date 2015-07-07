

from tia.agents         import Squad
from tia.coords         import Coords
from tia.engine         import Engine
from tia.commands       import PrintCommand, MoveCommand, QuitCommand
from tia.gui            import WorldView
from random import randint


if True:
    # initialization
    engine = Engine()
    engine.start()  # thread start
    gui = WorldView(engine)
    engine.register_observer(gui)
    gui.run()
    engine.join()  # wait the end

else:
    # initialization
    engine = Engine()
    u = Squad('Alpha', Coords(0, 0))

    # printings and start engine thread
    print('Press return key for continue, write something before for quit')
    engine.start()  # thread start

    # main loop
    input('')
    engine.add_command(MoveCommand(u, target=Coords(4, 1)))
    while not input(''):
        engine.add_command(MoveCommand(
            u, target=Coords(randint(0,10), randint(0,10))
        ))

    # quit command and wait for engine end
    engine.add_command(QuitCommand())
    engine.join()


