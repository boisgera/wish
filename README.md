
Wishlist
================================================================================

Intro/Motivation


Info / Installation
--------------------------------------------------------------------------------

Getting Started
--------------------------------------------------------------------------------

Simplest example: replace

  
    def f(a, b, c, d):
        # ...
        return e, f, g, h

with

    import wishlist

    def f(a, b, c, d, returns="e, f, g, h"):
        wishes = wishlist.make(returns)
        ...
        return wishes.grant()


Benefits (client-side): ...


**TODO.**

  - basic use case, explain the very simple syntax (natural tuple syntax).
    Function call usage:

  - suggest `returns` or `output`, `output_args`, etc.

  - default unwrap for one argument, how to force wrap. Explain that trailing
    comma works (simplifies programatic generation of wishlist from a true 
    list). State explictely that repeating an argument is ok.

  - examine the variables that are required for early checks or 
    reduced computations.

  - automatic selection of the variables from `locals()` or
    manual selection.


Real use-case: scientific computing where functions that return a lot of
arguments are common.

Concrete Use Case
--------------------------------------------------------------------------------

The [SciPy](http://www.scipy.org/) library provides an implementation of 
the [singular value decomposition][svd] of matrices. The code is available
in the file `decomp_svd.py`, available 
[online](https://github.com/scipy/scipy/blob/master/scipy/linalg/decomp_svd.py),
and reproduced in the [`examples` directory][examples] of `wishlist`.

[svd]: http://en.wikipedia.org/wiki/Singular_value_decomposition
[examples]: https://github.com/boisgera/wishlist/tree/master/examples



Example of a redesign of `scipy.linalg.svd` (actually, merge several
related functions). Start with 



    def svd(A, returns="U, S, V"):

        wishes = wishlist.make(returns)
        ...

        return wishes.grant()


Actually, do the stuff in an `examples` or `samples` dir and just display
the documentation / docstring here ?

