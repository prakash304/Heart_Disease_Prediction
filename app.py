from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import os

app = Flask(__name__)

# Paths
MODEL_PATH = "model/heart_model.pkl"
SCALER_PATH = "model/scaler.pkl"
FEATURES_PATH = "model/feature_names.pkl"

# Global variables
model = None
scaler = None
feature_names = None

# Load model function
def load_model():
    global model, scaler, feature_names
    if not os.path.exists(MODEL_PATH):
        print("ERROR: Model not found. Please run 'python train_model.py' first.")
        return False
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    feature_names = joblib.load(FEATURES_PATH)
    print("Model loaded successfully.")
    return True

# 🔥 LOAD MODEL HERE (AFTER FUNCTION DEFINITION)
load_model()

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded."}), 500

    try:
        data = request.get_json()

        features = [
            float(data.get("male", 0)),
            float(data.get("age", 0)),
            float(data.get("education", 1)),
            float(data.get("currentSmoker", 0)),
            float(data.get("cigsPerDay", 0)),
            float(data.get("BPMeds", 0)),
            float(data.get("prevalentStroke", 0)),
            float(data.get("prevalentHyp", 0)),
            float(data.get("diabetes", 0)),
            float(data.get("totChol", 0)),
            float(data.get("sysBP", 0)),
            float(data.get("diaBP", 0)),
            float(data.get("BMI", 0)),
            float(data.get("heartRate", 0)),
            float(data.get("glucose", 0)),
        ]

        X = np.array(features).reshape(1, -1)
        X_scaled = scaler.transform(X)

        prediction = int(model.predict(X_scaled)[0])
        probability = float(model.predict_proba(X_scaled)[0][1])

        if probability < 0.10:
            risk_level = "Low"
        elif probability < 0.20:
            risk_level = "Moderate"
        else:
            risk_level = "High"

        return jsonify({
            "prediction": prediction,
            "probability": round(probability * 100, 2),
            "risk_level": risk_level
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Run app (for deployment)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)