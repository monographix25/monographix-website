# -*- coding: utf-8 -*-
"""Desktop-Verknuepfung auf die Live-Seite (GitHub Pages)."""
import os
import subprocess
from pathlib import Path

URL = "https://danielgloeckler.github.io/monographix-website/"

DESKTOP = Path(os.popen(
    "powershell -NoProfile -Command \"[Environment]::GetFolderPath('Desktop')\""
).read().strip())

# alte lokale Verknuepfung entfernen
old = DESKTOP / "Monographix Website.lnk"
if old.exists():
    old.unlink()
    print("alte lokale Verknuepfung entfernt")

target = DESKTOP / "Monographix Website.url"
target.write_text(
    "[InternetShortcut]\r\n"
    f"URL={URL}\r\n"
    "IconIndex=0\r\n"
    "IconFile=%SystemRoot%\\System32\\imageres.dll\r\n",
    encoding="utf-8",
)
print("erstellt:", target)
subprocess.run(["powershell", "-NoProfile", "-Command",
                f"$s=(New-Object -ComObject WScript.Shell).CreateShortcut('{target}'); $s.IconLocation='%SystemRoot%\\System32\\imageres.dll,68'; $s.Save()"],
               check=False)
print("URL:", URL)
