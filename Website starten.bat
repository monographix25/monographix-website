@echo off
title Monographix Website
cd /d "%~dp0kunststudio"

set "PY=..\.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"

echo Starte lokalen Server auf http://localhost:8123 ...
start "" http://localhost:8123/

"%PY%" -m http.server 8123
pause
