# -*- coding: utf-8 -*-
"""Kleiner Qualitätscheck: interne Links, Anker, Tag-Balance, Alt-Texte."""
import pathlib
import re
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}


class Balance(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []
        self.ids = set()
        self.imgs_without_alt = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if "id" in d:
            self.ids.add(d["id"])
        if tag == "img" and not d.get("alt"):
            self.imgs_without_alt.append(d.get("src", "?"))
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"Schließendes </{tag}> ohne öffnendes Element (Zeile {self.getpos()[0]})")
            return
        if self.stack[-1][0] != tag:
            self.errors.append(
                f"</{tag}> in Zeile {self.getpos()[0]} erwartet </{self.stack[-1][0]}> (geöffnet Zeile {self.stack[-1][1]})"
            )
            # versuche zu reparieren
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    del self.stack[i:]
                    return
        else:
            self.stack.pop()


def main():
    pages = sorted(ROOT.glob("*.html"))
    anchors = {}
    parsers = {}
    for p in pages:
        html = p.read_text(encoding="utf-8")
        bp = Balance()
        bp.feed(html)
        bp.close()
        parsers[p.name] = bp
        anchors[p.name] = bp.ids
        problems = list(bp.errors)
        if bp.stack:
            problems.append("Nicht geschlossen: " + ", ".join(f"<{t}> (Zeile {l})" for t, l in bp.stack))
        if problems:
            print(f"\n[STRUKTUR] {p.name}")
            for prob in problems[:6]:
                print("   -", prob)

    print("\n[LINKS]")
    link_re = re.compile(r'(?:href|src)="([^"]+)"')
    missing = 0
    for p in pages:
        html = p.read_text(encoding="utf-8")
        for ref in set(link_re.findall(html)):
            if ref.startswith(("http://", "https://", "mailto:", "tel:", "data:", "#")):
                if ref.startswith("#") and ref[1:] and ref[1:] not in anchors.get(p.name, set()):
                    print(f"   {p.name}: Anker {ref} fehlt")
                    missing += 1
                continue
            target, _, frag = ref.partition("#")
            path = (ROOT / target).resolve()
            if not path.exists():
                print(f"   {p.name}: fehlende Datei {ref}")
                missing += 1
            elif frag and path.suffix == ".html":
                if frag not in anchors.get(path.name, set()):
                    print(f"   {p.name}: Anker {frag} fehlt in {path.name}")
                    missing += 1
    print("   " + ("alles ok" if missing == 0 else f"{missing} Problem(e)"))

    print("\n[BILDER ohne alt]")
    empty = {n: b.imgs_without_alt for n, b in parsers.items() if b.imgs_without_alt}
    # dekorative Bilder mit alt="" sind Absicht, geprueft wird nur fehlendes Attribut
    print("   " + ("keine" if not empty else str(empty)))


if __name__ == "__main__":
    main()
