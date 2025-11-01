#!/usr/bin/env python3
"""
Cleanup and Dedupe Tool for the Punk Zines Database

Actions:
1) Identify and optionally remove non‑zine entries using heuristic rules
2) Detect duplicates via:
   - Exact IA identifier (ia_metadata.identifier)
   - Exact archive_source URL (normalized)
   - Title+issue+year normalized key
   - Local image hash (sha1) when image_url points into ./images

Keeps the "best" record by source preference and metadata completeness:
  internet_archive > iiif > flickr > other_archive

Usage:
  python tools/cleanup_and_dedupe.py --analyze
  python tools/cleanup_and_dedupe.py --clean --yes
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "punk_zines_database.json"
BACKUPS = ROOT / "backups"
BACKUPS.mkdir(exist_ok=True)


def load_db() -> Dict:
    return json.loads(DB_PATH.read_text())


def save_db(db: Dict) -> None:
    DB_PATH.write_text(json.dumps(db, indent=2, ensure_ascii=False))


def backup_db() -> Path:
    p = BACKUPS / f"punk_zines_database_cleanup_{os.getpid()}.json"
    shutil.copy2(DB_PATH, p)
    return p


SRC_RANK = {
    "internet_archive": 4,
    "iiif": 3,
    "flickr": 2,
    "other_archive": 1,
    None: 0,
}

KNOWN_GOOD_SERIES = [
    # Major series and well-known titles
    "maximum rocknroll", "punk planet", "cometbus", "slug & lettuce", "slug and lettuce",
    "forced exposure", "touch and go", "flipside", "search & destroy", "sniffin' glue",
    "chainsaw", "ripped & torn", "kill your pet puppy", "jamming", "el zine",
    "heartattack", "we got power", "profane existence", "no mag", "damage",
]

POSITIVE_TOKENS = {
    "zine", "fanzine", "punk", "riot grrrl", "queercore", "hardcore", "diy",
    "issue", "no.", "numero", "nummer", "núm", "nº", "n°",
}

NEGATIVE_TOKENS = {
    # content types that are rarely zines
    "flyer", "poster", "postcard", "ticket", "press release", "program",
    "newspaper", "microfilm", "microfiche", "map", "drawing", "blueprint",
    "minutes", "meeting", "newsletter archive", "course", "syllabus", "capstone",
    "yearbook", "brochure", "directory", "newspaperissue", "music event",
}


def norm_text(s: Optional[str]) -> str:
    return (s or "").strip().lower()


def is_probable_zine(z: Dict) -> bool:
    name = norm_text(z.get("zine_name"))
    desc = norm_text(z.get("description"))
    # Intentionally ignore generic tags like 'zine' that we add by default
    text = " ".join([name, desc])
    # Series allowlist
    if any(series in name for series in KNOWN_GOOD_SERIES):
        return True
    # Strong positives
    if any(tok in text for tok in POSITIVE_TOKENS):
        return True
    # Strong negatives
    if any(tok in text for tok in NEGATIVE_TOKENS):
        return False
    # Heuristic: presence of typical zine fields
    if z.get("issue_number") or re.search(r"\bissue\b|\bno\.?\b", name):
        return True
    # Otherwise unknown
    return False


def url_key(u: Optional[str]) -> Optional[str]:
    if not u or not isinstance(u, str):
        return None
    # strip query/fragment
    m = re.match(r"^(https?://[^?#]+)", u)
    return m.group(1) if m else u


def title_issue_year_key(z: Dict) -> Optional[str]:
    name = norm_text(z.get("zine_name"))
    if not name:
        return None
    # remove generic words
    n = re.sub(r"[^a-z0-9\s]", "", name)
    n = re.sub(r"\b(issue|no|number|vol|volume)\b", "", n)
    n = re.sub(r"\s+", " ", n).strip()
    issue = norm_text(z.get("issue_number"))
    year = norm_text(z.get("year"))
    return f"{n}|{issue}|{year}"


def image_sha1(path: Path) -> Optional[str]:
    if not path.exists() or not path.is_file():
        return None
    h = hashlib.sha1()
    try:
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None


def pick_better(a: Dict, b: Dict) -> Dict:
    # Compare by source type rank
    ra = SRC_RANK.get(a.get("source_type")) or 0
    rb = SRC_RANK.get(b.get("source_type")) or 0
    if ra != rb:
        return a if ra > rb else b
    # Prefer one with IA link present
    ia_a = 1 if a.get("ia_item_url") else 0
    ia_b = 1 if b.get("ia_item_url") else 0
    if ia_a != ia_b:
        return a if ia_a > ia_b else b
    # Prefer filled year
    ya = 1 if a.get("year") else 0
    yb = 1 if b.get("year") else 0
    if ya != yb:
        return a if ya > yb else b
    # Prefer local image path
    la = 1 if str(a.get("image_url", "")).startswith("images/") else 0
    lb = 1 if str(b.get("image_url", "")).startswith("images/") else 0
    if la != lb:
        return a if la > lb else b
    # Fallback: keep first
    return a


def analyze(db: Dict):
    zines = db.get("zines", [])
    # Non‑zine detection
    nonz = []
    keep = []
    for z in zines:
        if is_probable_zine(z):
            keep.append(z)
        else:
            nonz.append(z)

    # Dedupe detection on the kept set
    by_ia = defaultdict(list)
    by_url = defaultdict(list)
    by_tiy = defaultdict(list)
    by_hash = defaultdict(list)

    for z in keep:
        meta = z.get("ia_metadata") or {}
        iid = meta.get("identifier") if isinstance(meta, dict) else None
        if iid:
            by_ia[iid].append(z)
        uk = url_key(z.get("archive_source"))
        if uk:
            by_url[uk].append(z)
        tk = title_issue_year_key(z)
        if tk:
            by_tiy[tk].append(z)
        iu = z.get("image_url")
        if isinstance(iu, str) and iu.startswith("images/"):
            h = image_sha1(ROOT / iu)
            if h:
                by_hash[h].append(z)

    def multi(d):
        return {k: v for k, v in d.items() if len(v) > 1}

    return {
        "total": len(zines),
        "kept": len(keep),
        "nonz": len(nonz),
        "dupe_ia": sum(len(v) - 1 for v in multi(by_ia).values()),
        "dupe_url": sum(len(v) - 1 for v in multi(by_url).values()),
        "dupe_tiy": sum(len(v) - 1 for v in multi(by_tiy).values()),
        "dupe_hash": sum(len(v) - 1 for v in multi(by_hash).values()),
    }


def clean_and_dedupe(db: Dict) -> Tuple[int, int]:
    zines = db.get("zines", [])
    # Step 1: filter probable zines
    removed_non = [z for z in zines if not is_probable_zine(z)]
    keep = [z for z in zines if is_probable_zine(z)]
    removed_nonz = len(removed_non)

    # Step 2: dedupe
    def index_multi(groups: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        return {k: v for k, v in groups.items() if len(v) > 1}

    groups = {
        "ia": defaultdict(list),
        "url": defaultdict(list),
        "tiy": defaultdict(list),
        "hash": defaultdict(list),
    }

    for z in keep:
        meta = z.get("ia_metadata") or {}
        iid = meta.get("identifier") if isinstance(meta, dict) else None
        if iid:
            groups["ia"][iid].append(z)
        uk = url_key(z.get("archive_source"))
        if uk:
            groups["url"][uk].append(z)
        tk = title_issue_year_key(z)
        if tk:
            groups["tiy"][tk].append(z)
        iu = z.get("image_url")
        if isinstance(iu, str) and iu.startswith("images/"):
            h = image_sha1(ROOT / iu)
            if h:
                groups["hash"][h].append(z)

    # Resolve duplicates with preference rules
    to_keep_ids = set()
    to_drop_ids = set()
    dropped_dupes_list: List[Dict] = []

    def resolve_group(items: List[Dict]):
        best = items[0]
        for it in items[1:]:
            best = pick_better(best, it)
        for it in items:
            (to_keep_ids if it is best else to_drop_ids).add(id(it))
            if it is not best:
                dropped_dupes_list.append(it)

    for g in [index_multi(groups["ia"]), index_multi(groups["url"]), index_multi(groups["tiy"]), index_multi(groups["hash"])]:
        for items in g.values():
            resolve_group(items)

    # Mark everything else as keep if not explicitly dropped
    for z in keep:
        if id(z) not in to_drop_ids:
            to_keep_ids.add(id(z))

    cleaned = [z for z in keep if id(z) in to_keep_ids]
    removed_dupes = len(keep) - len(cleaned)

    db["zines"] = cleaned
    # Update metadata
    if "database_info" in db:
        db["database_info"]["total_entries"] = len(cleaned)
    # write log
    log = {
        "removed_non_zines": removed_non,
        "removed_duplicates": dropped_dupes_list,
    }
    log_path = BACKUPS / f"cleanup_dedupe_removed_{os.getpid()}.json"
    log_path.write_text(json.dumps(log, indent=2, ensure_ascii=False))
    return removed_nonz, removed_dupes


def main():
    ap = argparse.ArgumentParser(description="Cleanup and dedupe the zines database")
    ap.add_argument("--analyze", action="store_true")
    ap.add_argument("--clean", action="store_true")
    ap.add_argument("--yes", action="store_true", help="Skip confirmation when cleaning")
    args = ap.parse_args()

    db = load_db()
    stats = analyze(db)
    print("\n=== ANALYSIS ===")
    for k, v in stats.items():
        print(f"{k:>12}: {v}")

    if args.analyze and not args.clean:
        return

    if not args.yes:
        resp = input("Proceed with cleanup and dedupe? (yes/no): ").strip().lower()
        if resp not in {"y", "yes"}:
            print("Cancelled.")
            return

    b = backup_db()
    print(f"Backup saved: {b}")
    removed_nonz, removed_dupes = clean_and_dedupe(db)
    save_db(db)
    print("\n=== CLEANUP COMPLETE ===")
    print(f"Removed non‑zines: {removed_nonz}")
    print(f"Removed duplicates: {removed_dupes}")
    print(f"Remaining entries: {len(db.get('zines', []))}")


if __name__ == "__main__":
    main()
