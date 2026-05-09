#!/usr/bin/env python3
"""Moving Inventory Manager - CSV-based inventory system for tracking items during a move."""

import csv
import os
from pathlib import Path
from datetime import datetime

# CSV file path
DEFAULT_CSV = Path(__file__).parent / "move_inventory.csv"

# Schema headers
SCHEMA = ["box_id", "contents", "notes"]


def create_csv() -> Path:
    """Create the CSV file with headers if it doesn't exist."""
    DEFAULT_CSV.touch()
    with open(DEFAULT_CSV, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=SCHEMA)
        writer.writeheader()
    print(f"Created inventory file: {DEFAULT_CSV}")
    return DEFAULT_CSV


def load_inventory() -> list[dict]:
    """Load all inventory items from CSV."""
    if not DEFAULT_CSV.exists():
        create_csv()
    items = []
    with open(DEFAULT_CSV, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            items.append(row)
    return items


def save_inventory(items: list[dict]) -> None:
    """Save all inventory items to CSV."""
    if not DEFAULT_CSV.exists():
        create_csv()
    with open(DEFAULT_CSV, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=SCHEMA)
        writer.writeheader()
        writer.writerows(items)


def add_item(contents: str, notes: str = "", box_id: str | None = None) -> dict:
    """Add a new item to the inventory."""
    items = load_inventory()

    if box_id is None:
        # Auto-generate box_id if not provided
        existing_ids = [int(item["box_id"]) for item in items if item["box_id"]]
        new_id = max(existing_ids, default=0) + 1
        box_id = f"{new_id:03d}"

    # Check if box_id already exists
    for item in items:
        if item["box_id"] == box_id:
            print(f"Warning: Box ID {box_id} already exists. Overwriting existing entry.")
            break

    new_item = {
        "box_id": box_id,
        "contents": contents,
        "notes": notes
    }

    items.append(new_item)
    save_inventory(items)

    print(f"Added item: {new_item}")
    return new_item


def update_item(box_id: str, contents: str | None = None,
                notes: str | None = None) -> dict | None:
    """Update an existing item by box_id."""
    items = load_inventory()

    for item in items:
        if item["box_id"] == box_id:
            if contents is not None:
                item["contents"] = contents
            if notes is not None:
                item["notes"] = notes
            save_inventory(items)
            print(f"Updated item {box_id}: {item}")
            return item

    print(f"Warning: Item with box_id {box_id} not found.")
    return None


def delete_item(box_id: str) -> bool:
    """Delete an item by box_id."""
    items = load_inventory()

    for i, item in enumerate(items):
        if item["box_id"] == box_id:
            del items[i]
            save_inventory(items)
            print(f"Deleted item: {item}")
            return True

    print(f"Warning: Item with box_id {box_id} not found.")
    return False


def list_items() -> list[dict]:
    """List all items in the inventory."""
    items = load_inventory()
    if not items:
        print("No items found in inventory.")
    else:
        print(f"\n{'Box ID':<10} {'Contents':<50} {'Notes':<30}")
        print("-" * 90)
        for item in items:
            contents = item["contents"][:47] + "..." if len(item["contents"]) > 50 else item["contents"]
            notes = item["notes"][:27] + "..." if len(item["notes"]) > 30 else item["notes"]
            print(f"{item['box_id']:<10} {contents:<50} {notes:<30}")
    return items


def search_items(query: str) -> list[dict]:
    """Search items by contents or notes."""
    items = load_inventory()
    query_lower = query.lower()

    results = [
        item for item in items
        if query_lower in item["contents"].lower() or query_lower in item["notes"].lower()
    ]

    if not results:
        print(f"No items found matching: '{query}'")
    else:
        print(f"\nFound {len(results)} item(s) matching '{query}':")
        for item in results:
            print(f"  [{item['box_id']}] {item['contents']}")
            if item["notes"]:
                print(f"         Notes: {item['notes']}")
    return results


def count_boxes() -> tuple[int, int]:
    """Count total boxes and items."""
    items = load_inventory()
    boxes_with_items = len(items)
    boxes_with_notes = sum(1 for item in items if item["notes"])
    return boxes_with_items, boxes_with_notes


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python inventory_manager.py <command> [args]")
        print("\nCommands:")
        print("  add <contents> [notes]           - Add new item (optional: box_id)")
        print("  update <box_id> <contents>       - Update item contents")
        print("  update <box_id> <notes>          - Update item notes")
        print("  delete <box_id>                  - Delete item")
        print("  list                             - List all items")
        print("  search <query>                   - Search items")
        print("  count                            - Count boxes")
        sys.exit(1)

    command = sys.argv[1]

    if command == "add":
        contents = " ".join(sys.argv[2:])
        if len(sys.argv) > 3:
            notes = sys.argv[3]
            add_item(contents, notes)
        else:
            add_item(contents)

    elif command == "update":
        if len(sys.argv) < 4:
            print("Usage: update <box_id> <contents|notes>")
            sys.exit(1)
        box_id = sys.argv[2]
        field = "contents" if len(sys.argv) == 4 and not sys.argv[3].lower().startswith("-") else "notes"
        value = " ".join(sys.argv[3:])
        update_item(box_id, contents=value if field == "contents" else None, notes=value if field == "notes" else None)

    elif command == "delete":
        box_id = sys.argv[2]
        delete_item(box_id)

    elif command == "list":
        list_items()

    elif command == "search":
        query = " ".join(sys.argv[2:])
        search_items(query)

    elif command == "count":
        total, with_notes = count_boxes()
        print(f"Total boxes: {total}")
        print(f"Boxes with notes: {with_notes}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
