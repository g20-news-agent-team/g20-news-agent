"""Load normalized G20 JSONL into the corpus database."""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit
from uuid import uuid7

import psycopg

REPO = Path(__file__).resolve().parents[1]
SAMPLE_SOURCE_IDS = {"外交部": "g20-01", "新华网": "g20-06"}
CONTENT_KINDS = {"full_text", "summary"}

UPSERT_SOURCE = """
    INSERT INTO sources (id, name, kind, entry_url)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (id) DO UPDATE
    SET name = EXCLUDED.name, kind = EXCLUDED.kind, entry_url = EXCLUDED.entry_url
    WHERE (sources.name, sources.kind, sources.entry_url)
        IS DISTINCT FROM (EXCLUDED.name, EXCLUDED.kind, EXCLUDED.entry_url)
"""

UPSERT_DOCUMENT = """
    INSERT INTO documents (
        id, source_id, canonical_url, original_url, title, content_text, content_kind,
        published_at, fetched_at, publisher, author, source_label, section, suggested_type
    ) VALUES (
        %(id)s, %(source_id)s, %(canonical_url)s, %(original_url)s, %(title)s,
        %(content_text)s, %(content_kind)s, %(published_at)s, %(fetched_at)s,
        %(publisher)s, %(author)s, %(source_label)s, %(section)s, %(suggested_type)s
    )
    ON CONFLICT (source_id, canonical_url) DO UPDATE
    SET content_text = EXCLUDED.content_text,
        content_kind = EXCLUDED.content_kind,
        original_url = EXCLUDED.original_url,
        published_at = COALESCE(documents.published_at, EXCLUDED.published_at),
        fetched_at = COALESCE(EXCLUDED.fetched_at, documents.fetched_at),
        publisher = COALESCE(documents.publisher, EXCLUDED.publisher),
        author = COALESCE(documents.author, EXCLUDED.author),
        source_label = COALESCE(documents.source_label, EXCLUDED.source_label),
        section = COALESCE(documents.section, EXCLUDED.section)
    WHERE documents.content_kind = 'summary' AND EXCLUDED.content_kind = 'full_text'
"""


def nonempty_text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip() or "\x00" in value:
        raise ValueError(f"{field} must be nonempty text")
    return value


def optional_text(value: object, field: str) -> str | None:
    if value is None or value == "":
        return None
    return nonempty_text(value, field)


def http_url(value: object, field: str) -> str:
    text = nonempty_text(value, field)
    parts = urlsplit(text)
    if parts.scheme not in {"http", "https"} or not parts.hostname or parts.username is not None:
        raise ValueError(f"{field} must be an HTTP(S) URL without credentials")
    return text


def timestamp(value: object, field: str) -> datetime | None:
    text = optional_text(value, field)
    if text is None:
        return None
    result = datetime.fromisoformat(text)
    if result.utcoffset() is None:
        raise ValueError(f"{field} must include a time zone")
    return result


def read_sources(path: Path) -> tuple[list[tuple[str, str, str, str]], dict[str, str]]:
    catalog = json.loads(path.read_text(encoding="utf-8-sig"))["sources"]
    rows = []
    source_ids = set()
    lookup = {}
    for source in catalog:
        identity = nonempty_text(source["id"], "source id")
        name = nonempty_text(source["name"], "source name")
        kind = nonempty_text(source["kind"], "source kind")
        config = source["config"]
        entry_url = http_url(config.get("feedUrl") or config.get("url"), "source entry URL")
        if identity in source_ids or name in lookup or identity in lookup:
            raise ValueError(f"Repeated source id or name: {identity}")
        rows.append((identity, name, kind, entry_url))
        source_ids.add(identity)
        lookup[identity] = identity
        lookup[name] = identity
    for alias, identity in SAMPLE_SOURCE_IDS.items():
        if identity in source_ids:
            lookup.setdefault(alias, identity)
    return rows, lookup


def read_document(record: dict, source_lookup: dict[str, str]) -> dict:
    if not isinstance(record, dict):
        raise ValueError("each JSONL row must be an object")
    source = nonempty_text(record.get("sourceId") or record.get("source"), "sourceId or source")
    if source not in source_lookup:
        raise ValueError(f"unknown source: {source}")

    canonical = http_url(record.get("canonicalUrl") or record.get("url"), "canonicalUrl or url")
    content_kind = nonempty_text(record.get("contentKind"), "contentKind")
    if content_kind not in CONTENT_KINDS:
        raise ValueError("contentKind must be full_text or summary")

    return {
        "id": uuid7(),
        "source_id": source_lookup[source],
        "canonical_url": canonical,
        "original_url": http_url(record.get("originalUrl") or record.get("url") or canonical, "originalUrl"),
        "title": nonempty_text(record.get("title"), "title"),
        "content_text": nonempty_text(record.get("text"), "text"),
        "content_kind": content_kind,
        "published_at": timestamp(record.get("publishedAt"), "publishedAt"),
        "fetched_at": timestamp(record.get("fetchedAt"), "fetchedAt"),
        "publisher": optional_text(record.get("publisher"), "publisher"),
        "author": optional_text(record.get("author"), "author"),
        "source_label": optional_text(record.get("sourceLabel"), "sourceLabel"),
        "section": optional_text(record.get("section"), "section"),
        "suggested_type": optional_text(record.get("type"), "type"),
    }


def read_documents(path: Path, source_lookup: dict[str, str]) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8-sig") as file:
        for line_number, line in enumerate(file, 1):
            if line.strip():
                try:
                    rows.append(read_document(json.loads(line), source_lookup))
                except ValueError as error:
                    raise ValueError(f"{path}:{line_number}: {error}") from error
    if not rows:
        raise ValueError(f"{path} has no documents")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path, default=REPO / "fixtures/documents.sample.jsonl")
    parser.add_argument("--sources", type=Path, default=REPO / "vendor/g20-sources.json")
    args = parser.parse_args()

    dsn = os.environ.get("G20_DATABASE_URL")
    if not dsn:
        parser.error("set G20_DATABASE_URL to the G20 corpus database")

    try:
        sources, source_lookup = read_sources(args.sources)
        documents = read_documents(args.input, source_lookup)
    except (OSError, KeyError, TypeError, ValueError) as error:
        parser.error(str(error))

    with psycopg.connect(dsn) as connection, connection.cursor() as cursor:
        cursor.executemany(UPSERT_SOURCE, sources)
        cursor.executemany(UPSERT_DOCUMENT, documents)
        affected = cursor.rowcount
    print(f"读取 {len(documents)} 条资料，新增或补全 {affected} 条。")


if __name__ == "__main__":
    main()
