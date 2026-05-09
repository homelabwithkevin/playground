import pandas as pd
from pathlib import Path


def update_item(box_id: str, contents: str | None = None, notes: str | None = None) -> str:
    """
    Update an item's contents or notes.
    Both fields are appended to, not replaced.

    Args:
        box_id: The box identifier to update
        contents: New content to append (or None if updating notes only)
        notes: New notes to append (or None if updating contents only)

    Returns:
        Success message with updated box_id
    """
    base_path = Path(__file__).parent.parent / "move_inventory.csv"
    # Use dtype=str to preserve leading zeros in box_id (e.g., "001" vs 1)
    df = pd.read_csv(base_path, dtype={'box_id': str})

    current_row = df[df["box_id"] == box_id]

    if current_row.empty:
        return f"Error: Box {box_id} not found"

    existing = current_row.iloc[0]
    existing_contents = existing.get("contents", "")
    existing_notes = existing.get("notes", "")

    if contents is not None:
        new_contents = contents
    else:
        new_contents = existing_contents

    if notes is not None:
        new_notes = notes
    else:
        new_notes = existing_notes

    df.loc[df["box_id"] == box_id, "contents"] = new_contents
    df.loc[df["box_id"] == box_id, "notes"] = new_notes
    df.to_csv(base_path, index=False)

    return f"Updated box {box_id}: contents='{new_contents}', notes='{new_notes}'"
