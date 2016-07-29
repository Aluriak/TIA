"""
Definition of the Report agent, a graphical indicator of
some agents position in space.
"""
from tia.coords import Coords
from tia.agents import Agent
import tia.time_scheduler as time



class Report:
    """
    """

    def __init__(self, unit, text=''):
        self.unit = unit
        self.text = str(text)
        self.time = time.time()
        # deductions from previous data
        self.coords = unit.coords

    def __str__(self):
        return 'Report of ' + str(self.unit) + ': ' + self.text


