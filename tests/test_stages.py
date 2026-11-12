"""Tests for the collect and train stages. Run with:  python3 -m pytest tests/test_stages.py

They check that each stage uses its inputs (parameters) instead of values
copied from train_all.py, such as a fixed file name or a fixed tree depth.
"""
import pandas as pd

from pipeline.collect import load_sales
from pipeline.train import train_model

COLUMNS = "sqft,bedrooms,year_built,region,sold_date,price\n"


def test_load_sales_reads_every_file_it_is_given(tmp_path):
    first = tmp_path / "first.csv"
    second = tmp_path / "second.csv"
    first.write_text(COLUMNS + "1500,3,1990,Suburbs,2025-05-01,420000\n"
                               "900,2,1975,Riverside,2025-06-12,250000\n")
    second.write_text(COLUMNS + "1800,3,2001,Hills,2026-02-23,510000\n")

    df = load_sales([first, second])

    assert len(df) == 3, (
        f"expected 3 rows from the two files, got {len(df)}: "
        "does load_sales read the files in `paths`, or a fixed file name?"
    )


def sample_data(n=60):
    X = pd.DataFrame({"sqft": range(600, 600 + 40 * n, 40), "bedrooms": [1 + i % 5 for i in range(n)]})
    y = X["sqft"] * 180 + X["bedrooms"] * 9_000
    return X, y


def test_train_model_uses_max_depth():
    X, y = sample_data()
    for depth in (1, 3):
        model = train_model(X, y, max_depth=depth)
        assert model.get_depth() <= depth, (
            f"asked for max_depth={depth}, got a tree of depth {model.get_depth()}: "
            "does train_model use its `max_depth` parameter?"
        )


def test_train_model_trains_on_all_rows_it_is_given():
    X, y = sample_data()
    model = train_model(X, y, max_depth=3)
    assert model.tree_.n_node_samples[0] == len(X), (
        f"trained on {model.tree_.n_node_samples[0]} of {len(X)} rows: "
        "the train/test split already happens in run_pipeline.py, so don't split again"
    )
