#!/usr/bin/env python3
"""
Remove specific entries from punk_zines_database.json by ID or pattern.

Input can be provided via:
- --ids: comma-separated list of IDs, e.g., --ids SG003,MRR432
- --file: a text file with one rule per line. Supported rule formats:
    id=SG003
    url~archive.qzap.org/index.php/Detail/Object/Show/object_id/400
    name~Not A Zine Title

Dry run:
  python tools/remove_entries.py --file removals.txt --dry-run

Execute:
  python tools/remove_entries.py --file removals.txt --yes
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "punk_zines_database.json"
BACKUPS = ROOT / "backups"
BACKUPS.mkdir(exist_ok=True)


def load_db() -> Dict:
    return json.loads(DB_PATH.read_text())


def save_db(db: Dict) -> None:
    DB_PATH.write_text(json.dumps(db, indent=2, ensure_ascii=False))


def backup_db() -> Path:
    p = BACKUPS / f"punk_zines_database_removed_{os.getpid()}.json"
    shutil.copy2(DB_PATH, p)
    return p


def parse_rules(text: str) -> List[Tuple[str, str]]:
    rules = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('id='):
            rules.append(('id', line[3:].strip()))
        elif line.startswith('url~'):
            rules.append(('url', line[4:].strip()))
        elif line.startswith('name~'):
            rules.append(('name', line[5:].strip()))
        else:
            # heuristic: looks like URL? treat as url~
            if '://' in line or '/' in line:
                rules.append(('url', line))
            else:
                rules.append(('id', line))
    return rules


def apply_rules(db: Dict, rules: List[Tuple[str, str]], dry_run: bool) -> int:
    zines = db.get('zines', [])
    keep = []
    removed = []
    for z in zines:
        kill = False
        for kind, val in rules:
            if kind == 'id' and str(z.get('id')) == val:
                kill = True
                break
            if kind == 'url' and val in str(z.get('archive_source')):
                kill = True
                break
            if kind == 'name' and val.lower() in str(z.get('zine_name','')).lower():
                kill = True
                break
        (removed if kill else keep).append(z)

    if dry_run:
        print(f"Would remove {len(removed)} entries (keeping {len(keep)}).")
        for z in removed[:20]:
            print(f"  - {z.get('id')} | {z.get('zine_name')} | {z.get('archive_source')}")
        return len(removed)

    db['zines'] = keep
    if 'database_info' in db:
        db['database_info']['total_entries'] = len(keep)
    save_db(db)
    # log
    log = BACKUPS / f"removed_manual_{os.getpid()}.json"
    log.write_text(json.dumps(removed, indent=2, ensure_ascii=False))
    print(f"Removed {len(removed)} entries. Log: {log}")
    return len(removed)


def main():
    ap = argparse.ArgumentParser(description='Remove entries by ID or pattern')
    ap.add_argument('--ids', help='Comma-separated list of IDs to remove')
    ap.add_argument('--file', help='File with removal rules (id=, url~, name~)')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--yes', action='store_true', help='Skip confirmation')
    args = ap.parse_args()

    if not args.ids and not args.file:
        ap.error('Provide --ids or --file')

    rules: List[Tuple[str,str]] = []
    if args.ids:
        for i in args.ids.split(','):
            rules.append(('id', i.strip()))
    if args.file:
        p = Path(args.file)
        if not p.exists():
            raise SystemExit(f'File not found: {p}')
        rules += parse_rules(p.read_text())

    db = load_db()
    to_remove = apply_rules(db.copy(), rules, dry_run=True)
    if args.dry_run:
        return
    if not args.yes:
        c = input(f'Proceed to remove {to_remove} entries? (yes/no): ').strip().lower()
        if c not in {'y','yes'}:
            print('Cancelled.')
            return
    b = backup_db()
    print(f'Backup saved: {b}')
    apply_rules(db, rules, dry_run=False)


if __name__ == '__main__':
    main()

