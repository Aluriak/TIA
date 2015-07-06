# -*- coding: utf-8 -*-
"""
"""
from tia.command import Command
from tia.coords  import Coords



###############################################################################
# MOVE
###############################################################################
class MoveCommand(Command):
    """
    """

    def __init__(self, time_shift, unit, target=None):
        super().__init__(time_shift)
        self.unit = unit
        if target is not None:
            self.unit.target = target

    def execute(self, engine):
        """
        """
        if not self.unit.movable or self.unit.target is None: return
        if engine.move_to_target(self.unit):
            self.unit.target = None
        else:  # target not reached
            engine.add_command(
                MoveCommand(self.unit.speed, self.unit)
            )



###############################################################################
# PRINT
###############################################################################
class PrintCommand(Command):
    """
    """

    def __init__(self, time_shift, message):
        super().__init__(time_shift)
        self.message = message

    def execute(self, engine):
        engine.say(self.message)



###############################################################################
# QUIT
###############################################################################
class QuitCommand(Command):
    """
    """

    def execute(self, engine):
        engine.quit()




