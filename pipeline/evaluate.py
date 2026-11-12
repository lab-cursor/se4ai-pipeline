"""Stage 5: evaluate -- measure the model and stop the pipeline if it is too weak.

This stage is already written for you. It adds something train_all.py never
had: an evaluation *gate*. A model that is worse than `max_mae` never gets
saved, so a bad model cannot quietly reach production.
"""
import pandas as pd
from sklearn.metrics import mean_absolute_error


def evaluate(model, X_test: pd.DataFrame, y_test: pd.Series, max_mae: float) -> dict:
    """Return metrics; exit with status 1 if the MAE is above `max_mae`."""
    mae = mean_absolute_error(y_test, model.predict(X_test))
    print(f"MAE: ${mae:,.0f} (gate: ${max_mae:,.0f})")
    if mae > max_mae:
        print("EVALUATION GATE FAILED: model not saved.")
        raise SystemExit(1)
    return {"mae": round(float(mae), 2), "test_rows": int(len(y_test))}
