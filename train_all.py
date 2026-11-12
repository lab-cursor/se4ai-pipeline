# train_all.py -- the home-value model, as it grew out of a notebook.
# Run from the repository root:  python train_all.py
#
# Everything happens in one file, top to bottom: load, clean, encode,
# train, evaluate, save. It works... for the data we had last year.

import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error

# ---- 1. collect ---------------------------------------------------------
df = pd.read_csv("data/sales_2025.csv")
print("loaded", len(df), "sales")

# ---- 2. clean -----------------------------------------------------------
df["sold_date"] = pd.to_datetime(df["sold_date"], format="%Y-%m-%d")
df = df[df["price"] > 10_000]           # drop obvious data-entry errors (price typos)

# ---- 3. features --------------------------------------------------------
df["age"] = df["sold_date"].dt.year - df["year_built"]
X = pd.get_dummies(df[["sqft", "bedrooms", "age", "region"]], columns=["region"], dtype=int)
y = df["price"]

# experiment from March: log-transformed price. Didn't help? Not sure. Keep for now.
USE_LOG_PRICE = False
if USE_LOG_PRICE:
    import numpy as np
    y = np.log(y)

# ---- 4. train -----------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = DecisionTreeRegressor(max_depth=8, random_state=0)
model.fit(X_train, y_train)

# ---- 5. evaluate --------------------------------------------------------
mae = mean_absolute_error(y_test, model.predict(X_test))
print(f"MAE: ${mae:,.0f}")

# ---- 6. save ------------------------------------------------------------
Path("out").mkdir(exist_ok=True)
joblib.dump(model, "out/model.joblib")
print("saved out/model.joblib")
