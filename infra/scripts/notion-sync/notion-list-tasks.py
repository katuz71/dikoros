#!/usr/bin/env python3
"""
Выгружает все задачи из Notion-базы и группирует:
- наши (с маркером sync-slug в свойстве "Комментарии")
- чужие (без маркера, существовавшие до синхронизации)
"""
import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()
NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATA_SOURCE_ID = os.environ["NOTION_TASKS_DATA_SOURCE_ID"]
SLUG_MARKER = "sync-slug:"

notion = Client(auth=NOTION_TOKEN)

def get_title(page):
    for prop in page["properties"].values():
        if prop["type"] == "title":
            parts = prop.get("title", [])
            return "".join(p.get("plain_text", "") for p in parts) or "(без названия)"
    return "(нет title-поля)"

def get_select(page, prop_name):
    prop = page["properties"].get(prop_name, {})
    if prop.get("type") == "select":
        s = prop.get("select")
        return s.get("name") if s else "—"
    return "—"

def get_slug_from_comments(page):
    comm = page.get("properties", {}).get("Комментарии", {}).get("rich_text", [])
    text = "".join(p.get("plain_text", "") for p in comm)
    if SLUG_MARKER in text:
        return text.split(SLUG_MARKER, 1)[1].split()[0].strip()
    return None

# Запрос всех страниц с пагинацией
all_pages = []
cursor = None
while True:
    kwargs = {"data_source_id": DATA_SOURCE_ID, "page_size": 100}
    if cursor:
        kwargs["start_cursor"] = cursor
    resp = notion.data_sources.query(**kwargs)
    all_pages.extend(resp.get("results", []))
    if not resp.get("has_more"):
        break
    cursor = resp.get("next_cursor")

print(f"\n=== Всего страниц в базе: {len(all_pages)} ===\n")

ours = []
others = []
for page in all_pages:
    title = get_title(page)
    status = get_select(page, "Статус")
    month = get_select(page, "Месяц")
    assignee = get_select(page, "Ответственный")
    slug = get_slug_from_comments(page)
    if slug:
        ours.append((slug, title, status, month, assignee))
    else:
        others.append((page["id"][:8], title, status))

print(f"=== Наши (с sync-slug): {len(ours)} ===")
for slug, title, status, month, assignee in sorted(ours):
    print(f"  [{slug:35}] {status:14} | {month:18} | {assignee:12} | {title[:50]}")

print(f"\n=== Чужие (без sync-slug): {len(others)} ===")
for pid, title, status in others:
    print(f"  [{pid}] {status:14} | {title[:80]}")
