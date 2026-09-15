@echo off
title LIGHT STREAM SWITCH APP
cd /d "%~dp0"
".\.venv\Scripts\python.exe" app_launcher.py %*
pause
