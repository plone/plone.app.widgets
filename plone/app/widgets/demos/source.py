"""

    Helpers to show source code examples.

"""

import sys


def get_class_source(klass):
    """ Grab the source code of the module declaring a Python class.
    """

    mod = klass.__module__
    path = sys.modules[mod].__file__

    path = path.replace(".pyc", ".py")

    f = open(path, "rt")
    text = f.read()
    f.close()
    return text
