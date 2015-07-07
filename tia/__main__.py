

from tia.agents         import Squad
from tia.coords         import Coords
from tia.engine         import Engine
from tia.commands       import PrintCommand, MoveCommand, QuitCommand


# initialization
e = Engine()
p = e.invoker
u = Squad('Alpha', Coords(0, 0))

# printings and start engine thread
print('Press return key for continue, write something before for quit')
e.start()  # thread start

# main loop
input('')
e.add_command(MoveCommand(0.0, u, target=Coords(4, 1)))
while not input(''):
    from random import randint
    e.add_command(MoveCommand(0.0, u, target=Coords(randint(0,10), randint(0,10))))

# quit command and wait for engine end
e.add_command(QuitCommand(0.0))
e.join()


