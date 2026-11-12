"""Tests for the clean stage. Run with:  pytest

They describe what the next stage relies on, for old AND new data formats.
"""
import pandas as pd

from pipeline.clean import clean_sales


def raw(rows):
    cols = ["sqft", "bedrooms", "year_built", "region", "sold_date", "price"]
    return pd.DataFrame(rows, columns=cols)


def test_2025_format_still_works():
    df = clean_sales(raw([[1500, 3, 1990, "Suburbs", "2025-05-01", 420_000]]))
    assert len(df) == 1
    assert pd.api.types.is_datetime64_any_dtype(df["sold_date"])
    assert df["sold_date"].iloc[0].year == 2025


def test_new_batch_dates_with_timezone():
    df = clean_sales(raw([
        [1500, 3, 1990, "Suburbs", "2025-05-01", 420_000],
        [1800, 3, 2001, "Hills", "2026-02-23T10:30:00+07:00", 510_000],
    ]))
    assert len(df) == 2
    assert pd.api.types.is_datetime64_any_dtype(df["sold_date"])
    assert df["sold_date"].dt.year.tolist() == [2025, 2026]


def test_no_missing_sqft_after_cleaning():
    df = clean_sales(raw([
        [1500, 3, 1990, "Suburbs", "2025-05-01", 420_000],
        [None, 2, 1975, "Riverside", "2026-01-10T10:30:00+07:00", 300_000],
    ]))
    assert df["sqft"].notna().all()


def test_drops_obvious_errors():
    df = clean_sales(raw([
        [1500, 3, 1990, "Suburbs", "2025-05-01", 420_000],
        [1500, 3, 1990, "Suburbs", "2025-05-02", 5],  # price typo
    ]))
    assert len(df) == 1
