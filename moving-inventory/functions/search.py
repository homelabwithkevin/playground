import pandas as pd
from pathlib import Path


def search_items(query: str) -> str:
    """
    Search for items matching a query string in contents or notes.

    Args:
        query: Search term

    Returns:
        Formatted string with matching items
    """
    base_path = Path(__file__).parent.parent / "move_inventory.csv"
    # Use dtype=str to preserve leading zeros in box_id (e.g., "001" vs 1)
    df = pd.read_csv(base_path, dtype={'box_id': str})

    # Combine contents and notes for searching
    df["search_text"] = (df["contents"].fillna("") + " " + df["notes"].fillna("")).str.lower()
    mask = df["search_text"].str.contains(query.lower(), case=False, na=False)
    matches = df[mask]

    output = []
    output.append(f"=== Search Results for: '{query}' ===\n")

    if matches.empty:
        output.append("No matches found.")
    else:
        for _, row in matches.iterrows():
            output.append(f"Box {row['box_id']}:")
            output.append(f"  Contents: {row['contents'] if pd.notna(row['contents']) else '(empty)'}")
            output.append(f"  Notes: {row['notes'] if pd.notna(row['notes']) else '(none)'}")
            output.append("")

    output.append("=")
    return "".join(output)
