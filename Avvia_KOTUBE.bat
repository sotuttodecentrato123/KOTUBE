@echo off
cd /d "%~dp0"
rem Ferma un'eventuale istanza vecchia, cosi' parte sempre il codice aggiornato
powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "%~dp0ferma_kotube.ps1"
start "" "%~dp0.venv\Scripts\pythonw.exe" "%~dp0avvia_kotube.py"