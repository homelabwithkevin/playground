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
## Project Structure

**Environment**:
- **Python**: 3.14.x
- **Web Framework**: Flask (for potential future web interface)
- **Data Format**: CSV (local file: `move_inventory.csv`)

**Design**: Core logic is split into separate `functions/*.py` modules for maintainability. The `inventory_manager.py` handles command-line parsing and serves as a single entry point that delegates to the `functions` module.

```
moving-inventory/
├── inventory_manager.py    # Main entry point for CLI/API usage
├── move_inventory.csv      # Data file with inventory records
├── ReadMe.md               # This file
│
├── functions/              # Modular function implementations
│   ├── __init__.py         # Exports all public functions
│   ├── add.py              # add_item() function
│   ├── update.py           # update_item() function
│   ├── delete.py           # delete_item() function
│   ├── list.py             # list_items() function
│   ├── search.py           # search_items() function
│   ├── count.py            # count_boxes() function
│   └── __pycache__/        # Bytecode cache
│
└── __pycache__/           # Bytecode cache for main modules
```

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