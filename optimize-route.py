import requests
import heapq
import polyline
from flask import Flask, jsonify, request

app = Flask(__name__)

# Google Maps API Key (Replace with your actual API key)
GOOGLE_MAPS_API_KEY = "AIzaSyBDIBv5G7hhvHHGi3fb4bjGja3xuPRFjWw"

# Dijkstra's Algorithm for shortest path
def dijkstra(graph, start, end):
    queue = [(0, start)]
    distances = {start: 0}
    predecessors = {}

    while queue:
        (cost, node) = heapq.heappop(queue)

        if node == end:
            path = []
            while node in predecessors:
                path.insert(0, node)
                node = predecessors[node]
            return path

        for neighbor, weight in graph.get(node, {}).items():
            new_cost = cost + weight
            if neighbor not in distances or new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                heapq.heappush(queue, (new_cost, neighbor))
                predecessors[neighbor] = node

    return []

# Get real-time traffic data
def get_real_time_traffic(origin, destination):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={AIzaSyBDIBv5G7hhvHHGi3fb4bjGja3xuPRFjWw}&traffic_model=best_guess&departure_time=now"
    response = requests.get(url)
    data = response.json()
    if data["status"] == "OK":
        return data["routes"][0]["legs"][0]
    return None

# Optimize multi-stop route using AI
@app.route("/optimize-route", methods=["POST"])
def optimize_route_api():
    locations = request.json.get("locations", [])
    vehicle_type = request.json.get("vehicle_type", "car")

    if len(locations) < 2:
        return jsonify({"error": "At least two locations required"})

    optimized_routes = []
    for i in range(len(locations) - 1):
        traffic_data = get_real_time_traffic(locations[i], locations[i + 1])
        if traffic_data:
            optimized_routes.append({
                "start": locations[i],
                "end": locations[i + 1],
                "distance": traffic_data["distance"]["text"],
                "duration": traffic_data["duration_in_traffic"]["text"],
                "polyline": traffic_data["steps"],
                "vehicle_type": vehicle_type
            })

    return jsonify({"optimized_route": optimized_routes})

if __name__ == "__main__":
    app.run(debug=True)
