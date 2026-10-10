"""Dump the text layer of a PDF, page by page.

Usage: python3 -I pdf_extract_text.py <src.pdf> <out.txt>

Use it to find which pages have NO text layer — those are usually
full-page screenshots (past-exam pages, scanned handouts) and are the
highest-value pages to render as images later.
"""
import os
import site
import sys


def _import_pypdf():
    try:
        from pypdf import PdfReader  # noqa: F401
        return PdfReader
    except ImportError:
        pass
    # `python3 -I` disables the user site dir, so put it back explicitly.
    for p in {site.getusersitepackages(), *getattr(site, "getsitepackages", lambda: [])()}:
        if p and os.path.isdir(p) and p not in sys.path:
            sys.path.append(p)
    try:
        from pypdf import PdfReader  # noqa: F811
        return PdfReader
    except ImportError:
        sys.exit("pypdf not found. Install it with:  pip3 install --user pypdf")


def main(src, out):
    reader = _import_pypdf()(src)
    lines = [f"FILE: {src}", f"PAGES: {len(reader.pages)}", ""]
    empty = []
    for i, page in enumerate(reader.pages, 1):
        text = (page.extract_text() or "").strip()
        if not text:
            empty.append(i)
        lines.append(f"=== PAGE {i} ===")
        lines.append(text)
        lines.append("")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"{out}  {len(reader.pages)} pages")
    if empty:
        print("no text layer (likely full-page images):", ", ".join(map(str, empty)))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
