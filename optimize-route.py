from flask import app, jsonify, request
@app.route("/optimize-route", methods=["POST"])
def optimize_route():
    locations = request.json["locations"]
    if len(locations) < 2:
        return jsonify({ "error": "At least two locations are required for route optimization." })
    
    # Call the routeopt.py module to optimize the route
    optimized_route = optimize_route(locations)
    
    return jsonify({ "optimized_route": optimized_route })