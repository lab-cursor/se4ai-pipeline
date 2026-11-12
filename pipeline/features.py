"""Stage 3: features -- turn cleaned sales into the model's inputs.

Training and prediction must both call this one function, so the model
always sees features encoded the same way (no training-serving skew).
"""
import pandas as pd


def encode(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Return (X, y): feature matrix and target price.

    X columns: sqft, bedrooms, age, and one 0/1 column per region.
    """
    # TODO (Task 1): move the "3. features" block from train_all.py here.
    # Leave the dead USE_LOG_PRICE experiment behind -- nobody uses it.
    df["age"] = df["sold_date"].dt.year - df["year_built"]
    X = pd.get_dummies(df[["sqft", "bedrooms", "age", "region"]], columns=["region"], dtype=int)
    y = df["price"]

    # experiment from March: log-transformed price. Didn't help? Not sure. Keep for now.
    USE_LOG_PRICE = False
    if USE_LOG_PRICE:
        import numpy as np
        y = np.log(y)

    return X, y