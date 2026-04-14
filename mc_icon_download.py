#!/usr/bin/env python3
"""Utilities for searching and downloading Minecraft assets from ccvaults.com.

This script uses the same API flow as the site:
1. POST /api/token with the site api key and required origin headers
2. GET metadata endpoints with the bearer token
3. Download image files directly from public asset URLs

It intentionally uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, List, Optional


BASE_URL = "https://ccvaults.com"
API_KEY = "mcicons-apikey-0201osaiudx-24493534"
TOKEN_PATH = "/api/token"
TOKEN_TTL_SECONDS = 15 * 60
DEFAULT_TIMEOUT = 30

ROOT_DIR = Path(__file__).resolve().parent
CACHE_DIR = ROOT_DIR / "cache"
OUTPUT_DIR = ROOT_DIR / "downloads"
TOKEN_CACHE_PATH = CACHE_DIR / "token.json"
ICONS_INDEX_PATH = CACHE_DIR / "icons_index.json"
TEXTURES_INDEX_PATH = CACHE_DIR / "textures_index.json"


@dataclass
class AssetRecord:
    kind: str
    file: str
    name: str
    category: Optional[str]
    subcategory: Optional[str]
    url: str
    thumbnail_url: Optional[str]

    @property
    def slug(self) -> str:
        parts = [self.kind]
        if self.category:
            parts.append(self.category)
        if self.subcategory:
            parts.append(self.subcategory)
        parts.append(self.file)
        return " / ".join(parts)


def ensure_dirs() -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def json_dump(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def json_load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def make_request(
    url: str,
    *,
    method: str = "GET",
    headers: Optional[dict[str, str]] = None,
    data: Optional[bytes] = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> bytes:
    req = urllib.request.Request(url, data=data, method=method)
    for key, value in (headers or {}).items():
        req.add_header(key, value)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} for {url}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error for {url}: {exc}") from exc


def token_headers() -> dict[str, str]:
    return {
        "x-api-key": API_KEY,
        "content-type": "application/json",
        "Origin": BASE_URL,
        "Referer": f"{BASE_URL}/",
    }


def auth_headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Origin": BASE_URL,
        "Referer": f"{BASE_URL}/",
    }


def get_token(force_refresh: bool = False) -> str:
    ensure_dirs()
    if not force_refresh and TOKEN_CACHE_PATH.exists():
        cached = json_load(TOKEN_CACHE_PATH)
        expires_at = float(cached.get("expires_at", 0))
        if time.time() < expires_at - 60:
            token = cached.get("token")
            if token:
                return token

    body = make_request(
        f"{BASE_URL}{TOKEN_PATH}",
        method="POST",
        headers=token_headers(),
        data=b"{}",
    )
    payload = json.loads(body.decode("utf-8"))
    token = payload.get("token")
    if not token:
        raise RuntimeError(f"Token response missing token field: {payload}")

    json_dump(
        TOKEN_CACHE_PATH,
        {
            "token": token,
            "fetched_at": time.time(),
            "expires_at": time.time() + TOKEN_TTL_SECONDS,
        },
    )
    return token


def api_get(path: str, *, force_refresh_token: bool = False) -> object:
    token = get_token(force_refresh=force_refresh_token)
    try:
        body = make_request(f"{BASE_URL}{path}", headers=auth_headers(token))
    except RuntimeError as exc:
        if "HTTP 401" in str(exc) or "HTTP 403" in str(exc):
            token = get_token(force_refresh=True)
            body = make_request(f"{BASE_URL}{path}", headers=auth_headers(token))
        else:
            raise
    return json.loads(body.decode("utf-8"))


def encode_path_parts(parts: Iterable[str]) -> str:
    return "/".join(urllib.parse.quote(part, safe="") for part in parts)


def build_icon_url(category: str, file: str, subcategory: Optional[str] = None) -> str:
    parts = ["assets", category]
    if subcategory:
        parts.append(subcategory)
    parts.append(file)
    return f"{BASE_URL}/{encode_path_parts(parts)}"


def build_thumbnail_url(category: str, file: str, subcategory: Optional[str] = None) -> str:
    parts = ["thumbnails", category]
    if subcategory:
        parts.append(subcategory)
    parts.append(file)
    return f"{BASE_URL}/{encode_path_parts(parts)}"


def build_texture_url(file: str) -> str:
    return f"{BASE_URL}/{encode_path_parts(['textures', file])}"


def normalize_name(file: str) -> str:
    stem = re.sub(r"\.[^.]+$", "", file)
    return stem.replace("_", " ")


def fetch_categories() -> list[dict]:
    payload = api_get("/api/categories")
    if not isinstance(payload, list):
        raise RuntimeError(f"Unexpected categories payload: {type(payload)}")
    return payload


def fetch_icons_index() -> list[AssetRecord]:
    payload = api_get("/api/assets/all")
    if not isinstance(payload, list) or len(payload) < 2:
        raise RuntimeError(f"Unexpected /api/assets/all payload shape: {type(payload)}")
    files = payload[1].get("files", [])
    records: list[AssetRecord] = []
    for item in files:
        category = item["category"]
        subcategory = item.get("subcategory")
        file = item["file"]
        records.append(
            AssetRecord(
                kind="icon",
                file=file,
                name=normalize_name(file),
                category=category,
                subcategory=subcategory,
                url=build_icon_url(category, file, subcategory),
                thumbnail_url=build_thumbnail_url(category, file, subcategory),
            )
        )
    return records


def fetch_textures_index() -> list[AssetRecord]:
    payload = api_get("/api/textures")
    files = payload.get("files", [])
    records: list[AssetRecord] = []
    for item in files:
        file = item["file"] if isinstance(item, dict) else item
        records.append(
            AssetRecord(
                kind="texture",
                file=file,
                name=normalize_name(file),
                category=None,
                subcategory=None,
                url=build_texture_url(file),
                thumbnail_url=None,
            )
        )
    return records


def save_index(kind: str, records: list[AssetRecord]) -> Path:
    ensure_dirs()
    path = ICONS_INDEX_PATH if kind == "icon" else TEXTURES_INDEX_PATH
    json_dump(path, [asdict(record) for record in records])
    return path


def load_index(kind: str) -> list[AssetRecord]:
    path = ICONS_INDEX_PATH if kind == "icon" else TEXTURES_INDEX_PATH
    if not path.exists():
        raise RuntimeError(
            f"Index file not found: {path}. Run 'index --kind {kind}' first."
        )
    payload = json_load(path)
    return [AssetRecord(**item) for item in payload]


def get_records(kind: str, refresh: bool = False) -> list[AssetRecord]:
    if refresh:
        records = fetch_icons_index() if kind == "icon" else fetch_textures_index()
        save_index(kind, records)
        return records
    try:
        return load_index(kind)
    except RuntimeError:
        records = fetch_icons_index() if kind == "icon" else fetch_textures_index()
        save_index(kind, records)
        return records


def filter_records(
    records: list[AssetRecord],
    *,
    query: Optional[str] = None,
    exact: bool = False,
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
) -> list[AssetRecord]:
    out = records
    if category:
        out = [record for record in out if record.category == category]
    if subcategory:
        out = [record for record in out if record.subcategory == subcategory]
    if query:
        needle = query.casefold().strip()
        if exact:
            out = [
                record
                for record in out
                if record.file.casefold() == needle
                or record.name.casefold() == needle
            ]
        else:
            out = [
                record
                for record in out
                if needle in record.file.casefold()
                or needle in record.name.casefold()
            ]
    return out


def choose_records(
    records: list[AssetRecord],
    *,
    first: bool = False,
    limit: Optional[int] = None,
) -> list[AssetRecord]:
    if first and records:
        return [records[0]]
    if limit is not None:
        return records[:limit]
    return records


def download_file(url: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "mc-icon-download/1.0"})
    with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
        path.write_bytes(resp.read())


def default_output_path(record: AssetRecord, base_dir: Path) -> Path:
    parts = [record.kind]
    if record.category:
        parts.append(record.category)
    if record.subcategory:
        parts.append(record.subcategory)
    path = base_dir
    for part in parts:
        path = path / sanitize_filename(part)
    return path / sanitize_filename(record.file)


def sanitize_filename(name: str) -> str:
    name = name.strip().replace("/", "_")
    return re.sub(r"[<>:\"\\\\|?*]", "_", name)


def print_records(records: list[AssetRecord], *, as_json: bool = False) -> None:
    if as_json:
        json.dump([asdict(record) for record in records], sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return

    for index, record in enumerate(records, start=1):
        print(f"[{index}] {record.slug}")
        print(f"    url: {record.url}")
        if record.thumbnail_url:
            print(f"    thumbnail: {record.thumbnail_url}")


def export_records(records: list[AssetRecord], path: Path, fmt: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fmt == "json":
        json_dump(path, [asdict(record) for record in records])
        return

    with path.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(
            fp,
            fieldnames=["kind", "file", "name", "category", "subcategory", "url", "thumbnail_url"],
        )
        writer.writeheader()
        for record in records:
            writer.writerow(asdict(record))


def cmd_categories(args: argparse.Namespace) -> int:
    categories = fetch_categories()
    if args.json:
        json.dump(categories, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0

    for item in categories:
        print(f"{item['category']}: {item['fileCount']}")
    return 0


def cmd_index(args: argparse.Namespace) -> int:
    kind = args.kind
    records = fetch_icons_index() if kind == "icon" else fetch_textures_index()
    path = save_index(kind, records)
    print(f"Saved {len(records)} {kind} records to {path}")
    return 0


def query_records_from_args(args: argparse.Namespace) -> list[AssetRecord]:
    records = get_records(args.kind, refresh=args.refresh)
    records = filter_records(
        records,
        query=args.query,
        exact=args.exact,
        category=getattr(args, "category", None),
        subcategory=getattr(args, "subcategory", None),
    )
    records = choose_records(records, first=getattr(args, "first", False), limit=getattr(args, "limit", None))
    return records


def cmd_search(args: argparse.Namespace) -> int:
    records = query_records_from_args(args)
    print_records(records, as_json=args.json)
    if not records:
        print("No records matched.", file=sys.stderr)
        return 1
    return 0


def cmd_urls(args: argparse.Namespace) -> int:
    records = query_records_from_args(args)
    if not records:
        print("No records matched.", file=sys.stderr)
        return 1
    for record in records:
        print(record.url)
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    records = query_records_from_args(args)
    path = Path(args.output).expanduser().resolve()
    export_records(records, path, args.format)
    print(f"Exported {len(records)} records to {path}")
    return 0


def cmd_download(args: argparse.Namespace) -> int:
    records = query_records_from_args(args)
    if not records:
        print("No records matched.", file=sys.stderr)
        return 1

    if not args.all and len(records) > 1 and not args.first and args.limit is None:
        print(
            "More than one record matched. Use --first, --limit, or --all.",
            file=sys.stderr,
        )
        return 2

    out_dir = Path(args.output_dir).expanduser().resolve()
    for record in records:
        target = default_output_path(record, out_dir)
        download_file(record.url, target)
        print(f"Downloaded {record.slug} -> {target}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Search, export, and download Minecraft assets from ccvaults.com",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    categories = subparsers.add_parser("categories", help="List categories from the remote API")
    categories.add_argument("--json", action="store_true", help="Print raw JSON")
    categories.set_defaults(func=cmd_categories)

    index = subparsers.add_parser("index", help="Fetch and cache an index")
    index.add_argument("--kind", choices=["icon", "texture"], required=True)
    index.set_defaults(func=cmd_index)

    def add_query_flags(p: argparse.ArgumentParser, *, include_output_dir: bool = False) -> None:
        p.add_argument("--kind", choices=["icon", "texture"], required=True)
        p.add_argument("--query", help="Substring or exact name to search")
        p.add_argument("--exact", action="store_true", help="Require exact name/file match")
        p.add_argument("--category", help="Filter by exact category name, for example '10. Items'")
        p.add_argument("--subcategory", help="Filter by exact subcategory name")
        p.add_argument("--refresh", action="store_true", help="Refresh the cached index before searching")
        p.add_argument("--first", action="store_true", help="Take only the first match")
        p.add_argument("--limit", type=int, help="Take only the first N matches")
        if include_output_dir:
            p.add_argument(
                "--output-dir",
                default=str(OUTPUT_DIR),
                help=f"Base output directory, default: {OUTPUT_DIR}",
            )

    search = subparsers.add_parser("search", help="Search the local or freshly fetched index")
    add_query_flags(search)
    search.add_argument("--json", action="store_true", help="Print JSON instead of a readable list")
    search.set_defaults(func=cmd_search)

    urls = subparsers.add_parser("urls", help="Print direct download URLs for matched records")
    add_query_flags(urls)
    urls.set_defaults(func=cmd_urls)

    export = subparsers.add_parser("export", help="Export matched records to JSON or CSV")
    add_query_flags(export)
    export.add_argument("--format", choices=["json", "csv"], default="json")
    export.add_argument("--output", required=True, help="Output file path")
    export.set_defaults(func=cmd_export)

    download = subparsers.add_parser("download", help="Download matched records")
    add_query_flags(download, include_output_dir=True)
    download.add_argument("--all", action="store_true", help="Allow downloading all matched records")
    download.set_defaults(func=cmd_download)

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    ensure_dirs()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
