"""
Notion data source inspector (Notion API 2025-09).
Lists all data sources accessible to the integration and prints schema.

Usage:
    python notion-inspect.py
"""
import os
import sys
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

token = os.getenv("NOTION_TOKEN")
if not token:
    print("ERROR: NOTION_TOKEN not found in .env", file=sys.stderr)
    sys.exit(1)

notion = Client(auth=token)

print("=" * 70)
print("Searching for data sources accessible to this integration...")
print("=" * 70)

try:
    response = notion.search(
        filter={"property": "object", "value": "data_source"},
        page_size=100,
    )
except Exception as e:
    print(f"\nSearch with data_source failed: {e}")
    print("Falling back to page search to list parent pages...")
    response = notion.search(page_size=100)

results = response.get("results", [])

if not results:
    print("\nNo data sources found. Make sure the integration is connected")
    print("to your database (... menu in database -> Connections -> Add).")
    sys.exit(1)

print(f"\nFound {len(results)} item(s):\n")

for i, item in enumerate(results, 1):
    obj_type = item.get("object", "unknown")
    item_id = item.get("id", "")

    title_parts = item.get("title", [])
    if not title_parts and "name" in item:
        title = item.get("name", "")
    else:
        title = "".join(p.get("plain_text", "") for p in title_parts) or "(untitled)"

    print(f"{'=' * 70}")
    print(f"[{i}] {title}")
    print(f"    Object type: {obj_type}")
    print(f"    ID: {item_id}")
    print(f"    URL: {item.get('url', '(no url)')}")
    print(f"{'=' * 70}")

    properties = item.get("properties", {})
    if properties:
        print(f"\n    Properties ({len(properties)}):\n")
        for prop_name, prop_data in properties.items():
            prop_type = prop_data.get("type", "unknown")
            line = f"      - {prop_name}  [{prop_type}]"

            if prop_type in ("select", "multi_select", "status"):
                options_data = prop_data.get(prop_type, {})
                options = options_data.get("options", [])
                if options:
                    opt_names = [o.get("name", "") for o in options]
                    line += f"  options: {opt_names}"

            if prop_type == "relation":
                relation_data = prop_data.get("relation", {})
                target_db = relation_data.get("database_id", "") or relation_data.get("data_source_id", "")
                line += f"  -> {target_db}"

            print(line)
    else:
        print("\n    (No properties — this is likely a page, not a database)")

    print()

print("=" * 70)
print("Done. Send the output to your assistant.")
print("=" * 70)
