# coding: utf-8
"""
TODO: documentation.
"""

# Third-Party Libaries
import pkg_resources 

def _open(filename):
    "Open a data file with the Resource Management API"
    requirement = pkg_resources.Requirement.parse(__name__)
    return open(pkg_resources.resource_filename(requirement, filename))

# Metadata
__name__        = "wishlist",
__version__     = None,
__license__     = "MIT License",
__author__      = u"Sébastien Boisgérault <Sebastien.Boisgerault@gmail.com>",
__url__         = "https://warehouse.python.org/project/wishlist",
__summary__     = "Specify the variables that a function returns."
__readme__      = _open("README.md").read(), 
__classifiers__ = ["Programming Language :: Python :: 2.7" ,
                   "Operating System :: OS Independent"    ,
                   "Topic :: Software Development"         ,
                   "Intended Audience :: Developers"       ,
                   "License :: OSI Approved :: MIT License",
                   "Development Status :: 3 - Alpha"       ]

# ------------------------------------------------------------------------------ 

# Python 2.7 Standard Library
import inspect

# Third-Party Libraries
pass

# Q: rename the module "wish" ? To avoid multiplication of the names ?
# The API is now wish / grant (as verbs). Or keep wishlist to emphasize
# the sequence API of the object ? Here "wish" does not mean *A* wish,
# the noun, but *TO* wish something.

# TODO: don't mix metaphors and keep simple things simple: in the basic
# use case, there is no need for an explicit "wishlist" concept: you just
# define
#
#     import wish
#
#     def  f(a, b, returns="a, b"):
#         ...
#         return wish.grant(returns)
#
# So, it makes sense to have a "wish" module. Wishlist may be useful, but
# this is arguably and advanced concept.

# Goal: management of multiple return values as tuples, which is classic in
# Python, but with a set of returned values that is configurable (by a 
# function arguments). So this is a kind of "configurable set of returned
# values). We are "packaging" the returned values.
#
# With this scheme, you avoid clumsy "unpacking" syntax stuff, you
# even may avoid the COMPUTATIONS of those values if you don't need it,
#
# We aim at: 1) being convenient for simple/default case (single return
# values for example) 2) support multiple return values "classically"
# (as tuples) 3) allows configurability 4) allow for lazyness (fat return
# values are avoided).
#
# Management of Named (multiple) Return Values, whose set is determined 
# by the input argument (to avoid computations of the values we dont need)
# Optionally, go for (custom) named tuples ?

# Return Values Specification: TODO
#
# Syntax: "NAME" (unwraped), "NAME,", (tuple wraped) "NAME_1, NAME2",
# "NAME_1, NAME_2,". Accept "*" as a wildcard ? List of returned values
# should obviously be accepted to (they are never unpacked)

# Question: return None or () ? Mmmm. () for consistency.

def wish(list_):
    return WishList(list_)

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

    def grant(self, env=None):
        if env is None:
            # use the caller's local environment.
            frame = inspect.currentframe()
            env = frame.f_back.f_locals
        output = tuple([env[name] for name in self])
        if self._unpack:
            output = output[0]
        return output

