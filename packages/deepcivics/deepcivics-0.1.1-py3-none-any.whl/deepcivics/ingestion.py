# Data ingestion logic
import pandas as pd

def fetch_csv(url: str) -> pd.DataFrame:
    """Load CSV from a public .gov or data portal link."""
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        raise RuntimeError(f"Failed to load data from {url}: {e}")

def preview_columns(df: pd.DataFrame) -> list:
    return df.columns.tolist()
