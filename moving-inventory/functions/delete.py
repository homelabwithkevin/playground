import pandas as pd
from pathlib import Path


def delete_item(box_id: str) -> str:
    """
    Delete an item from the inventory.

    Args:
        box_id: The box identifier to delete

    Returns:
        Result message
    """
    base_path = Path(__file__).parent.parent / "move_inventory.csv"
    # Use dtype=str to preserve leading zeros in box_id (e.g., "001" vs 1)
    df = pd.read_csv(base_path, dtype={'box_id': str})

    current_row = df[df["box_id"] == box_id]

    if current_row.empty:
        return f"Error: Box {box_id} not found"

    df = df[df["box_id"] != box_id].reset_index(drop=True)
    df.to_csv(base_path, index=False)

    return f"Deleted box {box_id}"
