"""
Definition of the priority queue of commands applied on the engine.

"""
import queue
import tia.time_scheduler as time


class PriorityQueue(queue.PriorityQueue):
    """
    Subclass that introduce a big miss in the original API and a
    quick access to the engine.


    """

    def __init__(self, target):
        super().__init__()
        self.target = target

    def execute_next(self):
        """Execute next command on target iff command execution time is coming
        """
        command = self.get(block=True)
        while not command.is_executable:
            self.put(command)
            time.sleep(0.01)
            command = self.get(block=True)
        command.execute(self.target)

    def add(self, command):
        """alias for put method"""
        return self.put(command)
