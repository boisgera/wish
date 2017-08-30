# coding: utf-8

# Python 2.7 Standard Library
import inspect

# Third-Party Libraries
pass

#
# Metadata
# ------------------------------------------------------------------------------
#
__name__        = "wish"
__version__     = "1.1.0-alpha.1"
__license__     = "MIT License"
__author__      = u"Sébastien Boisgérault <Sebastien.Boisgerault@gmail.com>"
__url__         = "http://boisgera.github.io/wish/"
__summary__     = "Selectable Return Values for Python"
__readme__      = "README.md"
__classifiers__ = ["Programming Language :: Python :: 2.7" ,
                   "Operating System :: OS Independent"    ,
                   "Topic :: Software Development"         ,
                   "Intended Audience :: Developers"       ,
                   "License :: OSI Approved :: MIT License",
                   "Development Status :: 3 - Alpha"       ]

# ------------------------------------------------------------------------------ 
def make(list_):
    return WishList(list_)

def grant(list_, env=None):
    return make(list_).grant(env, _back=2)
    
class WishList(list):
    def __init__(self, list_):
        self._unpack = False # by default, we return a tuple.
        list.__init__(self, [name.strip() for name in list_.split(",")])
        if len(self) == 1:
            # there is a single request and there is no trailing comma, 
            # so we won't pack the return value into a tuple.
            self._unpack = True
        if len(self) >= 1 and not self[-1]: 
            # Take care of the empty item generated by a trailing comma.
            self[:] = self[:-1]

    def grant(self, env=None, _back=1):
        if env is None:
            # use the caller's local environment if _back=1 (the default), 
            # the caller's caller's if _back=2, and so on.
            frame = inspect.currentframe()
            for i in range(_back):
                frame = frame.f_back
            env = frame.f_locals
        values = []
        for name in self:
            if name not in env:
                error = "{0!r} is not a valid return value"
                raise NameError(error.format(name))
            values.append(env[name])
        output = tuple(values)
        if self._unpack:
            output = output[0]
        return output
