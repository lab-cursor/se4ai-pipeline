"""Stage 4: train -- fit a model on the training split."""
import pandas as pd
from sklearn.tree import DecisionTreeRegressor


def train_model(X: pd.DataFrame, y: pd.Series, max_depth: int) -> DecisionTreeRegressor:
    """Fit and return a decision-tree regressor with the given max_depth."""
    # TODO (Task 1): move the model-fitting lines of "4. train" here.
    # Use the `max_depth` parameter, not the fixed 8 from the script.
    # Don't split the data here: the train/test split already lives in run_pipeline.py.
    raise NotImplementedError("train.train_model: move the code from train_all.py")
