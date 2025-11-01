#!/usr/bin/env python3
"""
IIIF Harvester for Institutional Archives (Pratt, Barnard, etc.)

Ingests IIIF Presentation API manifests (v2 or v3) and adds one database
entry per manifest, using the first canvas as the cover image.

Usage examples:

  # Single manifest
  python tools/iiif_harvester.py --manifest "https://example.org/iiif/manifest.json" --download

  # Text file with one manifest URL per line
  python tools/iiif_harvester.py --file iiif_seeds.txt --download

  # IIIF Collection (recursively gather manifests, up to --max-items)
  python tools/iiif_harvester.py --collection "https://example.org/iiif/collection.json" \
    --max-items 200 --download

Notes:
- --download saves a thumbnail/preview locally (images/iiif/) so the
  viewer works offline. Without it, entries will use the remote IIIF URL.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import requests

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "punk_zines_database.json"
IMG_DIR = ROOT / "images" / "iiif"


def load_db() -> Dict:
    if DB_PATH.exists():
        return json.loads(DB_PATH.read_text())
    return {"database_info": {}, "zines": []}


def save_db(db: Dict) -> None:
    info = db.setdefault("database_info", {})
    info["last_updated"] = time.strftime("%Y-%m-%d")
    info["total_entries"] = len(db.get("zines", []))
    DB_PATH.write_text(json.dumps(db, indent=2, ensure_ascii=False))


def generate_id(existing_ids: set, title: str) -> str:
    title = re.sub(r"[^A-Za-z0-9\s]", "", title or "Zine")
    words = [w for w in title.split() if w]
    if not words:
        prefix = "ZN"
    elif len(words) == 1:
        prefix = words[0][:3].upper()
    else:
        prefix = (words[0][0] + (words[1][0] if len(words) > 1 else "")).upper()
        if len(words) > 2:
            prefix += words[2][0].upper()
    prefix = re.sub(r"[^A-Z]", "", prefix)[:3] or "ZN"
    i = 1
    while f"{prefix}{i:03d}" in existing_ids:
        i += 1
    new_id = f"{prefix}{i:03d}"
    existing_ids.add(new_id)
    return new_id


def fetch_json(url: str) -> dict:
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=25)
    r.raise_for_status()
    return r.json()


def as_str_label(label) -> str:
    # v3: label is a language map object; v2: string
    if isinstance(label, str):
        return label
    if isinstance(label, dict):
        for k in ("en", "none"):
            v = label.get(k)
            if isinstance(v, list) and v:
                return str(v[0])
            if isinstance(v, str):
                return v
        # Fallback to first value
        for v in label.values():
            if isinstance(v, list) and v:
                return str(v[0])
            if isinstance(v, str):
                return v
    return "Untitled Zine"


def extract_homepage(man: dict) -> Optional[str]:
    hp = man.get("homepage")
    if isinstance(hp, list) and hp:
        item = hp[0]
        if isinstance(item, dict) and item.get("id"):
            return item["id"]
    if isinstance(hp, dict) and hp.get("id"):
        return hp["id"]
    return None


def extract_rights(man: dict) -> Optional[str]:
    return man.get("rights") or man.get("license")


def extract_summary(man: dict) -> str:
    s = man.get("summary")
    if isinstance(s, dict):
        return as_str_label(s)
    if isinstance(s, str):
        return s
    # v2 fallback
    if man.get("description"):
        d = man["description"]
        if isinstance(d, str):
            return d
        if isinstance(d, list):
            try:
                return "; ".join([str(x) for x in d if x])
            except Exception:
                pass
    # metadata fallback
    meta = man.get("metadata")
    if isinstance(meta, list):
        pairs = []
        for m in meta[:6]:
            label = as_str_label(m.get("label")) if isinstance(m, dict) else ""
            value = as_str_label(m.get("value")) if isinstance(m, dict) else ""
            if label or value:
                pairs.append(f"{label}: {value}".strip())
        return "; ".join(pairs)
    return "Imported via IIIF manifest"


def extract_year(man: dict) -> Optional[str]:
    # Try common metadata fields
    meta = man.get("metadata")
    if isinstance(meta, list):
        for m in meta:
            if not isinstance(m, dict):
                continue
            lab = as_str_label(m.get("label"))
            if lab and lab.lower() in {"date", "year", "issued", "published"}:
                val = as_str_label(m.get("value"))
                if val:
                    mobj = re.search(r"(19\d{2}|20\d{2})", val)
                    if mobj:
                        return mobj.group(1)
    # Try label string
    lab = as_str_label(man.get("label"))
    mobj = re.search(r"(19\d{2}|20\d{2})", lab)
    if mobj:
        return mobj.group(1)
    return None


def iiif_image_from_canvas_v3(canvas: dict) -> Optional[str]:
    try:
        ap = canvas["items"][0]  # AnnotationPage
        ann = ap["items"][0]     # Annotation
        body = ann.get("body")
        if isinstance(body, list) and body:
            body = body[0]
        if isinstance(body, dict):
            # Direct image id
            if body.get("id"):
                return body["id"]
            # Image service
            svc = body.get("service") or body.get("services")
            if isinstance(svc, list) and svc:
                svc = svc[0]
            if isinstance(svc, dict) and svc.get("id"):
                sid = svc["id"].rstrip("/")
                if sid.endswith("/info.json"):
                    sid = sid[:-10]
                return f"{sid}/full/600,/0/default.jpg"
    except Exception:
        return None
    return None


def iiif_image_from_manifest_v3(man: dict) -> Optional[str]:
    # Prefer explicit thumbnail first
    tn = man.get("thumbnail")
    if isinstance(tn, list) and tn:
        t = tn[0]
        if isinstance(t, dict) and t.get("id"):
            return t["id"]
        if isinstance(t, str):
            return t
    if isinstance(tn, dict) and tn.get("id"):
        return tn["id"]
    # Cover from first canvas
    items = man.get("items")
    if isinstance(items, list) and items:
        return iiif_image_from_canvas_v3(items[0])
    return None


def iiif_image_from_manifest_v2(man: dict) -> Optional[str]:
    # v2 thumbnail
    if isinstance(man.get("thumbnail"), str):
        return man["thumbnail"]
    if isinstance(man.get("thumbnail"), dict) and man["thumbnail"].get("@id"):
        return man["thumbnail"]["@id"]
    try:
        seqs = man.get("sequences") or []
        canv = seqs[0]["canvases"][0]
        imgs = canv.get("images") or []
        res = imgs[0].get("resource") or {}
        # Direct resource id
        if isinstance(res, dict) and res.get("@id"):
            return res["@id"]
        # Image service
        svc = res.get("service")
        if isinstance(svc, dict) and svc.get("@id"):
            sid = svc["@id"].rstrip("/")
            if sid.endswith("/info.json"):
                sid = sid[:-10]
            return f"{sid}/full/600,/0/default.jpg"
    except Exception:
        return None
    return None


def resolve_manifest_image(man: dict) -> Optional[str]:
    ctx = man.get("@context") or man.get("context")
    # v3 has "type": "Manifest"; v2 has "@type": "sc:Manifest"
    if man.get("type") == "Manifest" or (isinstance(ctx, str) and "/presentation/3" in ctx):
        return iiif_image_from_manifest_v3(man)
    return iiif_image_from_manifest_v2(man)


def pick_archive_source(man: dict, manifest_url: str) -> str:
    return extract_homepage(man) or manifest_url


def upsert_manifest(db: Dict, manifest_url: str, download: bool) -> int:
    try:
        man = fetch_json(manifest_url)
    except Exception as e:
        print(f"  ✗ Failed to fetch manifest: {e}")
        return 0

    label = as_str_label(man.get("label"))
    desc = extract_summary(man)
    year = extract_year(man)
    img_url = resolve_manifest_image(man)
    archive_source = pick_archive_source(man, manifest_url)
    rights = extract_rights(man)

    if not img_url:
        print("  ✗ No cover image found; skipping")
        return 0

    existing_srcs = {str(z.get("archive_source")) for z in db.get("zines", [])}
    if archive_source in existing_srcs:
        print("  → Already present; skipping")
        return 0

    IMG_DIR.mkdir(parents=True, exist_ok=True)
    local_path = None
    if download:
        try:
            rr = requests.get(img_url, timeout=25)
            if rr.status_code == 200:
                fname = re.sub(r"[^A-Za-z0-9_-]", "", (label or "zine"))[:40]
                out = IMG_DIR / f"{fname or 'iiif'}_{int(time.time())}.jpg"
                out.write_bytes(rr.content)
                local_path = str(out)
        except Exception:
            local_path = None

    existing_ids = {z["id"] for z in db.get("zines", [])}
    zid = generate_id(existing_ids, label)

    entry = {
        "id": zid,
        "zine_name": label,
        "issue_number": None,
        "year": year,
        "location": None,
        "image_url": local_path or img_url,
        "archive_source": archive_source,
        "description": desc,
        "tags": ["punk", "zine"],
        "bands_featured": [],
        "circulation": None,
        "creators": None,
        "source_type": "iiif",
        "attribution": "Imported via IIIF manifest",
        "license": rights,
    }

    db.setdefault("zines", []).append(entry)
    save_db(db)
    print(f"  ✓ Added: {label}")
    return 1


def iter_collection_manifests(coll_url: str, max_items: int) -> Iterable[str]:
    try:
        coll = fetch_json(coll_url)
    except Exception as e:
        print(f"✗ Failed to fetch collection: {e}")
        return []
    yielded = 0
    # v3: type: Collection, manifests under items; v2: @type: sc:Collection, manifests under 'manifests'
    items = []
    if isinstance(coll.get("items"), list):
        items = coll["items"]
    elif isinstance(coll.get("manifests"), list):
        items = coll["manifests"]
    for it in items:
        if yielded >= max_items:
            break
        if isinstance(it, dict):
            # v3: id; v2: @id
            murl = it.get("id") or it.get("@id")
            if isinstance(murl, str):
                yielded += 1
                yield murl


def main():
    ap = argparse.ArgumentParser(description="IIIF Harvester (manifests and collections)")
    ap.add_argument("--manifest", help="Single IIIF manifest URL")
    ap.add_argument("--file", help="Text file with one manifest URL per line")
    ap.add_argument("--collection", help="IIIF Collection URL (will gather manifests)")
    ap.add_argument("--max-items", type=int, default=200, help="Max manifests from a collection")
    ap.add_argument("--download", action="store_true", help="Download image locally for offline viewer")
    args = ap.parse_args()

    if not any([args.manifest, args.file, args.collection]):
        ap.error("Provide --manifest or --file or --collection")

    db = load_db()
    total = 0

    if args.manifest:
        total += upsert_manifest(db, args.manifest, args.download)

    if args.file:
        p = Path(args.file)
        if not p.exists():
            raise SystemExit(f"File not found: {p}")
        for line in p.read_text().splitlines():
            url = line.strip()
            if not url or url.startswith("#"):
                continue
            total += upsert_manifest(db, url, args.download)

    if args.collection:
        for murl in iter_collection_manifests(args.collection, args.max_items):
            total += upsert_manifest(db, murl, args.download)

    print(f"\nDone. Added {total} item(s).")


if __name__ == "__main__":
    main()

