#!/usr/bin/env python
# coding: utf-8

"""
Wishlist Test Suite
================================================================================

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


Numerical Differentiation Example
--------------------------------------------------------------------------------

    >>> def d(f, x, h=1e-7, returns="dq"):
    ...     dq = (f(x + h) - f(x)) / h
    ...     dq2 = (f(x + 0.5*h) - f(x)) / (0.5*h)
    ...     error = 2 * (dq - dq2)
    ...     return wish.grant(returns)
    >>> from math import sin
    >>> d(sin, x=0.0)
    0.9999999999999983
    >>> d(sin, x=0.0, returns="dq, error")
    (0.9999999999999983, -2.4424906541753444e-15)
    >>> d(sin, x=0.0, returns="error")
    -2.4424906541753444e-15


SVD Example
--------------------------------------------------------------------------------

  >>> from numpy import dot, diagonal, shape

  >>> A = [[ 0.0, -2.0,  0.0],
  ...      [ 1.0,  0.0,  0.0]]

  >>> from scipy.linalg import svd, diagsvd
  >>> sp = {}
  >>> sp["U"], sp["s"], sp["Vh"] = svd(A)
  >>> sp["S"] = diagsvd(sp["s"], shape(sp["U"])[1], shape(sp["Vh"])[0])

  >>> from wish.examples import svd
  >>> U, S, V = svd(A)
  >>> (U == sp["U"]).all()
  True
  >>> (diagonal(S) == sp["s"]).all()
  True
  >>> (V.conjugate().transpose() == sp["Vh"]).all()
  True
  >>> U, s, Vh = svd(A, returns="U, s, Vh")
  >>> (U == sp["U"]).all()
  True
  >>> (s == sp["s"]).all()
  True
  >>> (Vh == sp["Vh"]).all()
  True
  >>> s = svd(A, returns="s")
  >>> (s == sp["s"]).all()
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

