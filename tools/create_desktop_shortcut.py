# -*- coding: utf-8 -*-
"""Legt/aktualisiert die Desktop-Verknuepfung zur Website (ueber den lokalen Server)."""
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAUNCHER = ROOT / "Website starten.vbs"

DESKTOP = Path(os.popen(
    "powershell -NoProfile -Command \"[Environment]::GetFolderPath('Desktop')\""
).read().strip())
if not DESKTOP.exists():
    DESKTOP = Path(os.path.expanduser("~")) / "Desktop"

LINK = DESKTOP / "Monographix Website.lnk"

ps = f'''
$ws = New-Object -ComObject WScript.Shell
$sc = $ws.CreateShortcut("{LINK}")
$sc.TargetPath = "C:\\Windows\\System32\\wscript.exe"
$sc.Arguments = '"{LAUNCHER}"'
$sc.WorkingDirectory = "{ROOT}"
$sc.IconLocation = "%SystemRoot%\\System32\\imageres.dll,68"
$sc.Description = "Website Monographix - Atelier fuer Kreativitaet"
$sc.WindowStyle = 7
$sc.Save()
'''

subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)
print(f"Verknuepfung: {LINK}")
print(f"Startet:      {LAUNCHER} (lokaler Server + Browser)")
