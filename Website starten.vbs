' Monographix Website lokal starten
' Startet einen kleinen Webserver (unsichtbar) und oeffnet die Seite im Browser.
' Wird ueber die Desktop-Verknuepfung "Monographix Website" aufgerufen.

Option Explicit

Dim fso, sh, base, py, cmd
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh = CreateObject("WScript.Shell")

base = fso.GetParentFolderName(WScript.ScriptFullName)
sh.CurrentDirectory = base

py = base & "\..\.venv\Scripts\python.exe"
If Not fso.FileExists(py) Then
  py = "python.exe"
End If

cmd = """" & py & """ -m http.server 8123 --directory """ & base & """"
sh.Run cmd, 0, False

WScript.Sleep 900
sh.Run "http://localhost:8123/"
