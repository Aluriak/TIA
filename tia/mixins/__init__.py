"""
Interface for mixins.

Import automatically all mixins defined in files in the directory.
"""
# import all classes in mixins directory
import os
import importlib
from tia.commons import module_classes

globals().update(module_classes(__name__))



