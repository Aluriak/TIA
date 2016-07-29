

from tia.agents         import Squad
from tia.coords         import Coords
from tia.engine         import Engine
from tia.commands       import PrintCommand, MoveCommand, QuitCommand
from tia.gui            import WorldView, TerminalManagementInterface
import tia.commons as commons
import random
import time


LOGGER = commons.logger()


def test_whole():
    # initialization
    engine = Engine(Coords(800, 600))
    engine.start()  # thread start
    gui  = WorldView(engine)
    term = TerminalManagementInterface(engine, 'lucas')
    engine.register_observer(gui)

    gui.start()
    term.run()  # block


    gui.join()
    engine.join()  # wait the end




def test_report():
    class MockAgent():
        def __init__(self):
            self.coords = random.randint(10, 500), random.randint(10, 500)
    class MockEngine():
        def __init__(self):
            self.agents = [MockAgent() for _ in range(10)]
            self.agents = []
        def add_command(self, command):
            print('Engine receive', command)
        def agents_with(self, whatever):
            return self.agents
        def agents_at(self, coords, precision=1.0):
            try:
                return iter([random.choice(self.agents)])
            except IndexError:
                return None
    engine = MockEngine()
    engine.space_width = 800
    engine.space_height= 600

    # create and test the world view object
    wv = WorldView(engine)
    wv.start()
    for _ in range(10):
        wv.update({
            'new_report': MockAgent()
        })
        time.sleep(0.4)


if __name__ == "__main__":
    # test_whole()
    test_report()
