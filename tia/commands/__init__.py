from tia.commons          import module_classes
from tia.commands.command import Command

def keep_class(cls): return issubclass(cls, Command)
globals().update(module_classes(__name__, keepif=keep_class))


