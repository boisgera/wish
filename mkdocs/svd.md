
We redesign the API of the SVD function of SciPy
with wish to demonstrate the method and its benefits.

Context
--------------------------------------------------------------------------------

The [SciPy](http://www.scipy.org/) library 
implements [singular value decomposition](https://en.wikipedia.org/wiki/Singular_value_decomposition)
(SVD),
a matrix factorization that is instrumental
in numerical analysis, machine learning and data science.

The SVD of a matrix `A` provides three matrices `U`, `Sigma`
and `V`.
The matrix `S` has the same shape as `A` and is diagonal 
(`S[i,j] == 0` unless `i == j`). The matrices `U` and `V` are unitary. 
Refer for example to [SVD on Wikipedia](https://en.wikipedia.org/wiki/Singular_value_decomposition)
for more information.

In any case, to compute `A` from `U`, `S` and `V`, do:

    >>> from numpy import dot
    >>> Vh = V.conjugate().transpose()
    >>> A = dot(U, dot(S, Vh))

<!--
The SVD of a matrix $A \in \mathbb{C}^{m \times n}$ 
is a triple $(U, \Sigma, V)$ such that
  $$
  A = U \Sigma V^{\ast}
  $$
where $U \in \mathbb{C}^{m \times m}$ and $V \in \mathbb{C}^{n \times n}$
are *unitary matrices*, $V^{\ast}$ denotes the *conjugate transpose* of $V$ 
and $\Sigma \in \mathbb{C}^{m \times n}$ is a *diagonal matrix* 
(filled with zeros outside of its main diagonal)
whose diagonal coefficients $\sigma_k$
-- called the *singular values* of $A$ --
are real and satisfy

  $$
  \sigma_1 \geq \sigma_2 \geq \dots \geq \sigma_k \geq \dots \geq 0
  $$
-->

Basic API
--------------------------------------------------------------------------------

The `svd` function of SciPy works like this: you provide the matrix `A`
and it computes a matrix `U`, a vector `s` and a matrix `Vh`[^1]:

    >>> from scipy.linalg import svd
    >>> U, s, Vh = svd(A)

The default convention deviates a little from the definition of the SVD:
the vector `s` is the diagonal of `S` instead of `S` itself
and `Vh` corresponds to the conjugate transpose of `V` instead of `V`.

[^1]: For example, if

          >>> A = [[ 0.0, -2.0,  0.0],
          ...      [ 1.0,  0.0,  0.0]]

      then 

          >>> U
          array([[1.,  0.],
                [ 0.,  1.]])
          >>> s 
          array([ 2.,  1.])
          >>> Vh 
          array([[ 0., -1.,  0.],
                 [ 1.,  0.,  0.],
                 [ 0.,  0.,  1.]])

While there are good reasons for these conventions, 
I'd rather follow the [principle of least astonishment][POLA].
Thus, by default our SVD
implementation returns the triple `(U, S, V)`:

[POLA]: https://en.wikipedia.org/wiki/Principle_of_least_astonishment

    >>> from wish.examples import svd
    >>> U, S, V = svd(A)

The implementation is simple:

    def svd(A):

        U, S, V = ...

        return U, S, V

Enabling selectable return values for this function is easy:

    import wish

    def svd(A, returns="U, S, V"):

        U, S, V = ... 

        return wish.grant(returns)

But of course in this simple pattern .. **MENTION ERROR CHECKING
and NAMESPACE VALUE SELECTION**

    def svd(A, returns="U, S, V"):
        wishlist = wish.make(returns)
        for name in wishlist:
            if name not in ["U", "S", "V"]:
                 error = "{0!r} is not a valid return value"
                 raise NameError(error.format(name))

        U, S, V = ... 

        return wish.grant(wishlist)


Now, it should still be possible to get the output of SciPy, 
it's rather simple since we may select the return values:

    >>> U, s, Vh = svd(A, returns="U, s, Vh")

Implementation:

    import numpy
    import wish

    def svd(A, returns="U, S, V"):
        wishlist = wish.make(returns)
        for name in wishlist:
            if name not in ["U", "S", "V", "s", "Vh"]:
                 error = "{0!r} is not a valid return value"
                 raise NameError(error.format(name))

        U, S, V = ... 

        if "s" in wishlist:
            s = numpy.diagonal(S)
        if "Vh" in wishlist:
            Vh = V.conjugate().transpose()

        return wish.grant(wishlist)




Singular Values
--------------------------------------------------------------------------------

We frequently need to compute only the singular values of a matrix.
The scipy `svd` achieves this with an additional option `compute_uv` 
that can be set to `False` as describe in the documentation:

!!! Note "compute_uv: bool, optional." 
    Whether to compute also `U` and `Vh` in addition to `s`.
    Default is True.

It is used like this:

    >>> from scipy.linalg import svd
    >>> s = svd(M, compute_uv=False)

This interface is not totally satisfactory: 
while we easily understand that we won't 
compute -- and therefore won't return -- `U` and `Vh`, 
it is not totally obvious what is returned. 
And if in the first place you were only interested 
in the `s` array, you may not know what `U` and `Vh` are ...
There is nothing here that cannot be solved by reading 
the documentation of `svd`, but still this is not optimal.
The SciPy folks are apparently aware of this because they have implemented 
a helper function, `svdvals`, to avoid calling `svd` in this case:

!!! Note "svdvals(a, overwrite_a=False, check_finite=True)"
    Compute singular values of a matrix.

With `svdvals`, we can simply do

    >>> from scipy.linalg import svdvals
    >>> s = svdvals(A)

but of course now, you have another function to remember of.
And while it is a one-liner, its full documentation essentially 
duplicates the one of `svd`.

With the wish version, the equivalent code is simply

    >>> from wish.examples import svd
    >>> s = svd(A, returns="s")

We know what is returned and a no new function is necessary.

Implementation:

    import numpy
    import wish

    def svd(A, returns="U, S, V"):
        wishlist = wish.make(returns)
        for name in wishlist:
            if name not in ["U", "S", "V", "s", "Vh"]:
                 error = "{0!r} is not a valid return value"
                 raise NameError(error.format(name))

        if "U" in wishlist or "V" in wishlist or "Vh" in wishlist:
            U, S, V = ... 
        else:
            S = ...

        if "s" in wishlist:
            s = numpy.diagonal(S)
        if "Vh" in wishlist:
            Vh = V.conjugate().transpose()

        return wish.grant(wishlist)


Reconstruction
--------------------------------------------------------------------------------

Since SciPy `svd` returns the diagonal of $\Sigma$, 
it comes with the helper function `diagsvd` to build
$\Sigma$ from the singular values:

!!! Note "diagsvd(s, M, N)"
    Construct the sigma matrix in SVD from singular values and size `M`, `N`.

It is used like this:

    >>> U, s, Vh = svd(A)
    >>> S = diagsvd(s, shape(U)[1], shape(Vh)[0])

The matrix `S` is typically used to reconstruct `A`:

    >>> from numpy import dot
    >>> A = dot(U, dot(S, Vh))

Of course with the wish-enabled version, the same effect is obtained with

    >>> from wish.examples import svd
    >>> U, S, Vh = wsvd(A, returns="U, S, Vh")
    >>> A = dot(U, dot(S, Vh))

-----

Now, if you don't want to reconstruct the matrix `A` but a version of it
based on a different set of singular values -- for example to achieve
some [dimensionality reduction](https://en.wikipedia.org/wiki/Principal_component_analysis#Dimensionality_reduction) 
-- this is easy because NumPy already provides 
the appropriate functions. First, get the singular values with

    >>> U, S, Vh, s = w_svd(A, returns="U, S, Vh, s")

then replace the vector of singular values `s`
with a modified vector `s2` and inject the result in `S`

    >>> s2 = ...
    >>> from numpy import fill_diagonal
    >>> fill_diagonal(S, s)
    >>> A2 = dot(U, dot(S, Vh))


The New API
--------------------------------------------------------------------------------

The redesigned `svd` function now has arguably a simpler and more consistent
interface:

   - The simplest and most common usage follows closely the domain conventions,

   - The "configurable return values" pattern is supported
     with the extra parameter `returns`

   - The ad hoc parameter `compute_uv` is not needed anymore.

   - Two helper functions `svdvals` and `diagsvd` are not needed anymore

<!--
The general description of `scipy.linalg.svd` 
is still perfectly applicable:

!!! Note "Singular Value Decomposition."
    
    Factorizes the matrix a into two unitary matrices `U` and `Vh`, 
    and a 1-dim array `s` of singular values (real, non-negative) such that
    `a == U*S*Vh`, where `S` is a suitably shaped matrix of zeros with
    main diagonal `s`.

-->

The description of parameters and returned values is only slightly different[^2]:

!!! Note "Parameters"

      - `a`: `(M, N)` array_like

        Matrix to decompose.

      - ... 

      - `returns`: `string`, optional 
         
        Select the returned values, among `U`, `S`, `s`, `V` and `Vh`.
        Default is `"U, S, V"`.

[^2]: we have omitted any reference to the the parameters 
      `full_matrices`, `overwrite_a`, `check_finite` and `lapack_driver` 
      since the behavior of `svd` has not changed in this respect.
      Refer to the [Scipy documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.svd.html) for details.
 

!!! Note "Returns"

    The selection of return values is configurable with the `returns` parameter.

      - `U`: `ndarray`

        Unitary matrix having left singular vectors as columns.

      - `S` : `ndarray`

        A matrix with the singular values of `a`, sorted in non-increasing
        order, in the main diagonal and zeros elsewhere.

      - `V`: `ndarray`
         
        Unitary matrix having right singular vectors as columns.

      - `s`: `ndarray`, not returned by default
                
        The singular values, sorted in non-increasing order.

      - `Vh`: `ndarray`, not returned by default
         
        Conjugate transpose of `V`
        



<!--    

#### Parameters

  - `a`: `(M, N)` array_like

    Matrix to decompose.

  - ...

  - `returns`: `string`, optional 
     
    Select the returned values, among `U`, `S`, `Vh`, `s`.
    Default is `"U, S, Vh"`.

-->

<!--
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

-->
