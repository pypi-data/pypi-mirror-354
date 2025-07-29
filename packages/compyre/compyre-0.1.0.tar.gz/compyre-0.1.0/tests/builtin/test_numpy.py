import contextlib

import numpy as np
import pytest
import torch

from compyre import alias, api, builtin


class TestNumpyNdarray:
    @pytest.mark.parametrize(
        ("actual", "expected"),
        [
            (object(), np.array([])),
            (np.array([]), object()),
            (np.array([]), torch.tensor([])),
        ],
    )
    def test_not_supported(self, actual, expected):
        assert (
            builtin.equal_fns.numpy_ndarray(
                api.Pair(index=(), actual=actual, expected=expected)
            )
            is None
        )

    def test_equal(self):
        value = np.array([1.0], dtype=np.float64)

        result = builtin.equal_fns.numpy_ndarray(
            api.Pair(index=(), actual=value.copy(), expected=value.copy())
        )
        assert result is True

    def test_rtol_equal(self):
        rtol = 1e-2
        expected = np.array([1.0], dtype=np.float64)
        actual = expected * (1 + rtol / 2)

        result = builtin.equal_fns.numpy_ndarray(
            api.Pair(index=(), actual=actual, expected=expected),
            rtol=rtol,
            atol=0,
        )
        assert result is True

    def test_rtol_not_equal(self):
        rtol = 1e-2
        expected = np.array([1.0], dtype=np.float64)
        actual = expected * (1 + rtol * 2)

        result = builtin.equal_fns.numpy_ndarray(
            api.Pair(index=(), actual=actual, expected=expected),
            rtol=rtol,
            atol=0,
        )
        assert isinstance(result, AssertionError)

    def test_rtol_alias(self):
        rtol = 1e-2
        expected = np.array([1.0], dtype=np.float64)
        actual = expected * (1 + rtol / 2)

        api.assert_equal(
            actual,
            expected,
            unpack_fns=[],
            equal_fns=[builtin.equal_fns.numpy_ndarray],
            aliases={alias.RELATIVE_TOLERANCE: rtol},
            atol=0,
        )

    def test_atol_equal(self):
        atol = 1e-2
        expected = np.array([1.0], dtype=np.float64)
        actual = expected + atol / 2

        result = builtin.equal_fns.numpy_ndarray(
            api.Pair(index=(), actual=actual, expected=expected),
            atol=atol,
            rtol=0,
        )
        assert result is True

    def test_atol_not_equal(self):
        atol = 1e-2
        expected = np.array([1.0], dtype=np.float64)
        actual = expected + atol * 2

        result = builtin.equal_fns.numpy_ndarray(
            api.Pair(index=(), actual=actual, expected=expected),
            atol=atol,
            rtol=0,
        )
        assert isinstance(result, AssertionError)

    def test_atol_alias(self):
        atol = 1e-2
        expected = np.array([1.0], dtype=np.float64)
        actual = expected + atol / 2

        api.assert_equal(
            actual,
            expected,
            unpack_fns=[],
            equal_fns=[builtin.equal_fns.numpy_ndarray],
            aliases={alias.ABSOLUTE_TOLERANCE: atol},
            rtol=0,
        )

    @pytest.mark.parametrize("equal_nan", [True, False])
    def test_equal_nan(self, equal_nan):
        expected = np.array([float("NaN")])
        actual = expected.copy()

        result = builtin.equal_fns.numpy_ndarray(
            api.Pair(index=(), actual=actual, expected=expected), equal_nan=equal_nan
        )

        if equal_nan:
            assert result is True
        else:
            assert isinstance(result, AssertionError)

    @pytest.mark.parametrize("equal_nan", [True, False])
    def test_equal_nan_alias(self, equal_nan):
        expected = np.array([float("NaN")])
        actual = expected.copy()

        with contextlib.nullcontext() if equal_nan else pytest.raises(AssertionError):
            api.assert_equal(
                actual,
                expected,
                unpack_fns=[],
                equal_fns=[builtin.equal_fns.numpy_ndarray],
                aliases={alias.NAN_EQUALITY: equal_nan},
            )

    def test_verbose(self):
        def msg(*, verbose):
            expected = np.array([1.0])
            actual = expected + 1
            result = builtin.equal_fns.numpy_ndarray(
                api.Pair(index=(), actual=actual, expected=expected),
                rtol=0,
                atol=0,
                verbose=verbose,
            )
            assert isinstance(result, AssertionError)
            return str(result)

        assert len(msg(verbose=True)) > len(msg(verbose=False))
