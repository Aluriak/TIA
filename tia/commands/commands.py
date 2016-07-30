"""
Definition of various commands, designed to be used by players.

These commands/actions should not be used internally,
and should remain very simple, typically one call to an engine method.
"""
from tia.commands import Command
from tia.coords   import Coords
from tia.agents   import Agent


DEFAULT_TIME_SHIFT = 0.00


###############################################################################
# ADD AGENT
###############################################################################
class AddAgentCommand(Command):
    """
    """
    def __init__(self, agent, time_shift=DEFAULT_TIME_SHIFT):
        super().__init__(time_shift)
        assert(isinstance(agent, Agent))
        assert(agent.__class__ is not Agent)
        self.agent = agent

    def execute(self, engine):
        engine.add_agent(self.agent)


###############################################################################
# EMIT REPORT
###############################################################################
class EmitReportCommand(Command):
    """Add a new report to the engine"""

    def __init__(self, report, time_shift=DEFAULT_TIME_SHIFT):
        super().__init__(time_shift)
        self.report = report

    def execute(self, engine):
        engine.add_report(self.report)



###############################################################################
# MOVE
###############################################################################
class ChangeMoveTargetCommand(Command):
    """Change the target of given unit"""

    def __init__(self, unit, target=None, speed=None,
                 time_shift=DEFAULT_TIME_SHIFT):
        super().__init__(time_shift)
        self.unit   = unit
        self.target = target
        self.speed  = speed

    def execute(self, engine):
        unit = self.unit
        assert unit.movable
        unit.target = self.target
        unit.speed = unit.speed if self.speed is None else self.speed


###############################################################################
# PRINT
###############################################################################
class PrintCommand(Command):
    """
    """

    def __init__(self, message, time_shift=DEFAULT_TIME_SHIFT):
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




