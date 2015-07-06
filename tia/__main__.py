

from tia.units          import Squad
from tia.coords         import Coords
from tia.engine         import Engine
from tia.commands       import PrintCommand, MoveCommand, QuitCommand



e = Engine()
p = e.invoker

# for msg in ('C', 'B', 'D', 'A'):
    # sec = ord(msg) - ord('A')
    # p.put(PrintCommand(sec, msg))
# while not p.empty(): p.execute_next()

# p.put(MoveCommand(0.0, p, Coords(0,0), Coords(3,4)))
# p.put(QuitCommand(4.0))
# while not e.terminated: p.execute_next()


u = Squad('Alpha', Coords(0, 0))
e.add_command(MoveCommand(0.0, u, target=Coords(4, 1)))

print('Press return key for quit immediatly')
e.start()  # thread start

input('')
e.add_command(QuitCommand(0.0))

e.join()


