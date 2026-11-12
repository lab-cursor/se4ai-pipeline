"""Stage 1: collect -- load raw sales from one or more CSV files."""
from pathlib import Path

import pandas as pd


def load_sales(paths: list[Path]) -> pd.DataFrame:
    """Read every CSV in `paths` and return one DataFrame with all rows.

    Input:  list of CSV paths, each with columns
            sqft, bedrooms, year_built, region, sold_date, price
    Output: a single DataFrame (raw, uncleaned)
    """
    # TODO (Task 1): move the "1. collect" block from train_all.py here.
    # Hint: pd.concat([pd.read_csv(p) for p in paths], ignore_index=True)
    raise NotImplementedError("collect.load_sales: move the code from train_all.py")
