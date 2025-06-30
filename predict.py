
import joblib
import numpy as np
from flask import Flask, request, jsonify

# Load the model
model = joblib.load('model.joblib')

# Create Flask app
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # Get data from request
    data = request.get_json()
    
    # Extract features
    engagement_score = data.get('engagement_score', 0)
    experience_score = data.get('experience_score', 0)
    
    # Make prediction
    prediction = model.predict([[engagement_score, experience_score]])[0]
    
    # Return prediction
    return jsonify({
        'satisfaction_score': prediction,
        'model_version': '1.0.0'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
