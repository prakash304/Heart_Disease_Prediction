from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import os

app = Flask(__name__)


MODEL_PATH = "model/heart_model.pkl"
SCALER_PATH = "model/scaler.pkl"
FEATURES_PATH = "model/feature_names.pkl"

model = None
scaler = None
feature_names = None

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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded. Run train_model.py first."}), 500

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

     
        risk_flags = []
        if float(data.get("age", 0)) > 55:
            risk_flags.append("Age > 55")
        if float(data.get("currentSmoker", 0)) == 1:
            risk_flags.append("Current smoker")
        if float(data.get("cigsPerDay", 0)) > 10:
            risk_flags.append(f"Heavy smoker ({int(data.get('cigsPerDay',0))} cigs/day)")
        if float(data.get("sysBP", 0)) > 140:
            risk_flags.append(f"High systolic BP ({data.get('sysBP')} mmHg)")
        if float(data.get("totChol", 0)) > 240:
            risk_flags.append(f"High cholesterol ({data.get('totChol')} mg/dL)")
        if float(data.get("BMI", 0)) > 30:
            risk_flags.append(f"Obesity (BMI {data.get('BMI')})")
        if float(data.get("diabetes", 0)) == 1:
            risk_flags.append("Diabetes")
        if float(data.get("prevalentHyp", 0)) == 1:
            risk_flags.append("Hypertension")
        if float(data.get("prevalentStroke", 0)) == 1:
            risk_flags.append("Previous stroke")
        if float(data.get("glucose", 0)) > 125:
            risk_flags.append(f"High glucose ({data.get('glucose')} mg/dL)")

        protective_flags = []
        if float(data.get("currentSmoker", 0)) == 0:
            protective_flags.append("Non-smoker")
        if float(data.get("sysBP", 0)) < 120:
            protective_flags.append("Normal BP")
        if float(data.get("BMI", 0)) < 25:
            protective_flags.append("Healthy BMI")
        if float(data.get("totChol", 0)) < 200:
            protective_flags.append("Normal cholesterol")
        if float(data.get("diabetes", 0)) == 0 and float(data.get("glucose", 0)) < 100:
            protective_flags.append("Normal glucose")

        return jsonify({
            "prediction": prediction,
            "probability": round(probability * 100, 2),
            "risk_level": risk_level,
            "risk_flags": risk_flags[:5],
            "protective_flags": protective_flags[:4],
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    if load_model():
        print("Starting server at http://localhost:5000")
        app.run(debug=True, port=5000)
    else:
        print("Please run 'python train_model.py' first, then restart app.py")
