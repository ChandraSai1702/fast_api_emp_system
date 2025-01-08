from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

@app.route('/metrics', methods=['GET'])
def metrics():
    # Simulate some metrics
    metrics_data = {
        'temperature': random.uniform(20.0, 30.0),  # Random temperature value
        'humidity': random.uniform(40.0, 60.0),     # Random humidity value
        'timestamp': time.time()                    # Current time in seconds
    }
    return jsonify(metrics_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
