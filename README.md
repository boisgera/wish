
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
the [singular value decomposition][svd] of matrices. The code is in a file
`decomp_svd.py`, [available online](https://github.com/scipy/scipy/blob/master/scipy/linalg/decomp_svd.py), and reproduced in the [`examples` directory][examples] of `wishlist`.

[svd]: http://en.wikipedia.org/wiki/Singular_value_decomposition
[examples]: https://github.com/boisgera/wishlist/tree/master/examples

    def svd(a, full_matrices=True, compute_uv=True, overwrite_a=False,
            check_finite=True, returns="U, S, Vh"):


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

