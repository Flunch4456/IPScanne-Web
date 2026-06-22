from __future__ import annotations

# Serveur backend simple pour ping ICMP
# - Lance un serveur web local (Flask)
# - Sert l'interface HTML
# - Fournit une API /api/ping pour tester une IP/hostname

import os
import re
import subprocess
import threading
import time
import webbrowser
from pathlib import Path
import sys
import tkinter as tk

from flask import Flask, jsonify, request, send_from_directory
from werkzeug.serving import make_server

APP_DIR = Path(__file__).resolve().parent
HTML_FILE = "interface_gestion_ip.html"

# Motif simple pour sécuriser la cible (évite les commandes injectées)
SAFE_TARGET = re.compile(r"^[a-zA-Z0-9.\-:]+$")

app = Flask(__name__, static_folder=str(APP_DIR), static_url_path="")
http_server = None


@app.get("/")
def index():
    """Sert l'interface HTML principale."""
    return send_from_directory(APP_DIR, HTML_FILE)


@app.post("/api/ping")
def api_ping():
    """API JSON: {"target": "192.168.1.10"} -> {online, rtt_ms, error}"""
    payload = request.get_json(silent=True) or {}
    target = str(payload.get("target", "")).strip()

    # Validation basique de la cible
    if not target or not SAFE_TARGET.match(target):
        return jsonify({"online": False, "error": "Cible invalide"}), 400

    # Commande ping Windows :
    # -n 1   => 1 seule requête
    # -w 1000 => timeout 1000 ms
    cmd = ["ping", "-n", "1", "-w", "1000", target]

    start = time.perf_counter()
    try:
        # CREATE_NO_WINDOW évite l'ouverture d'une fenêtre CMD à chaque ping
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=2.5,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
    except subprocess.TimeoutExpired:
        return jsonify({"online": False, "error": "Timeout"})

    rtt_ms = int((time.perf_counter() - start) * 1000)
    online = result.returncode == 0

    return jsonify({"online": online, "rtt_ms": rtt_ms})


@app.post("/api/shutdown")
def api_shutdown():
    """Arrête proprement le serveur (appel local uniquement)."""
    if request.remote_addr not in {"127.0.0.1", "::1"}:
        return jsonify({"ok": False, "error": "Accès refusé"}), 403

    def shutdown():
        time.sleep(0.1)
        if http_server:
            http_server.shutdown()

    threading.Thread(target=shutdown, daemon=True).start()
    return jsonify({"ok": True})


def ensure_startup_entry():
    """Crée un lancement automatique au démarrage Windows (si absent)."""
    startup_dir = Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
    startup_dir.mkdir(parents=True, exist_ok=True)

    startup_file = startup_dir / "IPScanne.cmd"
    if startup_file.exists():
        return

    if getattr(sys, "frozen", False):
        # Cas .exe PyInstaller
        cmd = f'start "" "{sys.executable}"\n'
    else:
        # Cas script Python : utilise pythonw.exe si présent pour éviter la console
        pythonw = Path(sys.executable).with_name("pythonw.exe")
        python_exec = pythonw if pythonw.exists() else Path(sys.executable)
        cmd = f'start "" "{python_exec}" "{APP_DIR / "server.py"}"\n'

    startup_file.write_text(cmd, encoding="utf-8")


def run_server_in_thread():
    """Lance le serveur Flask en thread pour permettre un arrêt propre."""
    global http_server
    http_server = make_server("127.0.0.1", 5000, app)
    thread = threading.Thread(target=http_server.serve_forever, daemon=True)
    thread.start()

    def shutdown():
        if http_server:
            http_server.shutdown()
            http_server.server_close()

    return shutdown


def launch_taskbar_ui(shutdown_server):
    """Crée une petite fenêtre qui reste dans la barre des tâches.

    - Visible dans la barre des tâches (icône)
    - Se ferme proprement avec le bouton Quitter
    """
    root = tk.Tk()
    root.title("IPScanne")
    root.geometry("320x170")
    root.resizable(False, False)

    label = tk.Label(root, text="Serveur local actif\nhttp://127.0.0.1:5000", pady=12)
    label.pack()

    btn_open = tk.Button(root, text="Ouvrir l'interface", command=lambda: webbrowser.open("http://127.0.0.1:5000"))
    btn_open.pack(pady=6)

    def on_close():
        shutdown_server()
        root.destroy()

    btn_quit = tk.Button(root, text="Quitter", command=on_close)
    btn_quit.pack(pady=6)

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.after(200, root.iconify)  # Minimise automatiquement dans la barre des tâches
    root.mainloop()


if __name__ == "__main__":
    # Démarre le serveur local sur http://127.0.0.1:5000
    ensure_startup_entry()
    shutdown_server = run_server_in_thread()
    launch_taskbar_ui(shutdown_server)
