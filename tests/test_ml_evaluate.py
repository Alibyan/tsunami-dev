from src.ml_evaluate import _precision_at_k, _feature_and_label


def test_precision_at_k_basic():
    y_true = [1, 0, 1, 0]
    y_prob = [0.9, 0.8, 0.2, 0.1]
    assert _precision_at_k(y_true, y_prob, 2) == 0.5


def test_feature_and_label_shapes():
    rows = [
        {"mag": 7.0, "depth": 10.0, "time": 1_700_000_000_000, "updated": 1_700_000_010_000, "tsunami": 1},
        {"mag": 4.0, "depth": 300.0, "time": 1_600_000_000_000, "updated": 1_600_000_010_000, "tsunami": 0},
    ]
    X, y = _feature_and_label(rows)
    assert len(X) == 2 and len(y) == 2
    assert len(X[0]) == 3
    assert y == [1, 0]
