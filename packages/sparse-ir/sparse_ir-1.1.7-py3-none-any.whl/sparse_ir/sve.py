# Copyright (C) 2020-2022 Markus Wallerberger, Hiroshi Shinaoka, and others
# SPDX-License-Identifier: MIT
from warnings import warn
import numpy as np

from . import _gauss
from . import poly
from . import svd
from . import kernel

HAVE_XPREC = svd._ddouble is not None


def compute(K, eps=None, cutoff=None, n_sv=None, n_gauss=None, dtype=float,
            work_dtype=None, sve_strat=None, svd_strat=None):
    """Perform truncated singular value expansion of a kernel.

    Perform a truncated singular value expansion (SVE) of an integral
    kernel ``K : [xmin, xmax] x [ymin, ymax] -> R``::

        K(x, y) == sum(s[l] * u[l](x) * v[l](y) for l in (0, 1, 2, ...)),

    where ``s[l]`` are the singular values, which are ordered in non-increasing
    fashion, ``u[l](x)`` are the left singular functions, which form an
    orthonormal system on ``[xmin, xmax]``, and ``v[l](y)`` are the right
    singular functions, which form an orthonormal system on ``[ymin, ymax]``.

    The SVE is mapped onto the singular value decomposition (SVD) of a matrix
    by expanding the kernel in piecewise Legendre polynomials (by default by
    using a collocation).

    Arguments:
        K (kernel.AbstractKernel):
            Integral kernel to take SVE from
        eps (float):
            Accuracy target for the basis: attempt to have singular values down
            to a relative magnitude of ``eps``, and have each singular value
            and singular vector be accurate to ``eps``.  A ``work_dtype`` with
            a machine epsilon of ``eps**2`` or lower is required to satisfy
            this. Defaults to ``2.2e-16`` if xprec is available, and ``1e-8``
            otherwise.
        cutoff (float):
            Relative cutoff for the singular values.  A ``work_dtype`` with
            machine epsilon of ``cutoff`` is required to satisfy this.
            Defaults to a small multiple of the machine epsilon.

            Note that ``cutoff`` and ``eps`` serve distinct purposes. ``cutoff``
            reprsents the accuracy to which the kernel is reproduced, whereas
            ``eps`` is the accuracy to which the singular values and vectors
            are guaranteed.
        n_sv (int):
            Maximum basis size. If given, only at most the ``n_sv`` most
            significant singular values and associated singular functions are
            returned.
        n_gauss (int):
            Order of Legendre polynomials. Defaults to kernel hinted value.
        dtype (np.dtype):
            Data type of the result.
        work_dtype (np.dtype):
            Working data type. Defaults to a data type with machine epsilon of
            at most ``eps**2`` and at most  ``cutoff``, or otherwise most
            accurate data type available.
        sve_strat (AbstractSVE):
            SVE to SVD translation strategy. Defaults to ``SamplingSVE``,
            optionally wrapped inside of a ``CentrosymmSVE`` if the kernel
            is centrosymmetric.
        svd_strat ('fast' or 'default' or 'accurate'):
            SVD solver. Defaults to fast (ID/RRQR) based solution
            when accuracy goals are moderate, and more accurate Jacobi-based
            algorithm otherwise.

    Returns:
        An ``SVEResult`` containing the truncated singular value expansion.
    """
    safe_eps, work_dtype, svd_strat = _safe_eps(eps, work_dtype, svd_strat)
    if sve_strat is None:
        sve_strat = CentrosymmSVE if K.is_centrosymmetric else SamplingSVE
    if cutoff is None:
        cutoff = 2 * svd.finfo(work_dtype).eps
    sve = sve_strat(K, safe_eps, n_gauss=n_gauss, dtype=work_dtype)
    u, s, v = zip(*(svd.compute(matrix, sve.nsvals_hint, svd_strat)
                    for matrix in sve.matrices))
    u, s, v = _truncate(u, s, v, cutoff, n_sv)
    return sve.postprocess(u, s, v, dtype)


class AbstractSVE:
    """Truncated singular value expansion (SVE) of an integral kernel.

    Given an integral kernel `K`, this provides methods for computing its
    truncated singular value expansion (SVE), given by::

        K(x, y) == sum(s[l] * u[l](x) * v[l](y) for l in range(L)),

    where `L` is the truncation, `u[l](x)` is the `l`-th left singular
    function, `s[l]` is the `l`-th singular value, and `v[l](y)` is the `l`-th
    right singular function.  The left and right singular functions form
    orthonormal systems on their respective spaces.

    Computing the SVE involves introducing two sets of basis functions on the
    `x` and `y` axis and then translating the SVE into one or more matrices,
    the computing the singular value decomposition of those matrices, and
    finally postprocessing the data.
    """
    @property
    def matrices(self):
        """SVD problems underlying the SVE."""
        raise NotImplementedError()

    def postprocess(self, u, s, v, dtype=None):
        """Constructs the SVE result from the SVD"""
        raise NotImplementedError()


class SVEResult:
    """Result of singular value expansion"""
    def __init__(self, u, s, v, K, eps=None):
        self.u = u
        self.s = s
        self.v = v

        # In addition to its SVE, we remember the type of kernel and also the
        # accuracy to which the SVE was computed.
        self.K = K
        self.eps = eps

    def part(self, eps=None, max_size=None):
        if eps is None:
            eps = self.eps
        cut = (self.s >= eps * self.s[0]).sum()
        if max_size is not None and max_size < cut:
            cut = max_size
        if cut == self.s.size:
            return self.u, self.s, self.v
        else:
            return self.u[:cut], self.s[:cut], self.v[:cut]

    def __iter__(self):
        return iter((self.u, self.s, self.v))


class SamplingSVE(AbstractSVE):
    """SVE to SVD translation by sampling technique [1].

    Maps the singular value expansion (SVE) of a kernel ``K`` onto the singular
    value decomposition of a matrix ``A``.  This is achieved by chosing two
    sets of Gauss quadrature rules: ``(x, wx)`` and ``(y, wy)`` and
    approximating the integrals in the SVE equations by finite sums.  This
    implies that the singular values of the SVE are well-approximated by the
    singular values of the following matrix::

        A[i, j] = sqrt(wx[i]) * K(x[i], y[j]) * sqrt(wy[j])

    and the values of the singular functions at the Gauss sampling points can
    be reconstructed from the singular vectors ``u`` and ``v`` as follows::

        u[l,i] ≈ sqrt(wx[i]) u[l](x[i])
        v[l,j] ≈ sqrt(wy[j]) u[l](y[j])

    [1] P. Hansen, Discrete Inverse Problems, Ch. 3.1
    """
    def __init__(self, K, eps, *, n_gauss=None, dtype=float):
        self.K = K
        sve_hints = K.sve_hints(eps)
        if n_gauss is None:
            n_gauss = sve_hints.ngauss

        self.eps = eps
        self.n_gauss = n_gauss
        self.nsvals_hint = sve_hints.nsvals
        self._rule = _gauss.legendre(n_gauss, dtype)
        self._segs_x = sve_hints.segments_x.astype(dtype)
        self._segs_y = sve_hints.segments_y.astype(dtype)
        self._gauss_x = self._rule.piecewise(self._segs_x)
        self._gauss_y = self._rule.piecewise(self._segs_y)
        self._sqrtw_x = np.sqrt(self._gauss_x.w)
        self._sqrtw_y = np.sqrt(self._gauss_y.w)

    @property
    def matrices(self):
        result = kernel.matrix_from_gauss(self.K, self._gauss_x, self._gauss_y)
        result *= self._sqrtw_x[:, None]
        result *= self._sqrtw_y[None, :]
        return result,

    def postprocess(self, u, s, v, dtype=None):
        u, = u
        s, = s
        v, = v
        if dtype is None:
            dtype = np.result_type(u, s, v)

        s = s.astype(dtype)
        u_x = u / self._sqrtw_x[:,None]
        v_y = v / self._sqrtw_y[:,None]

        u_x = u_x.reshape(self._segs_x.size - 1, self.n_gauss, s.size)
        v_y = v_y.reshape(self._segs_y.size - 1, self.n_gauss, s.size)

        cmat = _gauss.legendre_collocation(self._rule)
        # lx,ixs -> ils -> lis
        u_data = (cmat @ u_x).transpose(1, 0, 2)
        v_data = (cmat @ v_y).transpose(1, 0, 2)

        dsegs_x = self._segs_x[1:] - self._segs_x[:-1]
        dsegs_y = self._segs_y[1:] - self._segs_y[:-1]
        u_data *= np.sqrt(.5 * dsegs_x)[None,:,None]
        v_data *= np.sqrt(.5 * dsegs_y)[None,:,None]

        # Construct polynomial
        ulx = poly.PiecewiseLegendrePoly(
                        u_data.astype(dtype), self._segs_x.astype(dtype))
        vly = poly.PiecewiseLegendrePoly(
                        v_data.astype(dtype), self._segs_y.astype(dtype))
        _canonicalize(ulx, vly)
        return SVEResult(ulx, s, vly, self.K, self.eps)


class CentrosymmSVE(AbstractSVE):
    """SVE of centrosymmetric kernel in block-diagonal (even/odd) basis.

    For a centrosymmetric kernel ``K``, i.e., a kernel satisfying:
    ``K(x, y) == K(-x, -y)``, one can make the following ansatz for the
    singular functions::

        u[l](x) = ured[l](x) + sign[l] * ured[l](-x)
        v[l](y) = vred[l](y) + sign[l] * ured[l](-y)

    where ``sign[l]`` is either +1 or -1.  This means that the singular value
    expansion can be block-diagonalized into an even and an odd part by
    (anti-)symmetrizing the kernel::

        Keven = K(x, y) + K(x, -y)
        Kodd  = K(x, y) - K(x, -y)

    The l-th basis function, restricted to the positive interval, is then
    the singular function of one of these kernels.  If the kernel generates a
    Chebyshev system [1], then even and odd basis functions alternate.

    [1]: A. Karlin, Total Positivity (1968).
    """
    def __init__(self, K, eps, *, InnerSVE=None, **inner_args):
        if InnerSVE is None:
            InnerSVE = SamplingSVE
        self.K = K
        self.eps = eps

        # Inner kernels for even and odd functions
        self.even = InnerSVE(K.get_symmetrized(+1), eps, **inner_args)
        self.odd = InnerSVE(K.get_symmetrized(-1), eps, **inner_args)

        # Now extract the hints
        self.nsvals_hint = max(self.even.nsvals_hint, self.odd.nsvals_hint)

    @property
    def matrices(self):
        m, = self.even.matrices
        yield m
        m, = self.odd.matrices
        yield m

    def postprocess(self, u, s, v, dtype):
        u_even, s_even, v_even = self.even.postprocess(u[:1], s[:1], v[:1], dtype)
        u_odd, s_odd, v_odd = self.odd.postprocess(u[1:], s[1:], v[1:], dtype)

        # Merge two sets - data is [legendre, segment, l]
        u_data = np.concatenate([u_even.data, u_odd.data], axis=2)
        v_data = np.concatenate([v_even.data, v_odd.data], axis=2)
        s = np.concatenate([s_even, s_odd])
        signs = np.concatenate([np.ones(s_even.size), -np.ones(s_odd.size)])

        # Sort: now for totally positive kernels like defined in this module,
        # this strictly speaking is not necessary as we know that the even/odd
        # functions intersperse.
        sort = s.argsort()[::-1]
        u_data = u_data[:, :, sort]
        v_data = v_data[:, :, sort]
        s = s[sort]
        signs = signs[sort]

        # Extend to the negative side
        inv_sqrt2 = 1/np.sqrt(np.array(2, dtype=u_data.dtype))
        u_data *= inv_sqrt2
        v_data *= inv_sqrt2
        poly_flip_x = ((-1)**np.arange(u_data.shape[0]))[:, None, None]
        u_neg = u_data[:, ::-1, :] * poly_flip_x * signs
        v_neg = v_data[:, ::-1, :] * poly_flip_x * signs
        u_data = np.concatenate([u_neg, u_data], axis=1)
        v_data = np.concatenate([v_neg, v_data], axis=1)

        # TODO: this relies on specific symmetrization behaviour ...
        full_hints = self.K.sve_hints(self.eps)
        u = poly.PiecewiseLegendrePoly(u_data, full_hints.segments_x, symm=signs)
        v = poly.PiecewiseLegendrePoly(v_data, full_hints.segments_y, symm=signs)
        return SVEResult(u, s, v, self.K, self.eps)


def _safe_eps(eps_required, work_dtype, svd_strat):
    # First, choose the working dtype based on the eps required
    if work_dtype is None:
        if eps_required is None or eps_required < 1e-8:
            work_dtype = svd.MAX_DTYPE
        else:
            work_dtype = np.float64
    else:
        work_dtype = np.dtype(work_dtype)

    # Next, work out the actual epsilon
    if work_dtype == np.float64:
        # This is technically a bit too low (the true value is about 1.5e-8),
        # but it's not too far off and easier to remember for the user.
        safe_eps = 1e-8
    else:
        safe_eps = np.sqrt(svd.finfo(work_dtype).eps)

    # Work out the SVD strategy to be used.  If the user sets this, we
    # assume they know what they are doing and do not warn if they compute
    # the basis.
    warn_acc = False
    if svd_strat is None:
        if eps_required is not None and eps_required < safe_eps:
            svd_strat = 'accurate'
            warn_acc = True
        else:
            svd_strat = 'fast'

    if warn_acc:
        msg = (f"\n"
            f"Requested accuracy is {eps_required:.2g}, which is below the\n"
            f"accuracy {safe_eps:.2g} for the work data type {work_dtype}.\n"
            f"Expect singular values and basis functions for large l to\n"
            f"have lower precision than the cutoff.\n")
        if not HAVE_XPREC:
            msg += "Install the xprec package to gain more precision.\n"
        warn(msg, UserWarning, 3)

    return safe_eps, work_dtype, svd_strat


def _canonicalize(ulx, vly):
    """Canonicalize basis.

    Each SVD (u_l, v_l) pair is unique only up to a global phase, which may
    differ from implementation to implementation and also platform.  We
    fix that gauge by demanding u_l(1) > 0.  This ensures a diffeomorphic
    connection to the Legendre polynomials for lambda_ -> 0.
    """
    gauge = np.sign(ulx(1))
    ulx.data[None, None, :] *= 1/gauge
    vly.data[None, None, :] *= gauge


def _truncate(u, s, v, rtol=0, lmax=None):
    """Truncate singular value expansion.

    Arguments:

     - ``u``, ``s``, ``v``: Thin singular value expansion
     - ``rtol`` : If given, only singular values satisfying
       ``s[l]/s[0] > rtol`` are retained.
     - ``lmax`` : If given, at most the ``lmax`` most significant singular
       values are retained.
    """
    if lmax is not None and (lmax < 0 or int(lmax) != lmax):
        raise ValueError("invalid value of maximum number of singular values")
    if not (0 <= rtol <= 1):
        raise ValueError("invalid relative tolerance")

    sall = np.hstack(s)

    # Determine singular value cutoff.  Note that by selecting a cutoff even
    # in the case of lmax, we make sure to never remove parts of a degenerate
    # singular value space, rather, we reduce the size of the basis.
    ssort = np.sort(sall)
    cutoff = rtol * ssort[-1]
    if lmax is not None and lmax < sall.size:
        cutoff = max(cutoff, ssort[sall.size - lmax - 1])

    # Determine how many singular values survive in each group
    scount = [(si > cutoff).sum() for si in s]

    u_cut = [ui[:, :counti] for (ui, counti) in zip(u, scount)]
    s_cut = [si[:counti] for (si, counti) in zip(s, scount)]
    v_cut = [vi[:, :counti] for (vi, counti) in zip(v, scount)]
    return u_cut, s_cut, v_cut
