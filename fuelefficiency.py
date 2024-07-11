import googlemaps
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

# Replace 'YOUR_GOOGLE_MAPS_API_KEY' with your actual API key
google_maps_api_key = 'AIzaSyBDIBv5G7hhvHHGi3fb4bjGja3xuPRFjWw'
gmaps = googlemaps.Client(key='AIzaSyBDIBv5G7hhvHHGi3fb4bjGja3xuPRFjWw')

def get_route_distance(origin, destination):
    # Get the route distance in meters using Google Maps API
    directions_result = gmaps.directions(origin, destination, mode="driving")
    distance_meters = directions_result[0]['legs'][0]['distance']['value']
    return distance_meters

# Example dataset
origins = ["New York, NY", "San Francisco, CA", "Los Angeles, CA"]
destinations = ["Boston, MA", "Seattle, WA", "Chicago, IL"]

# Fetch route distances
X = np.array([get_route_distance(o, d) for o, d in zip(origins, destinations)]).reshape(-1, 1)

# Example target variable (fuel efficiency)
y = np.array([25.0, 30.0, 22.0])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
predictions = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, predictions)
print(f"Mean Squared Error: {mse}")

# Example: Predict fuel efficiency for a new route
new_route_distance = get_route_distance("Miami, FL", "Dallas, TX")
predicted_fuel_efficiency = model.predict([[new_route_distance]])
print(f"Predicted Fuel Efficiency for the new route: {predicted_fuel_efficiency[0]}")