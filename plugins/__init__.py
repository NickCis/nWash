from os import listdir

plugins = __all__ = [x[:-3] for x in listdir(__path__[0]) if x.endswith('.py') and x.find('__') == -1]

from . import *

def plugin(name, *args, **kargs):
    if not name in __all__:
        return None

    return eval(name)
def getDefinition(name):
    if not name in __all__:
        return None
    plug = plugin(name)
    if not "__definition__" in dir(plug):
        return None
    return plug.__definition__

del listdir
