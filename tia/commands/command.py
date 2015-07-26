# -*- coding: utf-8 -*-
"""
"""
import tia.time_scheduler as time



class Command:
    """
    """

    def __init__(self, time_shift=0.01):
        self.time = time.time() + time_shift


    def execute(self, engine):
        raise NotImplementedError

    def __lt__(self, othr):
        return self.time < othr.time

    @property
    def is_executable(self):
        return self.time <= time.time()



