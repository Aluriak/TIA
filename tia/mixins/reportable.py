"""
"""
from tia.coords   import Coords
from tia.report   import Report
import tia.time_scheduler as time



class Reportable:
    """The Reportable property allows a component to emit reports
    """

    def __init__(self, timestamp=3):
        """By default, the component emit reports all 30 seconds"""
        self.report_timestamp = timestamp
        self._actualize_report_time()

    def report(self):
        """Return a report on the current situation"""
        self._actualize_report_time()
        return Report(unit=self, text='')

    @property
    def reportable(self): return True

    @property
    def remain_report_time(self):
        return self.next_report_time - time.time()

    def _actualize_report_time(self):
        self.next_report_time = time.time() + self.report_timestamp

    def __str__(self):
        next_time = round(self.remain_report_time, 1)
        if next_time >= 0:
            return '[NEXT REPORT IN ' + str(next_time) + 's]'
        else:
            return '[REPORT LATE OF ' + str(-next_time) + 's]'



