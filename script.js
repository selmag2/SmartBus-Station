async function updateDisplay() {
  try {
    const response = await fetch("http://localhost:5000/station_data");
    const stationData = await response.json();
    const busList = document.getElementById("bus-list");
    busList.innerHTML = "";

    // Trouver le bus avec l'ETA minimale
    let minEta = Infinity;
    stationData.buses.forEach(bus => {
      if (bus.eta_minutes < minEta) {
        minEta = bus.eta_minutes;
      }
    });

   stationData.buses.forEach(bus => {
  const etaClass = bus.eta_minutes === minEta && minEta <= 3 ? "arriving-soon" : "";
  const row = document.createElement("tr");

  row.innerHTML = `
    <td>${bus.bus_id}</td>
    <td>${bus.route}</td>
    <td class="${etaClass}">${bus.eta_minutes !== null ? bus.eta_minutes + " min" : "Indisponible"}</td>
    <td>${bus.passengers}</td>
    <td>${bus.statut || "Inconnu"}</td> <!-- ajout ici -->
  `;

  busList.appendChild(row);
});


    document.querySelector("h1").textContent = stationData.station_name + " - Bus en Approche";
  } catch (err) {
    console.error("Erreur lors du fetch:", err);
  }
}

function updateClock() {
  const now = new Date().toLocaleTimeString("fr-FR", {
    timeZone: "Africa/Casablanca",
    hour12: false
  });
  document.getElementById("clock").textContent = now;
}

setInterval(updateDisplay, 10000);
setInterval(updateClock, 1000);

updateDisplay();
updateClock();
