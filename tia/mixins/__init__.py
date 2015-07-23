"""
Interface for mixins.

Import automatically all mixins defined in files in the directory.
"""
# import all classes in mixins directory
import os
import importlib
from functools import partial
from tia.info  import PACKAGE_NAME

# all files in this directory
modules = (
    __name__ + '.' + name
    for name, ext in (
        os.path.splitext(filename)
        for filename in os.listdir(__name__.replace('.', '/'))
    )
    if ext == '.py' and not name.startswith('__')
)

# declare a new function, shortcut to the importlib one
imported = partial(importlib.import_module, package=PACKAGE_NAME)

# import all classes in the modules
globals().update({
    n:cls
    for module in modules
    for n, cls in imported(module).__dict__.items()
    # cls is a class, defined in the tia.mixins package
    if type(cls) is type and __name__ in cls.__module__
})



