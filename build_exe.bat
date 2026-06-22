@echo off
setlocal

REM --- Construction de l'exe en mode local (Windows) ---
REM 1) Installe PyInstaller si besoin
REM 2) Génère un exe sans console (arrière-plan)

python -m pip install --upgrade pip
python -m pip install pyinstaller

REM --onefile : un seul .exe
REM --noconsole : pas de fenêtre console
REM --add-data : inclut l'HTML dans l'exe
REM Utilise "python -m PyInstaller" pour éviter les soucis de PATH
python -m PyInstaller --onefile --noconsole --name IPScanne --add-data "interface_gestion_ip.html;." server.py

echo.
echo Exe genere dans le dossier "dist" : IPScanne.exe
echo Lance-le puis ouvre http://127.0.0.1:5000
pause
