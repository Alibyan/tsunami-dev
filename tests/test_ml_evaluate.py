import sqlite3
import json
import os

from src.cache import create_db, insert_raw_event
from src.ml_evaluate import (
    _precision_at_k,
    _feature_and_label,
    evaluate_model,
    write_metrics_artifact,
)


def test_precision_at_k_basic():
    y_true = [1, 0, 1, 0]
    y_prob = [0.9, 0.8, 0.2, 0.1]
    assert _precision_at_k(y_true, y_prob, 2) == 0.5


def test_feature_and_label_shapes():
    rows = [
        {
            "mag": 7.0,
            "depth": 10.0,
            "time": 1_700_000_000_000,
            "updated": 1_700_000_010_000,
            "tsunami": 1,
        },
        {
            "mag": 4.0,
            "depth": 300.0,
            "time": 1_600_000_000_000,
            "updated": 1_600_000_010_000,
            "tsunami": 0,
        },
    ]
    X, y = _feature_and_label(rows)
    assert len(X) == 2 and len(y) == 2
    assert len(X[0]) == 3
    assert y == [1, 0]


def test_evaluate_model_uses_stratified_fallback(tmp_path):
    db_path = str(tmp_path / "events.sqlite")
    create_db(db_path)
    conn = sqlite3.connect(db_path)

    # Create clustered labels in time order so time split fails class diversity:
    # first 20 rows tsunami=0, last 6 rows tsunami=1.
    base_time = 1_700_000_000_000
    for i in range(20):
        insert_raw_event(
            conn,
            evt_id=f"neg-{i}",
            raw_json="{}",
            time=base_time + i,
            updated=base_time + i,
            mag=5.0,
            depth=100.0,
            lat=0.0,
            lon=0.0,
            place="test",
            urls=None,
            tsunami=0,
        )

    for i in range(6):
        insert_raw_event(
            conn,
            evt_id=f"pos-{i}",
            raw_json="{}",
            time=base_time + 10_000 + i,
            updated=base_time + 10_000 + i,
            mag=7.0,
            depth=10.0,
            lat=0.0,
            lon=0.0,
            place="test",
            urls=None,
            tsunami=1,
        )

    conn.close()

    result = evaluate_model(db_path=db_path, train_ratio=0.8)
    assert result.split_mode_used == "stratified_fallback"
    assert result.pr_auc is not None


def test_write_metrics_artifact(tmp_path):
    db_path = str(tmp_path / "events.sqlite")
    create_db(db_path)
    conn = sqlite3.connect(db_path)
    base_time = 1_700_000_000_000

    for i in range(20):
        insert_raw_event(
            conn,
            evt_id=f"neg-art-{i}",
            raw_json="{}",
            time=base_time + i,
            updated=base_time + i,
            mag=5.0,
            depth=80.0,
            lat=0.0,
            lon=0.0,
            place="artifact-test",
            urls=None,
            tsunami=0,
        )
    for i in range(8):
        insert_raw_event(
            conn,
            evt_id=f"pos-art-{i}",
            raw_json="{}",
            time=base_time + 50_000 + i,
            updated=base_time + 50_000 + i,
            mag=7.0,
            depth=12.0,
            lat=0.0,
            lon=0.0,
            place="artifact-test",
            urls=None,
            tsunami=1,
        )
    conn.close()

    result = evaluate_model(db_path=db_path, train_ratio=0.8)
    output_path = str(tmp_path / "metrics.json")
    path = write_metrics_artifact(result, output_path)
    assert path == output_path
    assert os.path.exists(path)

    with open(path, "r", encoding="utf-8") as fh:
        payload = json.load(fh)
    assert payload["target_label"] == "tsunami"
    assert "precision_at_k" in payload
