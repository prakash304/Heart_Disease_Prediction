# Heart Disease Prediction — Full Stack Project

Predict a patient's **10-year coronary heart disease (CHD) risk** using a Logistic Regression model trained on the Framingham Heart Study dataset.

---

## Project Structure

```
heart_disease_project/
├── app.py                     # Flask web server
├── train_model.py             # Train & save the ML model
├── requirements.txt           # Python dependencies
├── framingham.csv             # Framingham Heart Study dataset
├── model/                     # Auto-created after training
│   ├── heart_model.pkl
│   ├── scaler.pkl
│   └── feature_names.pkl
├── templates/
│   └── index.html
├── static/
│   ├── css/style.css
│   └── js/main.js
└── Heart_disease_pred.ipynb   # Original EDA + modeling notebook
```

---

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the model
```bash
python train_model.py
```

### 3. Start the server
```bash
python app.py
```

### 4. Open browser
```
http://localhost:5000
```

---

## API

POST `/predict` with JSON body containing all 15 features.

Returns: `prediction`, `probability`, `risk_level`, `risk_flags`, `protective_flags`.

---

## Disclaimer

Educational use only. Not a substitute for professional medical advice.
