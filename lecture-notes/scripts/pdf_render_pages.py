"""Render selected PDF pages to JPEG, one page at a time.

Usage:
    python3 -I pdf_render_pages.py <src.pdf> <outdir> <page:name> [<page:name> ...]

Example:
    python3 -I pdf_render_pages.py slides.pdf ./附件 \
        4:第1讲-p04-边界值测试 12:第1讲-p12-贷款规格

Renders the whole page (not the embedded bitmaps) — for beamer-style
handouts the figures are vector art, and a page render also captures
content that only appears part-way through an animation.

Uses macOS `sips` if available, else `pdftoppm` (poppler).
"""
import os
import shutil
import site
import subprocess
import sys

TARGET_LONG_EDGE_PX = 1400
JPEG_QUALITY = 82


def _import_pypdf():
    try:
        from pypdf import PdfReader, PdfWriter  # noqa: F401
        return PdfReader, PdfWriter
    except ImportError:
        pass
    for p in {site.getusersitepackages(), *getattr(site, "getsitepackages", lambda: [])()}:
        if p and os.path.isdir(p) and p not in sys.path:
            sys.path.append(p)
    try:
        from pypdf import PdfReader, PdfWriter  # noqa: F811
        return PdfReader, PdfWriter
    except ImportError:
        sys.exit("pypdf not found. Install it with:  pip3 install --user pypdf")


def _dpi_for(page):
    """Pick a DPI that lands the long edge near TARGET_LONG_EDGE_PX."""
    box = page.mediabox
    long_edge_pt = max(float(box.width), float(box.height))
    if long_edge_pt <= 0:
        return 150
    return max(72, round(TARGET_LONG_EDGE_PX / long_edge_pt * 72))


def _render(one_pdf, out_jpg, page):
    sips = shutil.which("sips")
    if sips:
        subprocess.run(
            [sips, "-s", "format", "jpeg", "-s", "formatOptions", str(JPEG_QUALITY),
             "-Z", str(TARGET_LONG_EDGE_PX), one_pdf, "--out", out_jpg],
            check=True, capture_output=True,
        )
        return
    pdftoppm = shutil.which("pdftoppm")
    if pdftoppm:
        prefix = out_jpg[:-len(".jpg")]
        subprocess.run(
            [pdftoppm, "-jpeg", "-singlefile", "-r", str(_dpi_for(page)),
             "-jpegopt", f"quality={JPEG_QUALITY}", one_pdf, prefix],
            check=True, capture_output=True,
        )
        return
    sys.exit("No renderer found. Install poppler (`brew install poppler`) "
             "or run this on macOS, where `sips` is built in.")


def main(src, outdir, pairs):
    PdfReader, PdfWriter = _import_pypdf()
    os.makedirs(outdir, exist_ok=True)
    reader = PdfReader(src)
    total = 0
    for pno, name in pairs:
        page = reader.pages[pno - 1]
        writer = PdfWriter()
        writer.add_page(page)
        one = os.path.join(outdir, f"_tmp_{pno:03d}.pdf")
        jpg = os.path.join(outdir, f"{name}.jpg")
        with open(one, "wb") as f:
            writer.write(f)
        try:
            _render(one, jpg, page)
        finally:
            os.remove(one)
        size = os.path.getsize(jpg)
        total += size
        print(f"{pno:>4}  {size // 1024:>5} KB  {os.path.basename(jpg)}")
    print(f"--- {len(pairs)} page(s), {total // 1024} KB total")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    parsed = []
    for arg in sys.argv[3:]:
        if ":" not in arg:
            sys.exit(f"bad argument {arg!r}: expected <page>:<name>")
        pno, name = arg.split(":", 1)
        parsed.append((int(pno), name))
    main(sys.argv[1], sys.argv[2], parsed)
