"""
DIKOROS site SEO crawler.
Reads URLs from CSV (columns: url, type, lang), fetches each with a Chrome UA,
extracts SEO metadata, writes pages.csv.

Usage:
    python crawl.py --input urls.csv --output pages.csv [--limit N] [--rps 1.0]
"""

import argparse
import asyncio
import csv
import html
import sys
import time
from pathlib import Path

import httpx
from selectolax.parser import HTMLParser
from tqdm import tqdm

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)
HEADERS = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "uk-UA,uk;q=0.9,en;q=0.8,ru;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
}

FIELDNAMES = [
    "url", "type", "lang",
    "http_status", "final_url", "redirect_chain",
    "content_length", "last_modified", "content_type",
    "title", "description", "h1",
    "canonical", "robots",
    "og_title", "og_description", "og_image", "og_locale", "og_type",
    "hreflang_count", "hreflang_list",
    "elapsed_ms", "error",
]


def clean(text: str | None) -> str:
    """Decode HTML entities and collapse whitespace."""
    if not text:
        return ""
    return " ".join(html.unescape(text).split())


def attr(node, name: str) -> str:
    return clean(node.attributes.get(name, "")) if node else ""


def first_text(tree: HTMLParser, selector: str) -> str:
    node = tree.css_first(selector)
    return clean(node.text()) if node else ""


def first_attr(tree: HTMLParser, selector: str, attr_name: str) -> str:
    node = tree.css_first(selector)
    return attr(node, attr_name) if node else ""


def extract(html_text: str) -> dict:
    tree = HTMLParser(html_text)

    title = first_text(tree, "title")
    description = first_attr(tree, 'meta[name="description"]', "content")
    h1 = first_text(tree, "h1")
    canonical = first_attr(tree, 'link[rel="canonical"]', "href")
    robots = first_attr(tree, 'meta[name="robots"]', "content")

    og_title = first_attr(tree, 'meta[property="og:title"]', "content")
    og_description = first_attr(tree, 'meta[property="og:description"]', "content")
    og_image = first_attr(tree, 'meta[property="og:image"]', "content")
    og_locale = first_attr(tree, 'meta[property="og:locale"]', "content")
    og_type = first_attr(tree, 'meta[property="og:type"]', "content")

    hreflang_nodes = tree.css('link[rel="alternate"][hreflang]')
    hreflang_list = "|".join(
        f"{attr(n, 'hreflang')}={attr(n, 'href')}" for n in hreflang_nodes
    )

    return {
        "title": title,
        "description": description,
        "h1": h1,
        "canonical": canonical,
        "robots": robots,
        "og_title": og_title,
        "og_description": og_description,
        "og_image": og_image,
        "og_locale": og_locale,
        "og_type": og_type,
        "hreflang_count": len(hreflang_nodes),
        "hreflang_list": hreflang_list,
    }


async def fetch_one(client: httpx.AsyncClient, row: dict, sem: asyncio.Semaphore,
                    rps: float) -> dict:
    """Fetch one URL, throttled to <=rps requests per second globally via sem."""
    url = row["url"]
    result = {
        "url": url, "type": row.get("type", ""), "lang": row.get("lang", ""),
        "http_status": "", "final_url": "", "redirect_chain": "",
        "content_length": "", "last_modified": "", "content_type": "",
        "title": "", "description": "", "h1": "",
        "canonical": "", "robots": "",
        "og_title": "", "og_description": "", "og_image": "",
        "og_locale": "", "og_type": "",
        "hreflang_count": 0, "hreflang_list": "",
        "elapsed_ms": "", "error": "",
    }

    async with sem:
        await asyncio.sleep(1.0 / rps)
        t0 = time.perf_counter()
        try:
            resp = await client.get(url, follow_redirects=True, timeout=30.0)
            elapsed = int((time.perf_counter() - t0) * 1000)
            result["http_status"] = resp.status_code
            result["final_url"] = str(resp.url)
            result["redirect_chain"] = " -> ".join(str(h.url) for h in resp.history) or ""
            result["content_length"] = len(resp.content)
            result["last_modified"] = resp.headers.get("last-modified", "")
            result["content_type"] = resp.headers.get("content-type", "")
            result["elapsed_ms"] = elapsed

            ctype = result["content_type"].lower()
            if resp.status_code == 200 and "html" in ctype:
                meta = extract(resp.text)
                result.update(meta)
        except Exception as e:
            result["error"] = f"{type(e).__name__}: {e}"
    return result


async def main_async(args):
    rows = list(csv.DictReader(open(args.input, encoding="utf-8")))
    if args.limit:
        rows = rows[: args.limit]

    sem = asyncio.Semaphore(1)  # strict 1 req/sec for politeness
    limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)

    async with httpx.AsyncClient(headers=HEADERS, http2=True, limits=limits) as client:
        tasks = [fetch_one(client, r, sem, args.rps) for r in rows]
        results = []
        for coro in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="crawl"):
            results.append(await coro)

    # preserve input order
    order = {r["url"]: i for i, r in enumerate(rows)}
    results.sort(key=lambda r: order.get(r["url"], 1_000_000))

    with open(args.output, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(results)

    ok = sum(1 for r in results if r["http_status"] == 200)
    err = sum(1 for r in results if r["error"])
    print(f"\nDone. {len(results)} URLs, {ok} OK (200), {err} errors. -> {args.output}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--rps", type=float, default=1.0,
                   help="requests per second (global, default 1.0)")
    args = p.parse_args()
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
