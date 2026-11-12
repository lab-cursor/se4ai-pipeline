"""Optional: the same pipeline, orchestrated by Apache Airflow.

Each Airflow task calls one of YOUR stage functions from pipeline/, so finish
Task 1 first. Tasks hand over their results as files in out/airflow/, the way
real pipelines store intermediate results between stages.

Run it once in the terminal:    ./orchestration/airflow.sh dags test home_value_pipeline
Or open the web UI:             ./orchestration/airflow.sh standalone
"""
import sys
from datetime import datetime
from pathlib import Path

from airflow.sdk import dag, task

ROOT = Path(__file__).resolve().parents[2]   # repository root
sys.path.insert(0, str(ROOT))                # so `import pipeline` finds your code
WORK = ROOT / "out" / "airflow"              # intermediate results between tasks


@dag(
    dag_id="home_value_pipeline",
    schedule=None,                 # stretch goal: try "@weekly"
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["se4ai"],
)
def home_value_pipeline():

    @task
    def collect() -> str:
        from pipeline.collect import load_sales
        from run_pipeline import DATA_FILES

        WORK.mkdir(parents=True, exist_ok=True)
        raw = load_sales([ROOT / p for p in DATA_FILES])
        path = WORK / "raw.pkl"
        raw.to_pickle(path)
        print("collected", len(raw), "sales")
        return str(path)

    @task
    def clean(raw_path: str) -> str:
        import pandas as pd
        from pipeline.clean import clean_sales

        sales = clean_sales(pd.read_pickle(raw_path))
        path = WORK / "clean.pkl"
        sales.to_pickle(path)
        print("cleaned", len(sales), "sales")
        return str(path)

    @task
    def features(clean_path: str) -> str:
        import joblib
        import pandas as pd
        from pipeline.features import encode

        X, y = encode(pd.read_pickle(clean_path))
        path = WORK / "features.joblib"
        joblib.dump((X, y), path)
        return str(path)

    @task
    def train(features_path: str) -> str:
        import joblib
        from sklearn.model_selection import train_test_split
        from pipeline.train import train_model
        from run_pipeline import MAX_DEPTH

        X, y = joblib.load(features_path)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = train_model(X_train, y_train, max_depth=MAX_DEPTH)
        path = WORK / "candidate.joblib"
        joblib.dump((model, X_test, y_test), path)
        return str(path)

    @task
    def evaluate(candidate_path: str) -> dict:
        import json
        import joblib
        from pipeline.evaluate import evaluate as evaluate_gate
        from run_pipeline import MAX_MAE

        model, X_test, y_test = joblib.load(candidate_path)
        try:
            metrics = evaluate_gate(model, X_test, y_test, max_mae=MAX_MAE)
        except SystemExit:
            raise RuntimeError(f"Evaluation gate failed: MAE above {MAX_MAE:,}. Model not saved.")
        joblib.dump(model, ROOT / "out" / "model.joblib")
        (ROOT / "out" / "metrics.json").write_text(json.dumps(metrics, indent=2))
        return metrics

    evaluate(train(features(clean(collect()))))


home_value_pipeline()
