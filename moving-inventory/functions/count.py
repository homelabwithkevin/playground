import pandas as pd
from pathlib import Path


def count_boxes() -> str:
    """
    Count the total number of boxes in the inventory.

    Returns:
        String with the count
    """
    base_path = Path(__file__).parent.parent / "move_inventory.csv"
    # Use dtype=str to preserve leading zeros in box_id (e.g., "001" vs 1)
    df = pd.read_csv(base_path, dtype={'box_id': str})

    count = len(df)
    return f"Total boxes: {count}"
