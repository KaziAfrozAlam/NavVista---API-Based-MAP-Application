from flask import Flask, render_template, request, jsonify
from fuel_efficiency import calculate_fuel_efficiency

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('templates/index.html')

@app.route('/calculate_efficiency', methods=['POST'])
def calculate_efficiency():
    try:
        # Get parameters from the form
        distance = float(request.form['distance'])
        fuel_used = float(request.form['fuel_used'])

        # Calculate fuel efficiency using the fuel_efficiency.py script
        efficiency = calculate_fuel_efficiency(distance, fuel_used)

        # Return the result as JSON
        return jsonify({'efficiency': efficiency})
    except ValueError:
        return jsonify({'error': 'Invalid input. Please enter valid numbers for distance and fuel used.'})

if __name__ == "__main__":
    app.run(debug=True)
