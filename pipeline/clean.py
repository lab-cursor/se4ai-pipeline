"""Stage 2: clean -- fix types and drop rows we cannot trust."""
import pandas as pd


def clean_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy of the raw sales.

    Guarantees for the next stage:
      * sold_date is a datetime column
      * sqft has no missing values
      * rows with an obviously wrong price (<= 10,000) are removed
    """
    # TODO (Task 1): move the "2. clean" block from train_all.py here.
    # TODO (Task 2): make it work for data/sales_2026_q1.csv as well
    #                (run `pytest` to see what is expected).
    raise NotImplementedError("clean.clean_sales: move the code from train_all.py")
