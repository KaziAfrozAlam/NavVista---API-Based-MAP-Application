# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import joblib

# Sample dataset (replace this with your actual dataset)
data = {
    'Distance': [100, 200, 300, 400, 500],
    'Speed': [50, 60, 55, 45, 65],
    'FuelConsumption': [10, 15, 18, 20, 12]
}

df = pd.DataFrame(data)

# Split the dataset into features (X) and target variable (y)
X = df[['Distance', 'Speed']]
y = df['FuelConsumption']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a pipeline with a RandomForestRegressor
model = make_pipeline(StandardScaler(), RandomForestRegressor(random_state=42))

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
predictions = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, predictions)
print(f'Mean Squared Error: {mse}')

# Save the trained model for future use
joblib.dump(model, 'fuel_optimization_model.joblib')
