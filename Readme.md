# Gestion des IP 

Interface web + backend Python pour vérifier l’état (ping ICMP) d’une liste d’IP/hostnames toutes les 30 secondes.

## Fonctionnalités

- Ajout / suppression d’IP ou de noms d’hôte
- Ping ICMP côté serveur (plus fiable qu’un simple fetch navigateur)
- Rafraîchissement automatique toutes les 30 secondes
- Stockage local côté navigateur (localStorage)

## Prérequis

- Windows
- Python 3.10+ installé

## Installation

1. Ouvre un terminal dans ce dossier.
2. Installe les dépendances :
   - `pip install -r requirements.txt`

## Lancer le serveur

- Exécute : `python server.py`
- Ouvre ensuite : `http://127.0.0.1:5000`

## Générer un .exe (Windows, local)

1. Exécute le script `build_exe.bat`.
2. L’exécutable sera créé dans le dossier `dist` sous le nom `IPScanne.exe`.
3. Lance `IPScanne.exe` : le serveur tourne en arrière-plan (pas de console).
4. Ouvre : `http://127.0.0.1:5000`

## Arrêter le serveur depuis la barre des tâches

- Utilise le fichier `Stop_Server.bat`.
- Tu peux créer un raccourci et l’épingler à la barre des tâches pour arrêter le serveur en un clic.

## Icône dans la barre des tâches + démarrage auto

- Une petite fenêtre se lance automatiquement et reste dans la barre des tâches.
- Le serveur se ferme quand tu cliques sur “Quitter”.
- Un fichier de démarrage automatique est créé dans le dossier Startup Windows.

## Fichiers principaux

- `server.py` : backend Flask + API `/api/ping`
- `interface_gestion_ip.html` : interface web
- `requirements.txt` : dépendances Python

## Notes

- Le backend utilise la commande Windows `ping`.
- Les IP/hostnames ajoutés sont sauvegardés dans le navigateur (localStorage).

## Modifier le comportement

- Intervalle de ping : dans `interface_gestion_ip.html`, variable `PING_INTERVAL_MS`.
- Timeout ping : dans `server.py` (commande `ping` et timeout Python).
