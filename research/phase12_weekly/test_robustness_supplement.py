from __future__ import annotations

import math
import numpy as np

from robustness_supplement import cscv_splits, dsr_style_probability, holm_adjust


def test_cscv_path_count():
    paths = list(cscv_splits(63))
    assert len(paths) == 20
    assert all(len(train) > 0 and len(test) > 0 for train, test, _ in paths)


def test_holm_monotonicity():
    out = holm_adjust([("a", 0.001), ("b", 0.02), ("c", 0.4)])
    assert out["a"] <= out["b"] <= out["c"]


def test_dsr_finite():
    x = np.array([1, 2, -1, 3, 2, -2, 1, 4, -1, 2], dtype=float)
    out = dsr_style_probability(x, 30)
    assert 0.0 <= out["probability"] <= 1.0
    assert math.isfinite(out["weekly_sharpe_threshold"])


if __name__ == "__main__":
    test_cscv_path_count()
    test_holm_monotonicity()
    test_dsr_finite()
    print("robustness supplemental tests passed")