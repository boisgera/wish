#!/usr/bin/env python
# coding: utf-8

"""
Wishlist Test Suite
===================

    >>> import wish

    >>> a, b, c = 1, 2, 3
    >>> wish.grant("a, b, c")
    (1, 2, 3)
    >>> wish.grant("a, b")
    (1, 2)
    >>> wish.grant("c, b, a")
    (3, 2, 1)
    >>> wish.grant("b, a")
    (2, 1)
    >>> wish.grant("a, c")
    (1, 3)


    >>> wish.grant("a")
    1
    >>> wish.grant("b")
    2
    >>> wish.grant("c")
    3
    
    >>> wish.grant("a,")
    (1,)
    >>> wish.grant("a, b,")
    (1, 2)
    >>> wish.grant("a, b, c,")
    (1, 2, 3)


    >>> wish.make("a") == ["a"]
    True
    >>> wish.make("a, b") == ["a", "b"]
    True
    >>> wish.make("a, b, c") == ["a", "b", "c"]
    True

    >>> wish.make("a,") == ["a"]
    True
    >>> wish.make("a, b,") == ["a", "b"]
    True
    >>> wish.make("a, b, c,") == ["a", "b", "c"]
    True

"""

# Python 2.7 Standard Library
import doctest
import sys

__main__ = (__name__ == "__main__")
__name__ = "test"

if __main__:
    sys.modules[__name__] = sys.modules["__main__"]

import test

suite = doctest.DocTestSuite(test)

if __main__:
    doctest.testmod(test)

