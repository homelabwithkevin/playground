#!/usr/bin/env python
"""
Moving Inventory System - CLI Entry Point

Usage:
    python inventory_manager.py list          # List all items
    python inventory_manager.py add "content" [box_id]  # Add item
    python inventory_manager.py update ID "new content" [notes]  # Update item
    python inventory_manager.py search "query"  # Search items
    python inventory_manager.py delete ID  # Delete item
    python inventory_manager.py count  # Count boxes
"""

import argparse
from functions import (
    add_item,
    update_item,
    delete_item,
    list_items,
    search_items,
    count_boxes,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Moving Inventory Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list - no arguments
    subparsers.add_parser("list", help="List all items")

    # add: contents (required), box_id (optional)
    add_parser = subparsers.add_parser("add", help="Add item")
    add_parser.add_argument("contents", help="Item contents")
    add_parser.add_argument("box_id", nargs="?", default=None, help="Box ID (auto-generated if omitted)")

    # update: box_id (required), contents (optional), notes (optional)
    update_parser = subparsers.add_parser("update", help="Update item")
    update_parser.add_argument("box_id", help="Box ID to update")
    update_parser.add_argument("contents", nargs="?", default=None, help="New contents (appended)")
    update_parser.add_argument("notes", nargs="?", default=None, help="New notes (appended)")

    # search: query (required)
    search_parser = subparsers.add_parser("search", help="Search items")
    search_parser.add_argument("query", help="Search term")

    # delete: box_id (required)
    delete_parser = subparsers.add_parser("delete", help="Delete item")
    delete_parser.add_argument("box_id", help="Box ID to delete")

    # count - no arguments
    subparsers.add_parser("count", help="Count boxes")

    args = parser.parse_args()

    # Handle each command
    if args.command == "list":
        print(list_items())
    elif args.command == "add":
        if args.contents is None:
            print("Error: Contents required for add")
        else:
            if args.box_id:
                result = add_item(args.contents, box_id=args.box_id)
            else:
                result = add_item(args.contents)
            print(result)
    elif args.command == "update":
        if args.box_id is None:
            print("Error: Box ID required for update")
        else:
            result = update_item(
                box_id=args.box_id,
                contents=args.contents,
                notes=args.notes
            )
            print(result)
    elif args.command == "delete":
        if args.box_id is None:
            print("Error: Box ID required for delete")
        else:
            result = delete_item(args.box_id)
            print(result)
    elif args.command == "count":
        print(count_boxes())
    elif args.command == "search":
        if args.query is None:
            print("Error: Search term required")
        else:
            print(search_items(args.query))


if __name__ == "__main__":
    main()
