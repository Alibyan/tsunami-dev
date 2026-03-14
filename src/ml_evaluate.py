"""Phase 6: train/evaluate a lightweight classifier for triage interest.

Target label strategy:
- y = USGS `tsunami` property from event records (0 or 1)

This keeps evaluation independent from our internal score formula.
"""

import argparse
import json
import os
import sqlite3
from dataclasses import dataclass
from typing import Any


@dataclass
class EvalResult:
    rows_total: int
    train_rows: int
    test_rows: int
    target_label: str
    split_mode_used: str | None
    pr_auc: float | None
    precision_at_k: dict[str, float]
    positive_rate_test: float | None
    note: str | None = None


def _result_to_dict(result: EvalResult) -> dict[str, Any]:
    return {
        "rows_total": result.rows_total,
        "train_rows": result.train_rows,
        "test_rows": result.test_rows,
        "target_label": result.target_label,
        "split_mode_used": result.split_mode_used,
        "pr_auc": result.pr_auc,
        "precision_at_k": result.precision_at_k,
        "positive_rate_test": result.positive_rate_test,
        "note": result.note,
    }


def write_metrics_artifact(result: EvalResult, output_path: str) -> str:
    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(_result_to_dict(result), fh, indent=2)
    return output_path


def _precision_at_k(y_true: list[int], y_prob: list[float], k: int) -> float:
    if not y_true or k <= 0:
        return 0.0
    pairs = sorted(zip(y_true, y_prob), key=lambda x: x[1], reverse=True)
    top = pairs[: min(k, len(pairs))]
    positives = sum(1 for y, _ in top if y == 1)
    return positives / float(len(top)) if top else 0.0


def load_rows(db_path: str) -> list[dict[str, Any]]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, time, updated, mag, depth, tsunami
        FROM events
        WHERE mag IS NOT NULL
        ORDER BY COALESCE(time, updated, 0) ASC
        """
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def _feature_and_label(
    rows: list[dict[str, Any]],
) -> tuple[list[list[float]], list[int]]:
    X, y = [], []
    for r in rows:
        # Use last-known timestamp as age proxy feature.
        ref_ms = max(r.get("time") or 0, r.get("updated") or 0)
        if ref_ms <= 0:
            age_hours = 9999.0
        else:
            import time

            now_ms = time.time() * 1000.0
            age_hours = max(0.0, (now_ms - float(ref_ms)) / 3600000.0)

        label = 1 if int(r.get("tsunami") or 0) == 1 else 0

        depth = r.get("depth") if r.get("depth") is not None else 100.0
        X.append(
            [
                float(r.get("mag") or 0.0),
                float(depth),
                float(age_hours),
            ]
        )
        y.append(label)
    return X, y


def evaluate_model(
    db_path: str = "data/events.sqlite",
    train_ratio: float = 0.8,
) -> EvalResult:
    rows = load_rows(db_path)
    if len(rows) < 20:
        return EvalResult(
            rows_total=len(rows),
            train_rows=0,
            test_rows=0,
            target_label="tsunami",
            split_mode_used=None,
            pr_auc=None,
            precision_at_k={},
            positive_rate_test=None,
            note="Not enough rows for meaningful ML evaluation (need >= 20).",
        )

    X, y = _feature_and_label(rows)

    split_idx = int(len(X) * train_ratio)
    split_idx = max(1, min(split_idx, len(X) - 1))

    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    split_mode_used = "time"

    # Default to time split, then fallback if class diversity is insufficient.
    if len(set(y_train)) < 2 or len(set(y_test)) < 2:
        try:
            from sklearn.model_selection import train_test_split

            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=(1.0 - train_ratio),
                random_state=42,
                stratify=y,
            )
            split_mode_used = "stratified_fallback"
        except Exception:
            return EvalResult(
                rows_total=len(rows),
                train_rows=len(y_train),
                test_rows=len(y_test),
                target_label="tsunami",
                split_mode_used="time",
                pr_auc=None,
                precision_at_k={},
                positive_rate_test=(sum(y_test) / len(y_test)) if y_test else None,
                note=(
                    "Insufficient class diversity for LogisticRegression in time "
                    "split, and stratified fallback could not be created."
                ),
            )

    if len(set(y_train)) < 2 or len(set(y_test)) < 2:
        return EvalResult(
            rows_total=len(rows),
            train_rows=len(y_train),
            test_rows=len(y_test),
            target_label="tsunami",
            split_mode_used=split_mode_used,
            pr_auc=None,
            precision_at_k={},
            positive_rate_test=(sum(y_test) / len(y_test)) if y_test else None,
            note="Insufficient class diversity after split selection.",
        )

    # Deferred import keeps non-ML test paths lightweight.
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import average_precision_score
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler

    clf = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("lr", LogisticRegression(max_iter=1000, class_weight="balanced")),
        ]
    )
    clf.fit(X_train, y_train)
    y_prob = clf.predict_proba(X_test)[:, 1].tolist()

    pr_auc = float(average_precision_score(y_test, y_prob))
    p_at_5 = _precision_at_k(y_test, y_prob, 5)
    p_at_10 = _precision_at_k(y_test, y_prob, 10)
    p_at_20 = _precision_at_k(y_test, y_prob, 20)

    return EvalResult(
        rows_total=len(rows),
        train_rows=len(y_train),
        test_rows=len(y_test),
        target_label="tsunami",
        split_mode_used=split_mode_used,
        pr_auc=round(pr_auc, 4),
        precision_at_k={
            "k5": round(p_at_5, 4),
            "k10": round(p_at_10, 4),
            "k20": round(p_at_20, 4),
        },
        positive_rate_test=round(sum(y_test) / len(y_test), 4),
        note=None,
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Train/evaluate classifier using USGS tsunami flag target"
    )
    parser.add_argument("--db-path", default="data/events.sqlite", help="SQLite path")
    parser.add_argument(
        "--train-ratio",
        type=float,
        default=0.8,
        help="Time-based train split ratio",
    )
    parser.add_argument(
        "--output-json",
        default="artifacts/metrics_latest.json",
        help="Path to write evaluation JSON artifact",
    )
    return parser


if __name__ == "__main__":
    args = _build_parser().parse_args()
    result = evaluate_model(
        db_path=args.db_path,
        train_ratio=args.train_ratio,
    )
    output_path = write_metrics_artifact(result, args.output_json)
    print(json.dumps(_result_to_dict(result), indent=2))
    print(f"Wrote metrics artifact to {output_path}")
