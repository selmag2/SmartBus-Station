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

app.py # Serveur Flask (API + serveur de fichiers statiques)
buses_data.json # Données simulées des bus (à jour régulièrement)
static/
│ └── index.html # Interface web affichant les bus
└── README.md # Documentation du projet
#Architecture Logicielle
#Architecture matérielle
#Résultats, Démonstration
