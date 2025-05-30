# === IMPORTS DE MODULES ===
import json          # Pour écrire et lire des fichiers au format JSON
import time          # Pour introduire des pauses dans la boucle (simulation en temps réel)
import random        # Pour ajouter du réalisme avec des variations aléatoires
import math          # Pour les calculs mathématiques (haversine)

# === CONSTANTES ===
DATA_FILE = "buses_data.json"      # Fichier où les données visibles seront écrites
STATION_LAT = 33.987               # Latitude de la station de bus
STATION_LON = -6.870               # Longitude de la station de bus

# === CALCUL DE DISTANCE GÉOGRAPHIQUE (FORMULE DE HAVERSINE) ===
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Rayon de la Terre en kilomètres
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    # Formule de haversine pour calculer la distance entre deux points GPS
    a = math.sin(d_lat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Distance en kilomètres

# === CALCUL DU TEMPS D'ARRIVÉE ESTIMÉ (ETA) EN MINUTES ===
def estimate_eta(distance_km, speed_kmh):
    if speed_kmh == 0:
        return 999  # Si le bus est arrêté, retour d'un ETA fictif très élevé
    return round((distance_km / speed_kmh) * 60)  # ETA en minutes

# === CRÉATION INITIALE DES 10 BUS ===
buses = []
for i in range(10):
    buses.append({
        "bus_id": f"BUS{i+1:03}",                          # Identifiant du bus (BUS001, BUS002, etc.)
        "route": f"L{random.randint(1, 50)}",              # Ligne du bus (L1 à L50)
        "lat": 33.975 + random.uniform(0.001, 0.01),       # Latitude de départ aléatoire
        "lon": -6.890 + random.uniform(0.001, 0.02),       # Longitude de départ aléatoire
        "speed_kmh": random.uniform(15, 30),               # Vitesse initiale en km/h
        "eta_minutes": None,                               # Temps d'arrivée estimé (à calculer)
        "stuck_counter": 0,                                # Compteur pour détecter une panne (bus bloqué)
        "statut": "En route",                              # Statut initial
        "arrival_counter": 0                               # Temps écoulé après arrivée (pour rester affiché)
    })

# === DÉPLACEMENT DU BUS EN DIRECTION DE LA STATION ===
def move_towards_station(lat, lon, target_lat, target_lon, speed_kmh, time_seconds=5):
    speed_kmps = speed_kmh / 3600  # Conversion de la vitesse en km/s
    distance_to_move = speed_kmps * time_seconds  # Distance à parcourir en 5 secondes
    distance = haversine(lat, lon, target_lat, target_lon)
    if distance == 0:
        return lat, lon  # Déjà à la station
    frac = min(distance_to_move / distance, 1)  # Fraction de distance à parcourir
    new_lat = lat + (target_lat - lat) * frac
    new_lon = lon + (target_lon - lon) * frac
    return new_lat, new_lon

# === SIMULATION PRINCIPALE ===
def simulate():
    while True:
        etas = []  # Liste des bus visibles avec ETA valides

        for bus in buses:
            dist = haversine(bus["lat"], bus["lon"], STATION_LAT, STATION_LON)

            if bus["statut"] != "Arrivé":
                # Légère variation aléatoire de la vitesse
                speed_variation = random.uniform(-0.05, 0.05)
                bus["speed_kmh"] = max(5, min(40, bus["speed_kmh"] * (1 + speed_variation)))

                # Déplacement vers la station
                bus["lat"], bus["lon"] = move_towards_station(
                    bus["lat"], bus["lon"], STATION_LAT, STATION_LON, bus["speed_kmh"]
                )

                # Calcul de l'ETA avec un peu de bruit aléatoire
                eta = estimate_eta(dist, bus["speed_kmh"]) + random.choice([-2, -1, 0, 1, 2])
                eta = max(0, min(30, eta))  # Limite ETA entre 0 et 30
                bus["eta_minutes"] = eta

                # Si ETA reste élevé plusieurs fois, on considère le bus en panne
                if eta > 10:
                    bus["stuck_counter"] += 1
                else:
                    bus["stuck_counter"] = 0

                if bus["stuck_counter"] >= 3:
                    bus["statut"] = "En panne"
                    bus["speed_kmh"] = 0
                    bus["eta_minutes"] = None
                elif eta == 0:
                    bus["statut"] = "Arrivé"
                    bus["arrival_counter"] = 1
                else:
                    bus["statut"] = "En route"
                    bus["arrival_counter"] = 0

            elif bus["statut"] == "Arrivé":
                # Bus reste affiché pendant 5 secondes après son arrivée
                bus["arrival_counter"] += 1
                if bus["arrival_counter"] > 1 and bus["arrival_counter"] <= 5:
                    bus["eta_minutes"] = 0
                else:
                    bus["eta_minutes"] = None  # Supprimé de l'affichage ensuite

            # Sélectionne les bus à afficher (ETA connu + en route ou arrivé)
            if bus["statut"] in ["En route", "Arrivé"] and bus["eta_minutes"] is not None:
                etas.append((bus["eta_minutes"], bus))

        # Séparation des bus arrivés et non arrivés
        arrived_buses = [b for eta, b in etas if b["statut"] == "Arrivé"]
        other_buses = [b for eta, b in etas if b["statut"] != "Arrivé"]

        # Tri par ETA croissant
        arrived_buses.sort(key=lambda b: b["eta_minutes"])
        other_buses.sort(key=lambda b: b["eta_minutes"])

        # Sélection de 4 bus à afficher (priorité aux arrivés)
        selected_buses = arrived_buses[:4]
        if len(selected_buses) < 4:
            selected_buses += other_buses[:4 - len(selected_buses)]

        # Création des données visibles
        visible_buses = []
        for bus in selected_buses:
            visible_buses.append({
                "bus_id": bus["bus_id"],
                "route": bus["route"],
                "latitude": round(bus["lat"], 6),
                "longitude": round(bus["lon"], 6),
                "eta_minutes": bus["eta_minutes"],
                "passengers": random.randint(10, 40),  # Simulation du nombre de passagers
                "statut": bus["statut"]
            })

        # Enregistrement dans le fichier de données
        with open(DATA_FILE, "w") as f:
            json.dump({"buses": visible_buses}, f, indent=2)

        print(f"[INFO] Station mise à jour avec {len(visible_buses)} bus affichés.")

        # Pause de 5 secondes avant la prochaine mise à jour
        time.sleep(5)

        # Sauvegarde de l’état complet (debug)
        with open("all_buses_debug.json", "w") as f:
            json.dump({"buses": buses}, f, indent=2)

# === POINT D'ENTRÉE DU SCRIPT ===
if __name__ == "__main__":
    simulate()
