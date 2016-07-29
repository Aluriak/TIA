"""
Definition of the Report agent, a graphical indicator of
some agents position in space.
"""
from tia.coords import Coords
from tia.agents import Agent
import tia.time_scheduler as time

from enum import Enum


class Priority(Enum):
    """Two Report priorities level:
    - high is for "must be sent now"
    - normal is for "should be sent with the next report"

    """
    high = 3
    normal = 2


class Report:
    """
    """

    def __init__(self, unit, text='', priority=Priority.normal):
        self.unit = unit
        self.text = str(text)
        self.time = time.time()
        self.priority = priority
        # deductions from previous data
        self.coords = unit.coords

    def __str__(self):
        return 'Report of ' + str(self.unit) + ': ' + self.text

    def __gt__(self, othr):
        return self.priority > othr.priority
