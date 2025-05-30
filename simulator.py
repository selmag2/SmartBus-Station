import json
import time
import random
import math

DATA_FILE = "buses_data.json"
STATION_LAT = 33.987
STATION_LON = -6.870

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def estimate_eta(distance_km, speed_kmh):
    if speed_kmh == 0:
        return 999
    return round((distance_km / speed_kmh) * 60)

# Génère 10 bus
buses = []
for i in range(10):
    buses.append({
        "bus_id": f"BUS{i+1:03}",
        "route": f"L{random.randint(1, 50)}",
        "lat": 33.975 + random.uniform(0.001, 0.01),
        "lon": -6.890 + random.uniform(0.001, 0.02),
        "speed_kmh": random.uniform(15, 30),
        "eta_minutes": None,
        "stuck_counter": 0,
        "statut": "En route",
        "arrival_counter": 0  # Compteur pour gérer les 5 secondes après arrivée
    })

def move_towards_station(lat, lon, target_lat, target_lon, speed_kmh, time_seconds=5):
    speed_kmps = speed_kmh / 3600
    distance_to_move = speed_kmps * time_seconds
    distance = haversine(lat, lon, target_lat, target_lon)
    if distance == 0:
        return lat, lon
    frac = min(distance_to_move / distance, 1)
    new_lat = lat + (target_lat - lat) * frac
    new_lon = lon + (target_lon - lon) * frac
    return new_lat, new_lon

def simulate():
    while True:
        etas = []

        for bus in buses:
            dist = haversine(bus["lat"], bus["lon"], STATION_LAT, STATION_LON)

            if bus["statut"] != "Arrivé":
                speed_variation = random.uniform(-0.05, 0.05)
                bus["speed_kmh"] = max(5, min(40, bus["speed_kmh"] * (1 + speed_variation)))

                bus["lat"], bus["lon"] = move_towards_station(bus["lat"], bus["lon"], STATION_LAT, STATION_LON, bus["speed_kmh"])

                eta = estimate_eta(dist, bus["speed_kmh"]) + random.choice([-2, -1, 0, 1, 2])
                eta = max(0, min(30, eta))
                bus["eta_minutes"] = eta

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
                bus["arrival_counter"] += 1
                if bus["arrival_counter"] > 1 and bus["arrival_counter"] <= 5:
                    bus["eta_minutes"] = 0
                else:
                    bus["eta_minutes"] = None

            # On ne conserve que les bus qui ont un eta valide et statut "En route" ou "Arrivé"
            if bus["statut"] in ["En route", "Arrivé"] and bus["eta_minutes"] is not None:
                etas.append((bus["eta_minutes"], bus))

        # Séparer bus "Arrivé" et les autres
        arrived_buses = [b for eta, b in etas if b["statut"] == "Arrivé"]
        other_buses = [b for eta, b in etas if b["statut"] != "Arrivé"]

        # Trier les arrivés par eta (devrait tous être à 0)
        arrived_buses.sort(key=lambda b: b["eta_minutes"])
        # Trier les autres par eta croissant
        other_buses.sort(key=lambda b: b["eta_minutes"])

        # Prendre jusqu'à 4 bus en mettant d'abord les arrivés, puis compléter avec les autres
        selected_buses = arrived_buses[:4]
        if len(selected_buses) < 4:
            selected_buses += other_buses[:4 - len(selected_buses)]

        visible_buses = []
        for bus in selected_buses:
            visible_buses.append({
                "bus_id": bus["bus_id"],
                "route": bus["route"],
                "latitude": round(bus["lat"], 6),
                "longitude": round(bus["lon"], 6),
                "eta_minutes": bus["eta_minutes"],
                "passengers": random.randint(10, 40),
                "statut": bus["statut"]
            })

        with open(DATA_FILE, "w") as f:
            json.dump({"buses": visible_buses}, f, indent=2)

        print(f"[INFO] Station mise à jour avec {len(visible_buses)} bus affichés.")
        time.sleep(5)

        with open("all_buses_debug.json", "w") as f:
         json.dump({"buses": buses}, f, indent=2)


if __name__ == "__main__":
    simulate()
