from tia.commons      import module_classes
# these import is necessary, because all others use it
from tia.agents.agent import Agent
from tia.agents.troop import Troop
from tia.agents.squad import Squad

TROOPS = (Squad,)
# globals().update(module_classes(__name__))


