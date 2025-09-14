# app.py
from flask import Flask, render_template, request
import json
import joblib
import numpy as np
import os

app = Flask(__name__)

# Load artifacts with error handling
try:
    model = joblib.load("model.pkl")
    scaler = joblib.load("scaler.pkl")
    label_encoder = joblib.load("label_encoder.pkl")
    
    with open("feature_order.json", "r", encoding="utf-8") as f:
        FEATURE_ORDER = json.load(f)
    
    print("✅ All model files loaded successfully!")
    
except Exception as e:
    print(f"❌ Error loading model files: {e}")

EXPECTED_FEATURES = len(FEATURE_ORDER) if 'FEATURE_ORDER' in locals() else 25

@app.route("/")
def home():
    questions = [
        "Gender",
        "Age", 
        "Have you recently experienced stress in your life?",
        "Have you noticed a rapid heartbeat or palpitations?",
        "Have you been dealing with anxiety or tension recently?",
        "Do you face any sleep problems or difficulties falling asleep?",
        "Have you been getting headaches more often than usual?",
        "Do you get irritated easily?",
        "Do you have trouble concentrating on your academic tasks?",
        "Have you been feeling sadness or low mood?",
        "Have you been experiencing any illness or health issues?",
        "Do you often feel lonely or isolated?",
        "Do you feel overwhelmed with your academic workload?",
        "Are you in competition with your peers, and does it affect you?",
        "Do you find that your relationship often causes you stress?",
        "Are you facing any difficulties with your professors or instructors?",
        "Is your working environment unpleasant or stressful?",
        "Do you struggle to find time for relaxation and leisure activities?",
        "Is your hostel or home environment causing you difficulties?",
        "Do you lack confidence in your academic performance?",
        "Do you lack confidence in your choice of academic subjects?",
        "Academic and extracurricular activities conflicting for you?",
        "Do you attend classes regularly?",
        "Have you gained/lost weight?",
        "How would you rate your overall stress level?"
    ]
    
    return render_template("index.html", questions=questions)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        values = []
        
        for i in range(1, EXPECTED_FEATURES + 1):
            val = request.form.get(f"q{i}", "").strip()
            if val == "":
                return render_template("result.html", result=f"⚠️ Missing answer for Question {i}")
            values.append(float(val))
        
        feature_array = np.array(values, dtype=float).reshape(1, -1)
        scaled_features = scaler.transform(feature_array)
        prediction_index = model.predict(scaled_features)[0]
        stress_category = label_encoder.inverse_transform([prediction_index])[0]
        
        return render_template("result.html", result=stress_category)
        
    except Exception as e:
        return render_template("result.html", result="❌ Error during prediction. Please try again.")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)