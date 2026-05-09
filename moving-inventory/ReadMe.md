# Moving Inventory System

> **AI-Generated Context**: This project was assisted by AI. Future collaborators should reference this documentation and any relevant PR descriptions for full context.

I am organizing a move and need assistance managing an inventory spreadsheet using Python.

---

## Tech Stack

- **Primary Data Format**: CSV (Local file: `move_inventory.csv`)
- **Python Libraries**: Pandas (for CLI)
- **Database**: None (Flat file based)

---

## CSV Schema Headers

| Column          | Description                 |
|-----------------|--------------------------   |
| `box_id`        | Unique identifier           |
| `contents`      | Contents description        |
| `notes`         | Additional notes/comments   |

---

## Project Goals
1. Track inventory

---

## Best Practices Established
- Label boxes with Box #

---

## How to Interact

### Using the Command Line Interface

```bash
# List all items
python inventory_manager.py list

# Add a new item (auto-generates box_id)
python inventory_manager.py add "winter coats" "garage"

# Add with specific box_id
python inventory_manager.py add "kitchen utensils" "box 001"

# Update an item's contents
python inventory_manager.py update 001 "new contents"

# Update an item's notes
python inventory_manager.py update 002 "some notes"

# Search for items
python inventory_manager.py search "winter"

# Delete an item
python inventory_manager.py delete 001

# Count boxes
python inventory_manager.py count
```

### Python API

```python
from inventory_manager import add_item, update_item, delete_item, list_items, search_items

# Add item
add_item("winter coats", notes="garage")

# Update item
update_item("001", contents="new contents")

# Search
search_items("winter")

# List all
list_items()
```