@echo off
REM Arrête le serveur local via l'API (utilisable en raccourci/épinglé dans la barre des tâches)

powershell -NoProfile -ExecutionPolicy Bypass -Command "try { Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/api/shutdown | Out-Null } catch { }"
exit /b 0
