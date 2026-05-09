import pandas as pd
from pathlib import Path


def add_item(contents: str, box_id: str | None = None) -> str:
    """
    Add a new item to the inventory.

    Args:
        contents: Description of the item contents
        box_id: Optional box ID. Auto-generates if not provided.

    Returns:
        The generated or provided box_id
    """
    base_path = Path(__file__).parent.parent / "move_inventory.csv"
    # Use dtype=str to preserve leading zeros in box_id (e.g., "001" vs 1)
    df = pd.read_csv(base_path, dtype={'box_id': str})

    # Auto-generate box_id if not provided
    if box_id is None:
        max_id = df["box_id"].max()  # Already strings, no need to cast
        if max_id is None or max_id == "":
            # Empty CSV or no rows
            box_id = "001"
        else:
            # Remove leading zeros for arithmetic, then reformat
            try:
                num_id = int(max_id) + 1
                box_id = f"{num_id:03d}"
            except ValueError:
                # If max_id isn't numeric, start from "001"
                box_id = "001"
    else:
        # box_id was provided - use it as-is
        pass

    new_row = {"box_id": box_id, "contents": contents, "notes": ""}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    # Always write box_id as string to preserve formatting
    df["box_id"] = df["box_id"].astype(str)
    df.to_csv(base_path, index=False)

    return box_id
