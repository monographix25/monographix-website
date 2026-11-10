# -*- coding: utf-8 -*-
"""Desktop-Verknuepfung auf die Live-Seite (GitHub Pages, Account monographix25)."""
import os
from pathlib import Path

URL = "https://monographix25.github.io/monographix-website/"

DESKTOP = Path(os.popen(
    "powershell -NoProfile -Command \"[Environment]::GetFolderPath('Desktop')\""
).read().strip())

target = DESKTOP / "Monographix Website.url"
target.write_text(
    "[InternetShortcut]\r\n"
    f"URL={URL}\r\n"
    "IconIndex=0\r\n"
    "IconFile=%SystemRoot%\\System32\\imageres.dll\r\n",
    encoding="utf-8",
)
print("aktualisiert:", target)
print("URL:", URL)
