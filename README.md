
Wish
================================================================================

**TL;DR.** You have a function that returns three arguments (or more) ?
We may be able to help.

-----

Wish allows you to that you define and call functions that may
return a large number of return values in a Pythonic way.

There are several features, built into the Python language, to deal with
functions that may accept a large number of arguments: [default argument values, 
argument lists and keyword arguments][arguments]. And this panel of options
just works beautifully: the scheme is flexible, the syntax is terse and readable.

[arguments]: https://docs.python.org/2/tutorial/controlflow.html#more-on-defining-functions

And what do we have to deal with a large number of return values ? Tuples !
This is actually the canonical way to return multiple values, but it is not
really convienent. We may help you with that ... Read on !


Getting Started
--------------------------------------------------------------------------------

First, install wish

    $ pip install wish

*NOT AVAILABLE YET*

Simplest example: replace

  
    def f(a, b):
        c, d, e = a - b, a + b, a * b
        return c, d, e

with

    import wish

    def f(a, b, returns="c, d, e"):
        c, d, e = a - b, a + b, a * b
        return wishes.grant(returns)


Usage:

    >>> c, d, e = f(a, b) 

    >>> c = f(a, b, c, returns="c")
    >>> d = f(a, b, c, returns="d")
    >>> e = f(a, b, c, returns="e")

    >>> c, d = f(a, b, c, returns="c, d")
    >>> e, c, d = f(a, b, c, returns="e, c, d")    

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
the [singular value decomposition][svd] of matrices that provides of good
example of the kind of improvement that wishlist allows. 

The original code is in a file `decomp_svd.py`, [available online][decomp_svd.py], 
and reproduced in the [`examples` directory][examples] of `wishlist`. In the
same directory, the file [svd.py] is a redesign of the interface powered by
wishlist.

[svd]: http://en.wikipedia.org/wiki/Singular_value_decomposition
[decomp_svd.py]: https://github.com/scipy/scipy/blob/master/scipy/linalg/decomp_svd.py
[examples]: https://github.com/boisgera/wishlist/tree/master/examples
[svd.py]: https://github.com/boisgera/wishlist/tree/master/examples/svd.py

The original module exports three functions to deal with the different set of
returned values we may be interested in. Additionally, the main one has an 
optional parameter that provides a limited control on the returned values:
either three values are returned, or a single one.

The redesign provide instead a single function, whose prototype is:

    def svd(a, 
            full_matrices=True, compute_uv=True, overwrite_a=False, check_finite=True,
            returns="U, S, Vh"):


-----

The new interface can be used like that:

    >>> import numpy as np
    >>> a = np.random.randn(9, 6) + 1.j*np.random.randn(9, 6)
    >>> U, S, Vh, s = svd(a, returns="U, S, Vh, s")
    >>> U.shape, S.shape, Vh.shape, s.shape
    ((9, 9), (9, 6), (6, 6), (6,))

    >>> U, S, Vh = svd(a, full_matrices=False)
    >>> U.shape, S.shape, Vh.shape
    ((9, 6), (6, 6), (6, 6))
    >>> np.allclose(a, np.dot(U, np.dot(S, Vh)))
    True

    >>> s2 = svd(a, returns="s")
    >>> np.allclose(s, s2)
    True




Example of a redesign of `scipy.linalg.svd` (actually, merge several
related functions). Start with 

Benefits:


  - reduced redundancy

  - simpler interface: one function instead of three.




Here is the full documentation of the redesigned `svd` function, 
in the [NumpPy/Scipy style][numpy-doc].

[numpy-doc]: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt

-----

### Singular Value Decomposition.

Factorizes the matrix a into two unitary matrices `U` and `Vh`, and
a diagonal matrix `S` of suitable shape with non-negative real 
numbers on the diagonal.
    

#### Parameters

  - `a`: `(M, N)` array_like

    Matrix to decompose.

  - `full_matrices`: `bool`, optional
    
    If `True`, `U` and `Vh` are of shape `(M,M)`, `(N,N)`.
    If `False`, the shapes are `(M,K)` and `(K,N)`, where `K = min(M,N)`.

  - `overwrite_a`: `bool`, optional
      
     Whether to overwrite `a`; may improve performance.
     Default is `False`.

  - `check_finite`: `boolean`, optional
    
    Whether to check that the input matrix contains only finite numbers.
    Disabling may give a performance gain, but may result in problems
    (crashes, non-termination) if the inputs do contain infinities or NaNs.

  - `returns`: `string`, optional 
     
    Select the returned values, among `U`, `S`, `Vh`, `s`.
    Default is `"U, S, Vh"`.

#### Returns

The selection of return values is configurable by the `returns` parameter.

  - `U`: `ndarray`

    Unitary matrix having left singular vectors as columns.
    Of shape `(M,M)` or ``M,K)`, depending on `full_matrices`.

  - `S` : `ndarray`

    A matrix with the singular values of `a`, sorted in non-increasing
    order, in the main diagonal and zeros elsewhere.
    Of shape `(M,N)` or `(K,K)`, depending on `full_matrices`.

  - `Vh`: `ndarray`
     
    Unitary matrix having right singular vectors as rows.
    Of shape `(N,N)` or `(K,N)` depending on `full_matrices`.
    
  - `s`: `ndarray`, not returned by default
            
    The singular values, sorted in non-increasing order.
    Of shape `(K,)`, with `K = min(M, N)`.

#### Raises

  - `LinAlgError`

    If SVD computation does not converge.

