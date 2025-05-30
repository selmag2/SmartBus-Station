from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
import json

app = Flask(__name__, static_folder="static")
CORS(app)

DATA_FILE = "buses_data.json"
last_displayed_etas = {}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f).get("buses", [])
    return []

@app.route("/station_data", methods=["GET"])
def station_data():
    buses = load_data()
    sorted_buses = sorted(buses, key=lambda b: (b["eta_minutes"] if b["eta_minutes"] is not None else 999))

    display_buses = []
    backup_buses = []

    for bus in sorted_buses:
        bus_id = bus["bus_id"]
        new_eta = bus["eta_minutes"]
        last_eta = last_displayed_etas.get(bus_id)

        if last_eta is None or (new_eta is not None and abs(new_eta - last_eta) >= 1):
            last_displayed_etas[bus_id] = new_eta
            display_buses.append(bus)
        else:
            backup_buses.append(bus)

        if len(display_buses) >= 4:
            break

    if len(display_buses) < 4:
        for b in backup_buses:
            display_buses.append(b)
            if len(display_buses) >= 4:
                break

    return jsonify({
        "station_id": "ST123",
        "station_name": "Madinat Al Irfane",
        "buses": display_buses
    })


@app.route("/")
def index():
    return send_from_directory("static", "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
