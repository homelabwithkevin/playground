import pandas as pd
from pathlib import Path
import numpy as np


def list_items() -> str:
    """
    List all items in the inventory.

    Returns:
        Formatted string with all inventory items
    """
    base_path = Path(__file__).parent.parent / "move_inventory.csv"
    # Use dtype=str to preserve leading zeros in box_id (e.g., "001" vs 1)
    df = pd.read_csv(base_path, dtype={'box_id': str})

    output = []
    output.append("=== Moving Inventory ===\n")

    for _, row in df.iterrows():
        box_id = str(row["box_id"])
        contents = row["contents"] if pd.notna(row["contents"]) else "(empty)"
        notes = row["notes"] if pd.notna(row["notes"]) else "(none)"
        output.append(f"Box {box_id}:")
        output.append(f"  Contents: {contents}")
        output.append(f"  Notes: {notes}")
        output.append("")

    return "".join(output)
