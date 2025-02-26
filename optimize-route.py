from flask import Flask, jsonify, request
import requests
import polyline

app = Flask(__name__)

# API Keys (Replace with real keys)
GOOGLE_MAPS_API_KEY = "AIzaSyBDIBv5G7hhvHHGi3fb4bjGja3xuPRFjWw"
ORS_API_KEY = "5b3ce3597851110001cf6248f47f6898e78544358cfb813db8708c91"

# OpenRouteService vehicle types
ORS_VEHICLE_TYPES = {
    "car": "driving-car",
    "bike": "cycling-regular",
    "truck": "driving-hgv",
    "ev": "driving-car"
}

@app.route("/optimize-route", methods=["POST"])
def optimize_route():
    """Handles AI-powered route optimization."""
    data = request.json
    locations = data.get("locations", [])
    vehicle_type = data.get("vehicle_type", "car")
    optimize_for = data.get("optimize_for", "time")
    avoid_tolls = data.get("avoid_tolls", False)
    avoid_highways = data.get("avoid_highways", False)
    
    if len(locations) < 2:
        return jsonify({"error": "At least two locations are required for route optimization."})

    optimized_route = get_google_route(locations, vehicle_type, optimize_for, avoid_tolls, avoid_highways)
    
    return jsonify({"optimized_route": optimized_route})

def get_google_route(locations, vehicle_type, optimize_for, avoid_tolls, avoid_highways):
    """Fetches an optimized route from Google Maps API with AI enhancements."""
    base_url = "https://maps.googleapis.com/maps/api/directions/json"
    
    waypoints = "|".join(locations[1:-1]) if len(locations) > 2 else ""
    params = {
        "origin": locations[0],
        "destination": locations[-1],
        "waypoints": f"optimize:true|{waypoints}" if waypoints else "",
        "mode": "driving" if vehicle_type in ["car", "truck", "ev"] else "bicycling",
        "traffic_model": "best_guess",
        "departure_time": "now",
        "avoid": "|".join(filter(None, ["tolls" if avoid_tolls else "", "highways" if avoid_highways else ""])),
        "key": GOOGLE_MAPS_API_KEY
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if "routes" in data and data["routes"]:
        polyline_data = data["routes"][0]["overview_polyline"]["points"]
        return [{"polyline": polyline_data}]
    
    return [{"error": "No valid route found."}]

if __name__ == "__main__":
    app.run(debug=True)
