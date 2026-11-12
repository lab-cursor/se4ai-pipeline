"""Stage 4: train -- fit a model on the training split."""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

from train_all import X_train


def train_model(X: pd.DataFrame, y: pd.Series, max_depth: int) -> DecisionTreeRegressor:
    """Fit and return a decision-tree regressor with the given max_depth."""
    # TODO (Task 1): move the model-fitting lines of "4. train" here.
    # (The train/test split already lives in run_pipeline.py.)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = DecisionTreeRegressor(max_depth=8, random_state=0)
    model.fit(X_train, y_train)
    return model
