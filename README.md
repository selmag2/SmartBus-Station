# SmartBus-Station
# 🚌 Simulation intelligente d’un panneau d’arrivée de bus

Ce projet simule un panneau d’affichage dynamique pour une station de bus, affichant en temps réel les estimations d’arrivée des prochains bus à partir d’un fichier de données JSON.

---

## 📌 Objectifs

- Simuler un affichage de station de bus intelligent.
- Afficher dynamiquement les bus dont l’ETA change significativement.
- Limiter l’affichage à 4 bus maximum, avec une logique de mise à jour optimisée.
- Fournir une API REST simple pour alimenter une interface web.

---

## 📁 Structure du projet

SmartBus-Station/
├── backend/
│   ├── server.py
│   └── simulator.py
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── data/
│   ├── all_buses_debug.json
│   └── buses_data.json
└── README.md



---

## 🐍 Scripts Python du projet

### `server.py` – Serveur Flask (API + Web)
Ce script est le **cœur du backend**. Il :

- Lance un serveur web avec Flask.
- Sert le fichier `index.html` en tant que page d’accueil.
- Expose une route `/station_data` pour fournir les données des bus au format JSON.
- Trie et filtre les bus selon leur ETA (`eta_minutes`).
- Affiche jusqu’à 4 bus dont l’ETA a changé d’au moins 1 minute.

### `simulator.py` – Générateur de données de bus
Ce script **simule dynamiquement des données** d’arrivée de bus :

- Génére des bus avec identifiants (`bus_id`), lignes (`line`) et ETA.
- Écrit les données dans `buses_data.json` (consommées par `server.py`).
- Peut être exécuté en boucle ou en arrière-plan pour simuler un flux temps réel.

---

## 🚀 Lancement du projet

### 📦 Prérequis
- Python 3.7 ou plus
- `pip install flask flask-cors`

### ▶️ Exécution du backend

```bash
cd backend
python server.py


Fonctionnalités typiques :

Génère des bus avec identifiants (bus_id), lignes (line) et ETA.

Écrit les données dans buses_data.json (consommées par server.py).

Peut être exécuté en arrière-plan pour simuler un flux de données.

## Objectif 
L'objectif est de modéliser un système proche de la réalité, alliant interface utilisateur intuitive, communication en temps réel et traitement intelligent des données, dans le but de démontrer les capacités d’un système embarqué de nouvelle génération dédié à l'information des voyageurs.

###🔌 API REST
GET /station_data
Retourne les données des bus à afficher (jusqu’à 4 max).

### 🖥️ Visualisation des données (interface web) 
Ouvre un navigateur web et accède à l’adresse :

http://localhost:5000
📊 Description de l’interface
Affiche un panneau d’arrivée pour la station Madinat Al Irfane.

Liste jusqu’à 4 bus avec leur numéro de ligne et leur temps estimé d’arrivée (ETA) en minutes.

Les données sont mises à jour automatiquement toutes les quelques secondes via des requêtes vers l’API /station_data.

Seuls les bus dont l’ETA a changé significativement sont rafraîchis, afin d’éviter un affichage instable
