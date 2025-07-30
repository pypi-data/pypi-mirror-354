# Copyright (C) 2020-2022 Markus Wallerberger, Hiroshi Shinaoka, and others
# SPDX-License-Identifier: MIT
import numpy as np
import sparse_ir

import pytest


def _check_smooth(u, s, uscale, fudge_factor):
    eps = np.finfo(s.dtype).eps
    x = u.knots[1:-1]

    jump = np.abs(u(x + eps) - u(x - eps))
    compare = np.abs(u(x + 3 * eps) - u(x + eps))
    compare = np.maximum(compare, uscale * eps)

    # loss of precision
    compare *= fudge_factor * (s[0] / s)[:, None]
    try:
        np.testing.assert_array_less(jump, compare)
    except:
        print((jump > compare).nonzero())
        raise


@pytest.mark.parametrize("lambda_", [10, 42, 10_000])
def test_smooth(sve_logistic, lambda_):
    beta = 1
    basis = sparse_ir.FiniteTempBasis('F', beta, lambda_/beta,
                                      sve_result=sve_logistic[lambda_])
    _check_smooth(basis.u, basis.s, 2*basis.u(1).max(), 24)
    _check_smooth(basis.v, basis.s, 50, 20)


@pytest.mark.parametrize("lambda_", [10, 42, 10_000])
def test_num_roots_u(sve_logistic, lambda_):
    beta = 1
    basis = sparse_ir.FiniteTempBasis('F', beta, lambda_/beta,
                                      sve_result=sve_logistic[lambda_])
    for i in range(basis.u.size):
        ui_roots = basis.u[i].roots()
        assert ui_roots.size == i


@pytest.mark.parametrize("stat", ['F', 'B'])
@pytest.mark.parametrize("lambda_", [10, 42, 10_000])
def test_num_roots_uhat(sve_logistic, stat, lambda_):
    beta = 1
    basis = sparse_ir.FiniteTempBasis(stat, beta, lambda_/beta,
                                      sve_result=sve_logistic[lambda_])
    for i in [0, 1, 7, 10]:
        x0 = basis.uhat[i].extrema()
        assert i + 1 <= x0.size <= i + 2


@pytest.mark.parametrize("stat", ['F', 'B'])
@pytest.mark.parametrize("lambda_", [10, 42, 10_000])
def test_accuracy(sve_logistic, stat, lambda_):
    beta = 4
    basis = sparse_ir.FiniteTempBasis(stat, beta, lambda_/beta,
                                      sve_result=sve_logistic[lambda_])

    assert 0 < basis.accuracy <= basis.significance[-1]
    assert basis.significance[0] == 1
    assert basis.accuracy <= basis.s[-1] / basis.s[0]
