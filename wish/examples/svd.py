"""SVD decomposition functions."""
from __future__ import division, print_function, absolute_import

import wish

import numpy
from numpy import asarray_chkfinite, asarray, zeros, r_, diag
from scipy.linalg import calc_lwork

# Scipy.linalg imports.
from scipy.linalg.misc import LinAlgError, _datacopied
from scipy.linalg.lapack import get_lapack_funcs

__all__ = ['svd', 'orth']


def svd(a, full_matrices=True, compute_uv=True, overwrite_a=False,
        check_finite=True, returns="U, S, V"):
    """
    Singular Value Decomposition.

    Factorizes the matrix a into two unitary matrices U and Vh, and
    a diagonal matrix S of suitable shape with non-negative real 
    numbers on the diagonal.
.

    Parameters
    ----------
    a : (M, N) array_like
        Matrix to decompose.
    full_matrices : bool, optional
        If True, `U` and `Vh` are of shape ``(M,M)``, ``(N,N)``.
        If False, the shapes are ``(M,K)`` and ``(K,N)``, where
        ``K = min(M,N)``.
    overwrite_a : bool, optional
        Whether to overwrite `a`; may improve performance.
        Default is False.
    check_finite : boolean, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.
    returns: string, optional
        Select the returned values, among ``U``, ``S``, ``s``, ``V`` and ``Vh``,.
        Default is ``"U, S, Vh"``.
        
    Returns
    -------

    The selection of return values is configurable by the ``returns`` parameter.

    U : ndarray
        Unitary matrix having left singular vectors as columns.
        Of shape ``(M,M)`` or ``(M,K)``, depending on `full_matrices`.
    S : ndarray
        A matrix with the singular values of ``a``, sorted in non-increasing
        order, in the main diagonal and zeros elsewhere.
        Of shape ``(M,N)`` or ``(K,K)``, depending on `full_matrices`.
    V : ndarray
        Unitary matrix having right singular vectors as columns.
        Of shape ``(N,N)`` or ``(N, K)`` depending on `full_matrices`.
    s : ndarray, not returned by default
        The singular values, sorted in non-increasing order.
        Of shape (K,), with ``K = min(M, N)``.
    Vh : ndarray
        Unitary matrix having right singular vectors as rows.
        Of shape ``(N,N)`` or ``(N, K)`` depending on `full_matrices`.

    Raises
    ------
    LinAlgError
        If SVD computation does not converge.


    Examples
    --------
    >>> import numpy as np
    >>> from wish.examples import svd
    >>> a = np.random.randn(9, 6) + 1.j*np.random.randn(9, 6)
    >>> U, S, V = svd(a)
    >>> U.shape, S.shape, V.shape
    ((9, 9), (9, 6), (6, 6))

    >>> U, S, Vh = svd(a, full_matrices=False, returns="U, S, Vh")
    >>> U.shape, S.shape, Vh.shape
    ((9, 9), (9, 6), (6, 6))
    >>> np.allclose(a, np.dot(U, np.dot(S, Vh)))
    True

    >>> s = svd(a, returns="s")
    >>> np.allclose(s, np.diagonal(S))
    True

    """
    wishlist = wish.make(returns)
    for name in wishlist: 
        if name not in ["U", "S", "V", "s", "Vh"]:
            error = "unexpected return value {name!r}"
            raise TypeError(error.format(name=name))

    if check_finite:
        a1 = asarray_chkfinite(a)
    else:
        a1 = asarray(a)
    if len(a1.shape) != 2:
        raise ValueError('expected matrix')
    m,n = a1.shape
    overwrite_a = overwrite_a or (_datacopied(a1, a))
    gesdd, = get_lapack_funcs(('gesdd',), (a1,))

    lwork = calc_lwork.gesdd(gesdd.typecode, m, n, compute_uv)[1]

    compute_uv = "U" in wishlist or "V" in wishlist or "Vh" in wishlist

    U,s,Vh,info = gesdd(a1,compute_uv=compute_uv, lwork=lwork,
                       full_matrices=full_matrices, overwrite_a=overwrite_a)

    if info > 0:
        raise LinAlgError("SVD did not converge")
    if info < 0:
        raise ValueError('illegal value in %d-th argument of internal gesdd'
                                                                    % -info)

    if "V" in wishlist:
        V = Vh.transpose().conjugate() 
    if "S" in wishlist:
        S = _diagsvd(s, U.shape[1], Vh.shape[0]) 
        # fuck, maybe not computed. Use shape of A. 
        # Interaction with full_matrices?

    return wishlist.grant()

# This function is private
def _diagsvd(s, M, N):
    """
    Construct the sigma matrix in SVD from singular values and size M, N.

    Parameters
    ----------
    s : (M,) or (N,) array_like
        Singular values
    M : int
        Size of the matrix whose singular values are `s`.
    N : int
        Size of the matrix whose singular values are `s`.

    Returns
    -------
    S : (M, N) ndarray
        The S-matrix in the singular value decomposition

    """
    part = diag(s)
    typ = part.dtype.char
    MorN = len(s)
    if MorN == M:
        return r_['-1', part, zeros((M, N-M), typ)]
    elif MorN == N:
        return r_[part, zeros((M-N,N), typ)]
    else:
        raise ValueError("Length of s must be M or N.")


# Orthonormal decomposition

def orth(A):
    """
    Construct an orthonormal basis for the range of A using SVD

    Parameters
    ----------
    A : (M, N) ndarray
        Input array

    Returns
    -------
    Q : (M, K) ndarray
        Orthonormal basis for the range of A.
        K = effective rank of A, as determined by automatic cutoff

    See also
    --------
    svd : Singular value decomposition of a matrix

    """
    U, s = svd(A, returns="U, s")
    M, N = A.shape
    eps = numpy.finfo(float).eps
    tol = max(M,N) * numpy.amax(s) * eps
    num = numpy.sum(s > tol, dtype=int)
    Q = U[:,:num]
    return Q
