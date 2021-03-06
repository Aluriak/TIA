"""
"""

from tia.coords import Coords
from tia        import report
from tia        import commands
import tia.time_scheduler as time


class Reportable:
    """The Reportable property allows a component to emit reports
    """

    def __init__(self, timestamp=3):
        """By default, the component emit reports all 30 seconds"""
        self.report_timestamp = timestamp
        self.next_report_texts = []
        self.highest_report_priority = 0
        self.last_report = None
        self._actualize_report_time()

    def _update(self, engine):
        """Send a report if its time"""
        if self.remain_report_time < 0:
            self.last_report = self.report()
            engine.add_report(self.last_report)

    def add_to_next_report(self, text:str, *, priority=report.Priority.normal):
        """Add given text into next report"""
        self.next_report_texts.append(text)
        if priority > self.highest_report_priority:
            self.highest_report_priority = priority

    def report(self):
        """Return a report on the current situation"""
        self._actualize_report_time()
        return report.Report(unit=self, text='\n'.join(self.next_report_texts),
                             priority=self.highest_report_priority)

    @property
    def reportable(self):
        return True

    @property
    def remain_report_time(self):
        return self.next_report_time - time.time()

    def _actualize_report_time(self):
        self.next_report_time = time.time() + self.report_timestamp

    def __str__(self):
        remain_time = round(self.remain_report_time, 1)
        if remain_time > 0:
            return '[NEXT REPORT IN ' + str(remain_time) + 's]'
        else:
            return '[REPORT LATE OF ' + str(-remain_time) + 's]'
