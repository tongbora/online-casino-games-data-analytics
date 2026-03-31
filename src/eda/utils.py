"""Utility helpers for EDA workflows."""
from pathlib import Path
from typing import Optional

import pandas as pd

# Load data
def load_csv(path: Path | str, *, nrows: Optional[int] = None) -> pd.DataFrame:
    """Load a CSV file with sensible defaults for large datasets."""
    path = path.expanduser() if isinstance(path, Path) else path
    return pd.read_csv(path, nrows=nrows, low_memory=False)


def summarize_dataframe(df: pd.DataFrame) -> dict:
    """Return quick dataset metadata useful for notebook reporting."""
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "dtypes": df.dtypes.to_dict(),
        "missing_per_column": df.isna().sum().to_dict(),
    }


def top_categories(df: pd.DataFrame, column: str, n: int = 10) -> pd.DataFrame:
    """Return top categories with counts and share."""
    counts = df[column].value_counts(dropna=False).head(n)
    total = len(df)
    return (
        counts.rename_axis(column)
        .reset_index(name="count")
        .assign(share=lambda t: t["count"] / total)
    )
