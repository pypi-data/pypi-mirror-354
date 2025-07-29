# Plotting tools
import matplotlib.pyplot as plt
import pandas as pd

def plot_bar_count(df: pd.DataFrame, column: str, title: str = None):
    """Plot value counts for a specified column."""
    df[column].value_counts().plot(kind="bar")
    plt.title(title or f"Distribution by {column}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
