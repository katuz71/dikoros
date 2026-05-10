"""
Sync tasks from tasks.yaml into Notion "Задачи" database.

Idempotent: matches existing tasks by slug (in Комментарии field as marker).
Two-pass: pass 1 creates/updates pages, pass 2 sets relations.

Usage:
    python notion-sync.py --dry-run    # show what will happen
    python notion-sync.py --apply      # actually write to Notion
"""
import argparse
import os
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

TOKEN = os.getenv("NOTION_TOKEN")
DATA_SOURCE_ID = os.getenv("NOTION_TASKS_DATA_SOURCE_ID")
TASKS_FILE = Path(__file__).parent / "tasks.yaml"

SLUG_MARKER = "sync-slug:"


def die(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def load_tasks() -> list[dict]:
    if not TASKS_FILE.exists():
        die(f"{TASKS_FILE} not found")
    with TASKS_FILE.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, list):
        die("tasks.yaml must be a list of task dicts")
    return data


def fetch_existing(notion: Client) -> dict[str, dict]:
    """Return slug -> page mapping for already-synced tasks."""
    existing = {}
    cursor = None
    while True:
        kwargs = {"data_source_id": DATA_SOURCE_ID, "page_size": 100}
        if cursor:
            kwargs["start_cursor"] = cursor
        resp = notion.data_sources.query(**kwargs)
        for page in resp.get("results", []):
            comm = page.get("properties", {}).get("Комментарии", {}).get("rich_text", [])
            text = "".join(p.get("plain_text", "") for p in comm)
            if SLUG_MARKER in text:
                slug = text.split(SLUG_MARKER, 1)[1].split()[0].strip()
                if slug:
                    existing[slug] = page
        if not resp.get("has_more"):
            break
        cursor = resp.get("next_cursor")
    return existing


def build_properties(task: dict) -> dict:
    """Convert task dict to Notion properties payload."""
    props: dict = {
        "Название": {
            "title": [{"text": {"content": task["title"]}}]
        },
        "Комментарии": {
            "rich_text": [{
                "text": {
                    "content": f"{SLUG_MARKER}{task['slug']}\n\n{task.get('description', '')}"
                }
            }]
        },
    }

    if "status" in task:
        props["Статус"] = {"select": {"name": task["status"]}}
    if "priority" in task:
        props["Приоритет"] = {"select": {"name": task["priority"]}}
    if "category" in task:
        props["Категория"] = {"select": {"name": task["category"]}}
    if "month" in task:
        month_map = {
            "Месяц 1": "Месяц 1 — Май",
            "Месяц 2": "Месяц 2 — Июнь",
            "Месяц 3": "Месяц 3 — Июль",
            "Месяц 4": "Месяц 4 — Август",
            "Месяц 5": "Месяц 5 — Сентябрь",
        }
        month_value = month_map.get(task["month"], task["month"])
        props["Месяц"] = {"select": {"name": month_value}}
    if "week" in task:
        props["Неделя"] = {"select": {"name": task["week"]}}
    if "assignee" in task:
        props["Ответственный"] = {"select": {"name": task["assignee"]}}
    if "estimate_hours" in task:
        props["Оценка часов"] = {"number": float(task["estimate_hours"])}
    if "actual_hours" in task:
        props["Фактически часов"] = {"number": float(task["actual_hours"])}
    if task.get("start_date"):
        props["Дата начала"] = {"date": {"start": task["start_date"].isoformat() if hasattr(task["start_date"], "isoformat") else str(task["start_date"])}}
    if task.get("end_date"):
        props["Дата завершения"] = {"date": {"start": task["end_date"].isoformat() if hasattr(task["end_date"], "isoformat") else str(task["end_date"])}}

    return props


def create_or_update(notion: Client, task: dict, existing: dict, dry_run: bool) -> str | None:
    slug = task.get("slug")
    if not slug:
        print(f"  SKIP (no slug): {task.get('title')}")
        return None

    props = build_properties(task)

    if slug in existing:
        page_id = existing[slug]["id"]
        print(f"  UPDATE  [{slug}] {task['title']}")
        if not dry_run:
            notion.pages.update(page_id=page_id, properties=props)
        return page_id
    else:
        print(f"  CREATE  [{slug}] {task['title']}")
        if not dry_run:
            page = notion.pages.create(
                parent={"data_source_id": DATA_SOURCE_ID},
                properties=props,
            )
            return page["id"]
        return None


def set_relations(notion: Client, tasks: list[dict], slug_to_page_id: dict, dry_run: bool) -> None:
    for task in tasks:
        slug = task.get("slug")
        depends_on = task.get("depends_on", [])
        blocks = task.get("blocks", [])

        if not depends_on and not blocks:
            continue

        page_id = slug_to_page_id.get(slug)
        if not page_id:
            continue

        props: dict = {}
        if depends_on:
            ids = [{"id": slug_to_page_id[s]} for s in depends_on if s in slug_to_page_id]
            if ids:
                props["Зависит от"] = {"relation": ids}
        if blocks:
            ids = [{"id": slug_to_page_id[s]} for s in blocks if s in slug_to_page_id]
            if ids:
                props["Блокирует"] = {"relation": ids}

        if props:
            print(f"  RELATIONS [{slug}] depends_on={len(depends_on)} blocks={len(blocks)}")
            if not dry_run:
                notion.pages.update(page_id=page_id, properties=props)


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true", help="Show what would happen")
    group.add_argument("--apply", action="store_true", help="Actually write to Notion")
    args = parser.parse_args()

    if not TOKEN:
        die("NOTION_TOKEN not set in .env")
    if not DATA_SOURCE_ID:
        die("NOTION_TASKS_DATA_SOURCE_ID not set in .env")

    dry_run = args.dry_run
    mode = "DRY RUN" if dry_run else "APPLY"
    print(f"=== Notion task sync — mode: {mode} ===\n")

    notion = Client(auth=TOKEN)
    tasks = load_tasks()
    print(f"Loaded {len(tasks)} tasks from tasks.yaml")

    slugs = [t.get("slug") for t in tasks if t.get("slug")]
    if len(slugs) != len(set(slugs)):
        die("Duplicate slugs in tasks.yaml — fix before sync")

    print("Fetching existing tasks from Notion...")
    existing = fetch_existing(notion)
    print(f"Found {len(existing)} previously synced tasks\n")

    print("=== Pass 1: create / update tasks ===")
    slug_to_page_id: dict[str, str] = {}
    for task in tasks:
        page_id = create_or_update(notion, task, existing, dry_run)
        slug = task.get("slug")
        if slug:
            if page_id:
                slug_to_page_id[slug] = page_id
            elif slug in existing:
                slug_to_page_id[slug] = existing[slug]["id"]

    print("\n=== Pass 2: set relations ===")
    set_relations(notion, tasks, slug_to_page_id, dry_run)

    print(f"\n=== Done ({mode}) ===")
    if dry_run:
        print("Run with --apply to actually write changes.")


if __name__ == "__main__":
    main()
