"""Map slides -> embedded images and extract the ones you want.

Usage:
    python3 -I pptx_media.py <file.pptx> -                      # print the mapping only
    python3 -I pptx_media.py <file.pptx> <outdir>               # extract every slide image
    python3 -I pptx_media.py <file.pptx> <outdir> 8,10,11       # extract only these slides

Reads the zip in memory and writes only the requested images, named
`s<NN>_<original>.png` so the slide number stays visible in the filename.

Only images actually referenced by a slide's relationships are reported.
Files that sit in ppt/media/ but are referenced by no slide are template
backgrounds or leftovers — they are deliberately excluded. (Check them
with `pptx_dump.py`'s MEDIA section before assuming they're unimportant.)
"""
import os
import posixpath
import sys
import xml.etree.ElementTree as ET
import zipfile

P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


def slide_order(z):
    pres = ET.fromstring(z.read("ppt/presentation.xml"))
    rels = ET.fromstring(z.read("ppt/_rels/presentation.xml.rels"))
    rid2target = {r.get("Id"): r.get("Target") for r in rels}
    order = []
    for sld in pres.iter(P + "sldId"):
        t = rid2target.get(sld.get(R + "id"), "").lstrip("/")
        if not t.startswith("ppt/"):
            t = "ppt/" + t
        order.append(t)
    return order


def _rels_path(slidepath):
    return slidepath.replace("slides/", "slides/_rels/") + ".rels"


def images_of(z, slidepath):
    relpath = _rels_path(slidepath)
    if relpath not in z.namelist():
        return []
    out = []
    for r in ET.fromstring(z.read(relpath)):
        if r.get("Type", "").endswith("/image"):
            t = posixpath.normpath(posixpath.join("ppt/slides", r.get("Target")))
            out.append((r.get("Id"), t))
    return out


def audio_video(z, slidepath):
    relpath = _rels_path(slidepath)
    if relpath not in z.namelist():
        return []
    out = []
    for r in ET.fromstring(z.read(relpath)):
        ty = r.get("Type", "")
        if ty.endswith(("/media", "/video", "/audio")):
            t = posixpath.normpath(posixpath.join("ppt/slides", r.get("Target")))
            out.append((ty.rsplit("/", 1)[-1], t))
    return out


def main():
    src = sys.argv[1]
    z = zipfile.ZipFile(src)
    order = slide_order(z)
    if len(sys.argv) > 2 and sys.argv[2] != "-":
        outdir = sys.argv[2]
        want = set(int(x) for x in sys.argv[3].split(",")) if len(sys.argv) > 3 else None
        os.makedirs(outdir, exist_ok=True)
    else:
        outdir, want = None, None

    for i, path in enumerate(order, 1):
        imgs = images_of(z, path)
        av = audio_video(z, path)
        desc = " ".join(f"{os.path.basename(t)}[{z.getinfo(t).file_size}]" for _, t in imgs)
        extra = " ".join(f"{k}:{os.path.basename(t)}" for k, t in av)
        print(f"slide {i}\t{desc}{' ' + extra if extra else ''}")
        if outdir and (want is None or i in want):
            for _, t in imgs:
                out = os.path.join(outdir, f"s{i:02d}_{os.path.basename(t)}")
                with open(out, "wb") as f:
                    f.write(z.read(t))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main()
