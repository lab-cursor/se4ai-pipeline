"""Run the whole pipeline end to end:  python run_pipeline.py

collect -> clean -> features -> train -> evaluate (gate) -> save to out/
GitHub Actions runs exactly this command on every push.
"""
import json
from pathlib import Path

import joblib
from sklearn.model_selection import train_test_split

from pipeline.clean import clean_sales
from pipeline.collect import load_sales
from pipeline.evaluate import evaluate
from pipeline.features import encode
from pipeline.train import train_model

# ---- configuration: the only place you need to edit --------------------
DATA_FILES = [
    Path("data/sales_2025.csv"),
    # Task 2: add Path("data/sales_2026_q1.csv") here
]
MAX_DEPTH = 8          # Task 3: try 1 to see the evaluation gate fail
MAX_MAE = 50_000       # evaluation gate: maximum acceptable error in dollars
OUT = Path("out")


def main():
    raw = load_sales(DATA_FILES)
    print("collected", len(raw), "sales")
    sales = clean_sales(raw)
    print("cleaned  ", len(sales), "sales")
    X, y = encode(sales)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = train_model(X_train, y_train, max_depth=MAX_DEPTH)
    metrics = evaluate(model, X_test, y_test, max_mae=MAX_MAE)

    OUT.mkdir(exist_ok=True)
    joblib.dump(model, OUT / "model.joblib")
    (OUT / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print("saved", OUT / "model.joblib", "and", OUT / "metrics.json")


if __name__ == "__main__":
    main()
