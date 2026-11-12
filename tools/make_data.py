"""Generate the synthetic home-sales data used in this exercise.

Instructor reference only: you do not need to run this. The CSV files in
data/ were produced with this script and a fixed seed, so re-running it
gives identical files.

    python tools/make_data.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
REGIONS = {"Downtown": 1.35, "Riverside": 1.15, "Suburbs": 1.0, "Hills": 1.25, "Outskirts": 0.8}


def make_sales(n, start, end, rng):
    sqft = rng.integers(600, 3500, n)
    bedrooms = np.clip((sqft // 600) + rng.integers(-1, 2, n), 1, 6)
    year_built = rng.integers(1950, 2024, n)
    region = rng.choice(list(REGIONS), n)
    days = (pd.Timestamp(end) - pd.Timestamp(start)).days
    sold = pd.Timestamp(start) + pd.to_timedelta(rng.integers(0, days, n), unit="D")
    age = sold.year - year_built
    factor = np.array([REGIONS[r] for r in region])
    price = (60_000 + 180 * sqft + 9_000 * bedrooms - 900 * age) * factor
    price = price * rng.normal(1.0, 0.06, n)
    return pd.DataFrame({
        "sqft": sqft,
        "bedrooms": bedrooms,
        "year_built": year_built,
        "region": region,
        "sold_date": sold,
        "price": price.round(-2).astype(int),
    })


def main():
    rng = np.random.default_rng(41645)
    DATA.mkdir(exist_ok=True)

    old = make_sales(500, "2025-01-01", "2025-12-31", rng)
    old["sold_date"] = old["sold_date"].dt.strftime("%Y-%m-%d")
    old.to_csv(DATA / "sales_2025.csv", index=False)

    # The new batch comes from a different export: timestamps with a timezone,
    # and some listings without square footage.
    new = make_sales(150, "2026-01-01", "2026-03-31", rng)
    new["sold_date"] = new["sold_date"].dt.strftime("%Y-%m-%dT10:30:00+07:00")
    new["sqft"] = new["sqft"].astype("Int64")
    new.loc[rng.choice(len(new), 12, replace=False), "sqft"] = pd.NA
    new.to_csv(DATA / "sales_2026_q1.csv", index=False)


if __name__ == "__main__":
    main()
