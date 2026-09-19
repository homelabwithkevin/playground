import pandas as pd
from pathlib import Path


def update_item(
    box_id: str,
    contents: str | None = None,
    notes: str | None = None
) -> str:
    """
    Update an item's contents or notes.

    Both fields are appended to, not replaced. If a field is None, its
    existing value is preserved.

    Args:
        box_id: The box identifier to update
        contents: New content to append (or None to preserve existing)
        notes: New notes to append (or None to preserve existing)

    Returns:
        Success message with updated box_id
    """
    base_path = Path(__file__).parent.parent / "move_inventory.csv"
    df = pd.read_csv(base_path, dtype={"box_id": str, "notes": str})

    current_row = df[df["box_id"] == box_id]

    if current_row.empty:
        return f"Error: Box {box_id} not found"

    existing = current_row.iloc[0]
    existing_contents = existing.get("contents", "")
    existing_notes = existing.get("notes", "")

    # pandas converts empty CSV cells to pd.NA/NaN when dtype=str
    # Check for pd.NA, NaN, empty string, or None as "no value"
    if pd.isna(existing_contents):
        existing_contents = ""
    if pd.isna(existing_notes):
        existing_notes = ""

    # Append new content if provided, otherwise preserve existing
    if contents is not None:
        new_contents = f"{existing_contents} {contents}".strip()
    else:
        new_contents = existing_contents

    # Append new notes if provided AND there are existing notes, otherwise use provided or existing
    if notes is not None and existing_notes:
        new_notes = f"{existing_notes} {notes}".strip()
    elif notes is not None:
        # New notes provided but existing was empty, use new notes only
        new_notes = notes
    else:
        # No new notes provided, preserve existing (which is empty)
        new_notes = existing_notes

    # Only update fields that actually changed
    if new_contents != existing_contents:
        df.loc[df["box_id"] == box_id, "contents"] = new_contents
    if new_notes != existing_notes:
        df.loc[df["box_id"] == box_id, "notes"] = new_notes

    df.to_csv(base_path, index=False)

    return f"Updated box {box_id}: contents='{new_contents}', notes='{new_notes}'"
