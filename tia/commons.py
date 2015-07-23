# -*- coding: utf-8 -*-

import os
import importlib
from functools  import partial
from tia.info   import PACKAGE_NAME
from tia.logger import logger, log_level


# Directory and file paths
DIR_DATA       = 'data/'
DIR_RESSOURCES = DIR_DATA + 'ressources/'
LOGGER         = logger()


# Function that can be used for automatic import of classes
def module_classes(module_name, recursive=False):
    """Return a dict str:type that contains all classes
    (name:class) defined in files in the same directory.

    If recursive is True, all directories under are explored.
    """
    if recursive:
        LOGGER.warning('tia.commons.module_classes(2):'
                       + 'recursive option is not implemented')
    # all files in this directory
    modules = (
        module_name + '.' + name
        for name, ext in (
            os.path.splitext(filename)
            for filename in os.listdir(module_name.replace('.', '/'))
        )
        if ext == '.py' and not name.startswith('__')
    )

    # declare a new function, shortcut to the importlib one
    imported = partial(importlib.import_module, package=PACKAGE_NAME)

    # return all classes in the modules
    return {
        n:cls
        for module in modules
        for n, cls in imported(module).__dict__.items()
        # cls is a class, defined in the tia.mixins package
        if type(cls) is type and module_name in cls.__module__
    }




