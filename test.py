#!/usr/bin/env python
# coding: utf-8

# Python 2.7 Standard Library
import doctest
import unittest
import sys

__main__ = __name__ == "__main__" 
__name__ = "test"
if __main__:
    sys.modules[__name__] = sys.modules["__main__"]

def test():
    """
    >>> from wishlist import wish, grant

    >>> wish("a") == ["a"]
    True
    >>> wish("a, b") == ["a", "b"]
    True
    >>> wish("a, b, c") == ["a", "b", "c"]
    True

    >>> wish("a,") == ["a"]
    True
    >>> wish("a, b,") == ["a", "b"]
    True
    >>> wish("a, b, c,") == ["a", "b", "c"]
    True

    >>> a, b, c = 1, 2, 3
    >>> wish("a, b, c").grant()
    (1, 2, 3)
    >>> wish("a, b").grant()
    (1, 2)
    >>> wish("a")
    1
    >>> wish("b")
    2
    >>> wish("c")
    3
    """

test_suite = doctest.DocTestSuite()

if __main__:
    doctest.testmod()


