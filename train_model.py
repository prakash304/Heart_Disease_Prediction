
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
import joblib
import os

print("Loading dataset...")
df = pd.read_csv("framingham.csv")
print(f"Dataset shape: {df.shape}")

df.dropna(axis=0, inplace=True)
print(f"After dropping NaN: {df.shape}")

X = df.iloc[:, 0:15]
y = df.iloc[:, 15]

feature_names = list(X.columns)
print(f"Features: {feature_names}")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=21
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\nTraining Logistic Regression model...")
model = LogisticRegression(max_iter=1000, random_state=21)
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/heart_model.pkl")
joblib.dump(scaler, "model/scaler.pkl")
joblib.dump(feature_names, "model/feature_names.pkl")

print("\nModel saved to model/heart_model.pkl")
print("Scaler saved to model/scaler.pkl")
print("Feature names saved to model/feature_names.pkl")
print("\nTraining complete! You can now run: python app.py")
