import leafmap.kepler as leafmap
import geopandas as gpd
import requests
import polyline
import pandas as pd
from shapely.geometry import LineString

# API Endpoint for Route Optimization (Change if hosted elsewhere)
API_URL = "navvista.netlify.app/optimize-route"

# User-Defined Route Preferences
vehicle_type = "car"  # Options: "car", "bike", "truck", "ev"
optimize_for = "fuel"  # Options: "fuel", "time", "distance", "traffic"

# Example Locations (Replace with dynamic user input if needed)
locations = [
    "51.52738771088042,-0.15355043538426116",
    "51.50723029796882,-0.1734286299198402"
]

# Request AI-Optimized Route
response = requests.post(API_URL, json={
    "locations": locations,
    "vehicle_type": vehicle_type,
    "optimize_for": optimize_for
})

data = response.json()

if "optimized_route" in data:
    optimized_routes = data["optimized_route"]
    decoded_routes = []

    # Decode polyline for each optimized segment
    for route in optimized_routes:
        encoded_polyline = route["polyline"]
        decoded_polyline = polyline.decode(encoded_polyline)
        decoded_polyline = [t[::-1] for t in decoded_polyline]
        decoded_routes.append(LineString(decoded_polyline))

    # Convert to GeoSeries for visualization
    route_geometry = gpd.GeoSeries(decoded_routes, crs="EPSG:4326")

    # Initialize Leafmap for visualization
    m = leafmap.Map(center=[51.52738771088042, -0.15355043538426116], zoom=12, height=1000, widescreen=False)
    m.add_gdf(route_geometry, f"AI-Optimized {vehicle_type.capitalize()} Route ({optimize_for.capitalize()})")
    m

    print(f"Optimized {vehicle_type} route ({optimize_for}) displayed on the map.")
else:
    print("Error fetching optimized route:", data)
