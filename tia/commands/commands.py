# -*- coding: utf-8 -*-
"""
"""
from tia.commands import Command
from tia.coords   import Coords
from tia.agents   import Agent



###############################################################################
# ADD AGENT
###############################################################################
class AddAgentCommand(Command):
    """
    """
    def __init__(self, agent, time_shift=0.01):
        super().__init__(time_shift)
        assert(isinstance(agent, Agent))
        assert(agent.__class__ is not Agent)
        self.agent = agent

    def execute(self, engine):
        engine.add_agent(self.agent)
        # new agent must emit its first report
        engine.add_command(EmitReportCommand(self.agent))



###############################################################################
# EMIT REPORT
###############################################################################
class EmitReportCommand(Command):
    """Add a new report to the engine, and add a new one in a number
     of seconds equals to the unit report timestamp

    """

    def __init__(self, unit, time_shift=0.01):
        super().__init__(time_shift)
        self.unit = unit

    def execute(self, engine):
        engine.add_report(self.unit.report())
        engine.add_command(EmitReportCommand(
            self.unit,
            time_shift=self.unit.report_timestamp
        ))



###############################################################################
# MOVE
###############################################################################
class RecursiveMoveCommand(Command):
    """Move unit to target. Create another instance
    of RecursiveMoveCommand for perform the next steps.
    """

    def __init__(self, time_shift, unit):
        super().__init__(time_shift)
        self.unit   = unit

    def execute(self, engine):
        """
        """
        if self.unit.target:  # target defined
            # move, and create a move action if necessary
            target_reached = engine.move(self.unit)
            if target_reached:
                self.unit.target = None
            else:  # target not reached
                engine.add_command(RecursiveMoveCommand(
                    self.unit.speed,
                    self.unit
                ))


class MoveCommand(Command):
    """Move unit to target, or stop the motion if no target
    """

    def __init__(self, unit, target=None, time_shift=0.01):
        super().__init__(time_shift)
        self.unit   = unit
        self.target = target

    def execute(self, engine):
        """
        """
        if not self.unit.movable: return
        if self.unit.target:
            # already move: get new target
            self.unit.target = self.target
        elif self.target:
            # not in moving, and new target
            assert(self.unit.target is None)
            self.unit.target = self.target
            engine.add_command(RecursiveMoveCommand(
                self.unit.speed,
                self.unit
            ))



###############################################################################
# PRINT
###############################################################################
class PrintCommand(Command):
    """
    """

    def __init__(self, message, time_shift=0.01):
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



###############################################################################
# TOGGLE_PAUSE
###############################################################################
class TogglePauseCommand(Command):
    """
    """

    def __init__(self, time_shift=0.0):
        super().__init__(time_shift)

    def execute(self, engine):
        engine.toggle_pause()




