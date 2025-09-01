# app.py
from flask import Flask, render_template, request
import json
import joblib
import numpy as np

app = Flask(__name__)

# Load artifacts
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")
label_encoder = joblib.load("label_encoder.pkl")

with open("feature_order.json", "r", encoding="utf-8") as f:
    FEATURE_ORDER = json.load(f)   # list of 25 feature column names

EXPECTED_FEATURES = len(FEATURE_ORDER)  # should be 25

@app.route("/")
def home():
    # Pass questions to the template (25 questions, no target question)
    questions = [
        "Gender",
        "Age",
        "Have you recently experienced stress in your life?",
        "Have you noticed a rapid heartbeat or palpitations?",
        "Have you been dealing with anxiety or tension recently?",
        "Do you face any sleep problems or difficulties falling asleep?",
        "Have you been dealing with anxiety or tension recently?.1",  # duplicated column in CSV but kept once after dedup
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
        "Have you gained/lost weight?"
        # NOTE: The target "Which type of stress..." is NOT part of the form
    ]

    # Safety: if feature order differs from these labels, the backend still uses FEATURE_ORDER.json keys
    return render_template("index.html", questions=questions)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Collect values in the SAME ORDER used during training (FEATURE_ORDER)
        # We expect fields named f"q1"..."q25" from the form.
        values = []
        for i in range(1, EXPECTED_FEATURES + 1):
            val = request.form.get(f"q{i}", "").strip()
            if val == "":
                return render_template("result.html", result=f"⚠️ Missing answer for Question {i}")
            values.append(float(val))

        # Shape check
        arr = np.array(values, dtype=float).reshape(1, -1)
        if arr.shape[1] != EXPECTED_FEATURES:
            return render_template("result.html", result=f"⚠️ Expected {EXPECTED_FEATURES} features, got {arr.shape[1]}.")

        # Scale and predict
        arr_s = scaler.transform(arr)
        pred_idx = model.predict(arr_s)[0]
        pred_label = label_encoder.inverse_transform([pred_idx])[0]

        return render_template("result.html", result=pred_label)

    except Exception as e:
        return render_template("result.html", result=f"Error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
