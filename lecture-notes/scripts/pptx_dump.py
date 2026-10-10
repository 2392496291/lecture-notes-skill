"""Dump the text of every slide (plus speaker notes) of a .pptx, and the media inventory.

Usage: python3 -I pptx_dump.py <file.pptx> <out.txt>

Speaker notes matter: in some decks the lecturer's remarks carry facts that
never make it onto the slide, and they're easy to lose if you only read the
rendered slides.

The MEDIA section at the end lists every file under ppt/media/ with its size —
compare it against `pptx_media.py`'s per-slide mapping to spot leftover
resources that no slide references.
"""
import xml.etree.ElementTree as ET
import zipfile
import sys

A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


def para_text(p):
    """Text of one <a:p>, joining runs; render a:br as a soft break."""
    out = []
    for node in p.iter():
        if node.tag == A + "t" and node.text:
            out.append(node.text)
        elif node.tag == A + "br":
            out.append(" / ")
    return "".join(out).strip()


def slide_text(xml_bytes):
    root = ET.fromstring(xml_bytes)
    lines = []
    for p in root.iter(A + "p"):
        t = para_text(p)
        if t:
            lines.append(t)
    return lines


def media_of(z):
    return sorted((n, z.getinfo(n).file_size) for n in z.namelist()
                  if n.startswith("ppt/media/"))


def main(src, out):
    z = zipfile.ZipFile(src)
    names = set(z.namelist())

    pres = ET.fromstring(z.read("ppt/presentation.xml"))
    rels = ET.fromstring(z.read("ppt/_rels/presentation.xml.rels"))
    rid2target = {r.get("Id"): r.get("Target") for r in rels}
    order = []
    for sld in pres.iter(P + "sldId"):
        tgt = rid2target.get(sld.get(R + "id"), "").lstrip("/")
        if not tgt.startswith("ppt/"):
            tgt = "ppt/" + tgt
        order.append(tgt)

    lines = [f"FILE: {src}", f"SLIDES: {len(order)}", ""]
    for i, path in enumerate(order, 1):
        lines.append(f"=== SLIDE {i} ({path}) ===")
        if path in names:
            lines.extend(slide_text(z.read(path)))
        else:
            lines.append("(missing)")
        relpath = path.replace("slides/", "slides/_rels/") + ".rels"
        if relpath in names:
            for r in ET.fromstring(z.read(relpath)):
                if r.get("Type", "").endswith("/notesSlide"):
                    nt = "ppt/" + r.get("Target").replace("../", "")
                    if nt in names:
                        body = [t for t in slide_text(z.read(nt)) if not t.isdigit()]
                        if body:
                            lines.append("--- 备注 ---")
                            lines.extend(body)
        lines.append("")

    lines.append("=== MEDIA ===")
    for n, sz in media_of(z):
        lines.append(f"{n}\t{sz}")

    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"{out}\tslides={len(order)}\tmedia={len(media_of(z))}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
