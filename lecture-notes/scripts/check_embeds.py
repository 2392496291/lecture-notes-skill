"""Check that every Obsidian embed resolves and that no attached image is orphaned.

Usage: python3 -I check_embeds.py <vault_root> [assets_dirname]

`assets_dirname` defaults to `附件`; every file under a directory with that
name is treated as a note attachment and reported if no note embeds it.

Checks:
  1. every ![[...]] target exists somewhere in the vault (Obsidian resolves
     embeds by basename across the whole vault, so we do too)
  2. no attachment file is left unused
  3. embeds with no width/alt are listed for review

Note on tables: Obsidian requires the pipe in `![[img.png\\|520]]` to be
escaped inside a table cell, so the raw text contains a backslash. That
backslash is stripped here — otherwise every in-table embed looks broken.
"""
import os
import re
import sys

EMBED_RE = re.compile(r"!\[\[([^\]|]+?)(?:\\?\|[^\]]*)?\]\]")


def main(vault, assets_dirname="附件"):
    vault = os.path.abspath(vault)
    if not os.path.isdir(vault):
        sys.exit(f"not a directory: {vault}")

    note_files = []
    all_basenames = set()
    assets = {}
    for root, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if d not in {".git", ".obsidian", ".trash"}]
        for name in files:
            full = os.path.join(root, name)
            all_basenames.add(name)
            if name.endswith(".md"):
                note_files.append(full)
            if os.path.basename(root) == assets_dirname:
                assets[name] = full

    used = set()
    broken = []
    no_width = []
    embed_count = 0
    for note in note_files:
        with open(note, encoding="utf-8", errors="replace") as f:
            text = f.read()
        for m in EMBED_RE.finditer(text):
            target = m.group(1).strip()
            embed_count += 1
            used.add(target)
            if target not in all_basenames:
                broken.append((os.path.relpath(note, vault), target))
            elif "|" not in m.group(0):
                no_width.append((os.path.relpath(note, vault), target))

    orphaned = sorted(set(assets) - used)

    print(f"notes scanned : {len(note_files)}")
    print(f"embeds found  : {embed_count}")
    print(f"attachments   : {len(assets)}")
    print(f"missing files : {len(broken)}")
    for note, target in broken:
        print(f"    MISSING  {target}   <- {note}")
    print(f"unused attach : {len(orphaned)}")
    for name in orphaned:
        print(f"    ORPHAN   {name}")
    if no_width:
        print(f"no width set  : {len(no_width)} (cosmetic; Obsidian shows full size)")
        for note, target in no_width:
            print(f"    NO-WIDTH {target}   <- {note}")

    return 1 if (broken or orphaned) else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(main(*sys.argv[1:]))
