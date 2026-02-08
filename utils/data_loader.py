"""
Data loading and cleaning utilities for the housing dashboard.

This module handles reading raw CSV data and transforming it
into a clean, long-format DataFrame ready for visualization.
"""

import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def load_zhvi_data() -> pd.DataFrame:
    """
    Load and reshape the Zillow Home Value Index data.

    The raw CSV has one row per state and one column per month (wide format).
    This function melts it into long format with columns:
        - state: State name
        - date: Month as a datetime
        - median_home_value: The ZHVI value in dollars

    Returns:
        pd.DataFrame in long format, sorted by state and date.

    Raises:
        FileNotFoundError: If the data file hasn't been downloaded yet.
    """
    filepath = os.path.join(DATA_DIR, "zhvi_by_state.csv")

    if not os.path.exists(filepath):
        raise FileNotFoundError(
            "Data file not found. Run 'python scripts/download_data.py' first."
        )

    df = pd.read_csv(filepath)

    # Identify date columns (they look like "2000-01-31")
    date_columns = [col for col in df.columns if col.startswith("20")]
    id_columns = ["RegionName"]  # State name

    # Melt from wide to long format
    df_long = df.melt(
        id_vars=id_columns,
        value_vars=date_columns,
        var_name="date",
        value_name="median_home_value",
    )

    # Clean up
    df_long = df_long.rename(columns={"RegionName": "state"})
    df_long["date"] = pd.to_datetime(df_long["date"])
    df_long = df_long.dropna(subset=["median_home_value"])
    df_long = df_long.sort_values(["state", "date"]).reset_index(drop=True)

    return df_long


def get_states(df: pd.DataFrame) -> list[str]:
    """Return a sorted list of unique state names."""
    return sorted(df["state"].unique().tolist())


def filter_data(
    df: pd.DataFrame,
    states: list[str] | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> pd.DataFrame:
    """
    Filter the dataset by state(s) and date range.

    Args:
        df: The full long-format DataFrame.
        states: List of state names to include. None means all states.
        start_date: Start date string (e.g., "2015-01-01"). None means no lower bound.
        end_date: End date string. None means no upper bound.

    Returns:
        Filtered DataFrame.
    """
    filtered = df.copy()

    if states:
        filtered = filtered[filtered["state"].isin(states)]

    if start_date:
        filtered = filtered[filtered["date"] >= pd.to_datetime(start_date)]

    if end_date:
        filtered = filtered[filtered["date"] <= pd.to_datetime(end_date)]

    return filtered
